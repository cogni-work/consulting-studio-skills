"""Prepare a partial Creator update; never publish or change the 27-method release."""
import argparse
import copy
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat
import tarfile
import zipfile

HERE = Path(__file__).resolve().parent
SCHEMA = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
ENTRY = './skills/setup/SKILL.md'
SETUP_FILES = ('skills/setup/SKILL.md', 'skills/setup/agents/openai.yaml',
               'skills/setup/references/optional-synthetic-example.md',
               'skills/setup/references/pages-setup.md')
REQUIRED = (
    'skills/org-specialize/SKILL.md',
    'skills/org-specialize/references/governing.md',
    'skills/org-specialize/references/source/implementation/skills/workspace-bindings/procedure.md',
    'skills/org-specialize/references/source/implementation/workspace-bindings/contract.md',
    'skills/org-specialize/references/source/implementation/business-skills/installation-storage-lifecycle.md',
)
REFERENCE_MAP = dict(zip((
    '../../../skills/org-specialize/SKILL.md',
    '../../../skills/workspace-bindings/SKILL.md',
    '../../../workspace-bindings/contract.md',
    '../../../business-skills/installation-storage-lifecycle.md',
), (REQUIRED[0], REQUIRED[2], REQUIRED[3], REQUIRED[4])))


def require(value, message):
    if not value:
        raise ValueError(message)


def safe_path(path):
    require(isinstance(path, str) and path and '\\' not in path,
            'Invalid package path')
    parts = PurePosixPath(path).parts
    require(not path.startswith('/') and all(p not in ('.', '..') for p in parts)
            and str(PurePosixPath(path)) == path, 'Unsafe package path: ' + path)
    return path


def read_package(path):
    """Read an exact root archive/directory; reject links, traversal and duplicates."""
    path = Path(path)
    files = {}

    def add(name, data):
        safe_path(name)
        require(name not in files, 'Duplicate member: ' + name)
        files[name] = data

    if path.is_dir():
        for item in sorted(path.rglob('*')):
            require(not item.is_symlink(), 'Package symlink: ' + str(item))
            if item.is_file():
                add(item.relative_to(path).as_posix(), item.read_bytes())
    elif zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for member in archive.infolist():
                require(not stat.S_ISLNK(member.external_attr >> 16), 'Archive symlink')
                if not member.is_dir():
                    add(member.filename, archive.read(member))
    else:
        with tarfile.open(path, 'r:*') as archive:
            for member in archive:
                require(member.isdir() or member.isfile(), 'Nonregular archive member')
                if member.isfile():
                    add(member.name, archive.extractfile(member).read())
    require('plugin.json' in files, 'Expected one plugin at archive root')
    require(not any(p.endswith('/plugin.json') and p != '.codex-plugin/plugin.json'
                    for p in files), 'Nested plugin manifest')
    return files


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def version_tuple(version):
    require(isinstance(version, str) and re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', version),
            'Expected a plain stable SemVer')
    return tuple(map(int, version.split('.')))


def compose(original, version, setup=None, reference_map=None):
    """Return manifests/Setup files and evidence of every retained input byte."""
    for name in original:
        safe_path(name)
    manifest = json.loads(original['plugin.json'])
    require(manifest.get('$schema') == SCHEMA, 'Expected current portable manifest')
    require(isinstance(manifest.get('extensions'), dict)
            and isinstance(manifest['extensions'].get('com.openai'), dict),
            'Inspect and migrate effective legacy-only settings before this overlay')
    require(version_tuple(version) > version_tuple(manifest.get('version')), 'Version must increase')
    methods = sorted(p for p in original if re.fullmatch(r'skills/[^/]+/SKILL.md', p))
    require(len(methods) == 27 and 'skills/setup/SKILL.md' not in methods,
            'Expected the inspected 27-method predecessor without Setup')
    reference_map = REFERENCE_MAP if reference_map is None else reference_map
    required = REQUIRED if reference_map is REFERENCE_MAP else (REQUIRED[1], *reference_map.values())
    for path in required:
        require(path in original, 'Missing existing Setup dependency: ' + path)
    require(not any(p.startswith('skills/setup/') for p in original),
            'Setup already exists; inspect and reconcile before updating')
    setup = dict(setup) if setup is not None else {p: (HERE / p).read_bytes() for p in SETUP_FILES}
    require(set(setup) == set(SETUP_FILES), 'Unexpected Setup files')
    require(setup['skills/setup/SKILL.md'].startswith(b'---\nname: setup\n'), 'Invalid Setup entry')
    source_setup = setup['skills/setup/SKILL.md']
    text = source_setup.decode()
    for source, destination in reference_map.items():
        require(text.count('](' + source + ')') == 1, 'Expected exact Setup source link: ' + source)
        relative = posixpath.relpath(destination, 'skills/setup')
        text = text.replace('](' + source + ')', '](' + relative + ')')
    setup['skills/setup/SKILL.md'] = text.encode()
    updated = copy.deepcopy(manifest)
    updated['version'] = version
    extensions = updated.setdefault('extensions', {})
    require(isinstance(extensions, dict), 'Invalid extensions')
    openai = extensions.setdefault('com.openai', {})
    require(isinstance(openai, dict), 'Invalid OpenAI extension')
    require('onboardingSkill' not in openai, 'Existing onboarding entry needs reconciliation')
    openai['onboardingSkill'] = ENTRY
    overlay = {'plugin.json': encode(updated), **setup}
    legacy_path = '.codex-plugin/plugin.json'
    if legacy_path in original:
        legacy = json.loads(original[legacy_path])
        require(legacy.get('name') == manifest.get('name')
                and legacy.get('version') == manifest.get('version'), 'Compatibility identity mismatch')
        legacy['version'] = version
        legacy.setdefault('extensions', {}).setdefault('com.openai', {})['onboardingSkill'] = ENTRY
        overlay[legacy_path] = encode(legacy)
    effective = {**original, **overlay}
    for path, data in setup.items():
        if not path.endswith('.md'):
            continue
        for target in re.findall(r'\]\(([^)]+)\)', data.decode()):
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
            safe_path(resolved)
            require(resolved in effective, 'Missing Setup reference: ' + resolved)
    hashes = lambda files: {p: hashlib.sha256(data).hexdigest() for p, data in sorted(files.items())}
    receipt = {'schema_version': 1, 'old_version': manifest['version'], 'new_version': version,
               'onboarding_skill': ENTRY, 'business_methods': 27,
               'changed_or_added': sorted(overlay),
               'retained_sha256': hashes({p: d for p, d in original.items() if p not in overlay}),
               'overlay_sha256': hashes(overlay),
               'setup_source_sha256': hashlib.sha256(source_setup).hexdigest(),
               'reference_adaptations': reference_map,
               'native_fresh': 'NOT_RUN', 'native_existing': 'NOT_RUN'}
    return overlay, receipt


def zip_bytes(files):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path, data in sorted(files.items()):
            safe_path(path)
            member = zipfile.ZipInfo(path, (2026, 1, 1, 0, 0, 0))
            member.external_attr = 0o100644 << 16
            member.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(member, data)
    return output.getvalue()


def write_once(path, data):
    path = Path(path)
    if path.exists():
        require(path.read_bytes() == data, 'Conflicting existing artifact: ' + str(path))
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--version', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    original = read_package(args.source)
    overlay, receipt = compose(original, args.version)
    require(args.output.resolve() != args.source.resolve()
            and args.source.resolve() not in args.output.resolve().parents,
            'Output must be outside inspected source')
    artifacts = {'rollback.zip': zip_bytes(original), 'update.zip': zip_bytes(overlay),
                 'preservation.json': encode(receipt)}
    # Check the entire retry before writing any artifact.
    for name, data in artifacts.items():
        path = args.output / name
        require(not path.exists() or path.read_bytes() == data, 'Conflicting existing artifact: ' + str(path))
    for name, data in artifacts.items():
        write_once(args.output / name, data)
    print(json.dumps({'business_methods': 27, 'overlay_files': sorted(overlay),
                      'retained_files': len(receipt['retained_sha256']),
                      'output': str(args.output), 'native_tests': 'NOT_RUN'}))


if __name__ == '__main__':
    main()
