#!/usr/bin/env python3
"""Build or validate a complete private Creator ZIP from pinned repository source."""
import argparse
import copy
import importlib.util
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


methods = load('standalone_methods', 'implementation/business-skills/release.py')
setup = load('standalone_setup', 'implementation/plugin-setup/package_update.py')
# check_packages imports its sibling as `release`; scope that alias to its load.
previous = sys.modules.get('release')
sys.modules['release'] = methods
try:
    links = load('standalone_links', 'implementation/business-skills/check_packages.py')
finally:
    if previous is None:
        del sys.modules['release']
    else:
        sys.modules['release'] = previous

require, digest, encoded = methods.require, methods.digest, methods.encoded
STAMP = (1980, 1, 1, 0, 0, 0)
MAX_ARCHIVE_BYTES = 128 * 1024 * 1024
MAX_TOTAL_BYTES = 128 * 1024 * 1024
MAX_MEMBER_BYTES = 8 * 1024 * 1024
MAX_MEMBERS = 4096
INPUTS = (
    'implementation/plugin-distribution/release.py',
    'implementation/plugin-distribution/release.json',
    'implementation/plugin-distribution/plugin.json',
    'implementation/plugin-distribution/runtime-readme.md',
    'implementation/business-skills/release.py',
    'implementation/business-skills/check_packages.py',
    'implementation/plugin-setup/package_update.py',
    'implementation/plugin-setup/skills/setup/SKILL.md',
    'implementation/plugin-setup/skills/setup/agents/openai.yaml',
    'implementation/plugin-setup/skills/setup/references/optional-synthetic-example.md',
    'implementation/plugin-setup/skills/setup/references/pages-setup.md',
)


def safe_path(path):
    require(isinstance(path, str) and path and '\\' not in path and ':' not in path
            and not any(ord(c) < 32 for c in path), 'Unsafe archive path: ' + repr(path))
    parts = PurePosixPath(path)
    require(not parts.is_absolute() and '..' not in parts.parts
            and str(parts) == path and path != '.', 'Unsafe archive path: ' + path)
    return path


def zip_bytes(files, compresslevel=9):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=compresslevel) as archive:
        for name, data in sorted(files.items()):
            safe_path(name)
            info = zipfile.ZipInfo(name, STAMP)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data, compresslevel=compresslevel)
    return stream.getvalue()


def unpack(data, expected):
    """Preflight the exact inventory and bounded ZIP directory before inflation.

    This release uses ordinary single-disk, comment-free ZIP (not ZIP64). Payload
    compression bytes can differ; names, metadata, sizes and source bytes cannot.
    """
    require(22 <= len(data) <= MAX_ARCHIVE_BYTES, 'Archive byte limit')
    sizes = {p: len(value) for p, value in expected.items()}
    require(0 < len(sizes) <= MAX_MEMBERS and max(sizes.values()) <= MAX_MEMBER_BYTES
            and sum(sizes.values()) <= MAX_TOTAL_BYTES, 'Expected expansion limit')
    # Standard 22-byte end-of-central-directory record. Bound the directory
    # itself before ZipFile allocates entries; no comments, ZIP64 or disk splits.
    signature, disk, directory_disk, disk_count, count, directory_size, directory_offset, comment = \
        struct.unpack('<4s4H2LH', data[-22:])
    require(signature == b'PK\x05\x06' and disk == directory_disk == comment == 0
            and disk_count == count == len(sizes), 'ZIP directory/count mismatch')
    require(directory_size == sum(46 + len(p.encode('utf-8')) for p in sizes)
            and directory_offset + directory_size == len(data) - 22,
            'ZIP directory size/layout mismatch')
    # ZipFile follows this locator and can replace the ordinary EOCD's bounded
    # size/count with ZIP64 values before it allocates entries. This release's
    # size caps never need ZIP64, so reject that override before construction.
    require(data[-42:-38] != b'PK\x06\x07', 'ZIP64 directory override is unsupported')
    files, folded = {}, set()
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        infos = archive.infolist()
        require([info.filename for info in infos] == sorted(sizes), 'Full archive name/order inventory drift')
        offset, total = 0, 0
        for info in infos:
            name = safe_path(info.filename)
            require(name not in files and name.casefold() not in folded, 'Duplicate archive member')
            require(stat.S_IFMT(info.external_attr >> 16) == stat.S_IFREG
                    and (info.external_attr >> 16) & 0o777 == 0o644, 'Nonregular archive member')
            require(info.date_time == STAMP and info.create_system == 3
                    and info.create_version == info.extract_version == 20
                    and info.internal_attr == info.volume == 0
                    and not info.extra and not info.comment
                    and info.compress_type == zipfile.ZIP_DEFLATED
                    and info.flag_bits == (0 if name.isascii() else 0x800),
                    'Nondeterministic/unsupported archive metadata')
            require(info.file_size == sizes[name] and info.file_size <= MAX_MEMBER_BYTES,
                    'Member expansion size mismatch: ' + name)
            total += info.file_size
            require(total <= MAX_TOTAL_BYTES, 'Total expansion limit')
            require(info.header_offset == offset and offset + 30 <= directory_offset,
                    'ZIP local header layout mismatch')
            header = struct.unpack_from('<4s5H3L2H', data, offset)
            encoded_name = name.encode('utf-8')
            require(header == (b'PK\x03\x04', 20, info.flag_bits, zipfile.ZIP_DEFLATED,
                               0, 33, info.CRC, info.compress_size, info.file_size, len(encoded_name), 0)
                    and data[offset + 30:offset + 30 + len(encoded_name)] == encoded_name,
                    'ZIP local/central metadata mismatch')
            offset += 30 + len(encoded_name) + info.compress_size
            require(offset <= directory_offset, 'Compressed member overlaps directory')
            folded.add(name.casefold())
        require(offset == directory_offset and total == sum(sizes.values()), 'ZIP payload/total size mismatch')
        require(not archive.comment, 'Unexpected archive comment')
        # No member is opened until EVERY directory/name/size/header check passes.
        for info in infos:
            with archive.open(info) as member:
                value = member.read(sizes[info.filename] + 1)
                require(len(value) == sizes[info.filename] and not member.read(1),
                        'Expanded member size mismatch')
                files[info.filename] = value
    return files


def manifest_checks(files, names, version, auxiliary=('setup',)):
    require('plugin.json' in files, 'Expected plugin.json at archive root')
    portable = json.loads(files['plugin.json'])
    require(portable.get('$schema') == setup.SCHEMA, 'Unsupported portable manifest schema')
    name = portable.get('name')
    require(isinstance(name, str) and len(name) <= 64
            and re.fullmatch(r'[a-z0-9]+(?:[.-][a-z0-9]+)*', name), 'Invalid plugin name')
    require(portable.get('version') == version, 'Plugin version drift')
    require(not {'skills', 'mcpServers', 'apps', 'interface'} & portable.keys(), 'Legacy portable fields')
    openai = portable['extensions']['com.openai']
    require(openai.get('onboardingSkill') == setup.ENTRY, 'Missing Setup entry')
    interface = openai['interface']
    require(isinstance(interface['shortDescription'], str)
            and 0 < len(interface['shortDescription']) <= 30, 'Invalid listing subtitle')
    require(isinstance(interface['capabilities'], list), 'Invalid capabilities')
    legacy = json.loads(files['.codex-plugin/plugin.json'])
    for key in ('name', 'version', 'description', 'author', 'license'):
        require(legacy[key] == portable[key], 'Compatibility manifest drift: ' + key)
    require(legacy['interface'] == interface and legacy['skills'] == './skills'
            and legacy['extensions']['com.openai']['onboardingSkill'] == setup.ENTRY,
            'Compatibility presentation/Setup drift')
    entries = {p.split('/')[1] for p in files if re.fullmatch(r'skills/[^/]+/SKILL.md', p)}
    require(entries == set(names) | set(auxiliary), 'Complete method and auxiliary entry inventory required')
    require(sum(PurePosixPath(p).name.casefold() == 'skill.md' for p in files) == len(names) + len(auxiliary),
            'Unexpected nested skill registration')
    for name in entries:
        text = files[f'skills/{name}/SKILL.md'].decode('utf-8')
        # Canonical frontmatter uses these two plain scalar fields. No YAML rewrite.
        require(len(text.encode()) <= 1024 * 1024 and text.startswith('---\n'), 'Invalid skill entry')
        front = text.split('\n---\n', 1)[0]
        require(re.search(r'^name: ' + re.escape(name) + r'\s*$', front, re.M)
                and re.search(r'^description: \S.+$', front, re.M), 'Invalid skill frontmatter')


def build(config=None):
    config = json.loads((HERE / 'release.json').read_bytes()) if config is None else config
    setup.version_tuple(config['version'])
    source = methods.RuntimeSource(config['core_commit'])
    names = [i['name'] for i in source.catalog['skills']]
    canonical = {p: digest(source.read(p)) for paths in source.methods.values() for p in paths}
    generators = {p: digest((ROOT / p).read_bytes()) for p in INPUTS}
    files, rows = {}, []
    for name in names:
        skill = methods.assemble(source, name, config, generators)
        links.check_links(skill)
        # Preserve the existing individually importable shape and complete reads.
        manifest = json.loads(skill['manifest.json'])
        require(set(manifest['files']) == set(skill) - {'manifest.json'}, 'Method file inventory drift')
        require(all(digest(skill[p]) == sha for p, sha in manifest['files'].items()), 'Method hash drift')
        rows.append({'name': name, 'method_version': manifest['method_version'],
                     'modes': manifest['modes'], 'resources': len(manifest['resources']),
                     'manifest_sha256': digest(skill['manifest.json'])})
        files.update({f'skills/{name}/{p}': data for p, data in skill.items()})
    portable = json.loads((HERE / 'plugin.json').read_bytes())
    require(portable['version'] == config['version'], 'Release/manifest version mismatch')
    predecessor = copy.deepcopy(portable)
    predecessor['version'] = config['previous_business_bundle']
    del predecessor['extensions']['com.openai']['onboardingSkill']
    reference_map = dict(setup.REFERENCE_MAP)
    reference_map['../../../business-skills/installation-storage-lifecycle.md'] = (
        'skills/org-specialize/references/source/implementation/runtime/storage-lifecycle.md')
    overlay, setup_receipt = setup.compose({'plugin.json': encoded(predecessor), **files}, config['version'],
                                         reference_map=reference_map)
    require(json.loads(overlay['plugin.json']) == portable, 'Setup composition drift')
    files.update(overlay)
    files['plugin.json'] = (HERE / 'plugin.json').read_bytes()
    legacy = {key: portable[key] for key in ('name', 'version', 'description', 'author', 'license')}
    legacy.update(interface=portable['extensions']['com.openai']['interface'], skills='./skills',
                  extensions={'com.openai': {'onboardingSkill': setup.ENTRY}})
    files['.codex-plugin/plugin.json'] = encoded(legacy)
    for name in ('LICENSE', 'NOTICE'):
        files[name] = source.read(name)
    files['README.md'] = (HERE / 'runtime-readme.md').read_bytes()
    provenance = dict(
        schema_version=1, version=config['version'], source_repository=config['repository'],
        source_commit=source.commit, source_tree=source.tree, generator_inputs=generators,
        business_skills=27, modes=35, business_resources=len(canonical), auxiliary_skills=['setup'],
        methods=rows, canonical_business_sha256=canonical,
        resource_profile='operational',
        ancestry={key: config[key] for key in ('previous_core_commit', 'previous_business_bundle',
                  'previous_installed_plugin', 'previous_export_sha256')},
        transformations=[
            'Local resource links rewritten; common working instructions composed into skill entry points.',
            'Setup links resolve to packaged methods and location instructions.'],
        setup={'source_sha256': setup_receipt['setup_source_sha256'],
               'reference_adaptations': setup_receipt['reference_adaptations']},
        license_scope={
            'inherited_methods': 'All 27 business method folders preserve existing Apache-2.0 grants; their LICENSE/NOTICE include the current source text without withdrawing those grants.',
            'current_source': 'Root and per-method LICENSE/NOTICE are exact current pinned source bytes. LICENSE Part B retains the complete Apache-2.0 text and NOTICE the applicable upstream attributions.',
            'commercial_standard': 'LICENSE Part A applies only to separately identified future commercial deliveries expressly incorporated into an authorized agreement. This source archive creates no customer order, commercial agreement or relicensing of inherited material.',
            'component_list': 'files identifies every included component except distribution.json itself; canonical_business_sha256 identifies the exact included canonical method sources. No fonts, rendered fixtures, customer content or app bindings are included.'},
        standing=config['standing'],
        gates={p: 'NOT_RUN' for p in ('clean_install', 'native_execution', 'workspace_availability',
                                    'wa_adoption', 'owner_acceptance')},
        inventory_rule='SHA-256 of every regular file except distribution.json; archive SHA-256 is external to avoid self-reference.',
        files={p: digest(data) for p, data in sorted(files.items())})
    files['distribution.json'] = encoded(provenance)
    methods.check_runtime_instructions(files)
    manifest_checks(files, names, config['version'])
    # Setup points to sibling method resources; validate its final plugin-relative links.
    for match in methods.LINK.finditer(files['skills/setup/SKILL.md'].decode()):
        links.destination(files, 'skills/setup/SKILL.md', match.group(2))
    return files, provenance


def validate(data, expected=None):
    if expected is None:
        expected, _ = build()
    files = unpack(data, expected)
    require('distribution.json' in files, 'Missing complete distribution inventory')
    provenance = json.loads(files['distribution.json'])
    require(set(provenance['files']) == set(files) - {'distribution.json'}, 'Full file inventory drift')
    require(all(digest(files[p]) == sha for p, sha in provenance['files'].items()), 'Resource checksum mismatch')
    manifest_checks(files, [m['name'] for m in provenance['methods']], provenance['version'])
    require(files == expected, 'Pinned source/composition fidelity drift')
    return dict(version=provenance['version'], files=len(files), business_skills=27,
                auxiliary_skills=['setup'], modes=35, business_resources=provenance['business_resources'],
                source_commit=provenance['source_commit'], archive_sha256=digest(data),
                clean_install='NOT_RUN')


def read_archive(path):
    require(path.stat().st_size <= MAX_ARCHIVE_BYTES, 'Archive byte limit')
    with path.open('rb') as handle:
        data = handle.read(MAX_ARCHIVE_BYTES + 1)
    require(len(data) <= MAX_ARCHIVE_BYTES, 'Archive byte limit')
    return data


def write_outputs(output, artifacts):
    output = Path(output).absolute()
    for path in (output, *output.parents):
        require(not path.is_symlink(), 'Output/ancestor symlink: ' + str(path))
    require(not output.exists() or output.is_dir(), 'Output is not a directory')
    for name, data in artifacts.items():
        path = output / name
        require(not path.is_symlink() and (not path.exists() or path.is_file() and path.read_bytes() == data),
                'Conflicting existing artifact: ' + str(path))
    output.mkdir(parents=True, exist_ok=True)
    for name, data in artifacts.items():
        (output / name).write_bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output', type=Path)
    mode.add_argument('--check', type=Path)
    args = parser.parse_args()
    files, provenance = build()
    data = read_archive(args.check) if args.check else zip_bytes(files)
    result = validate(data, files)
    if args.output:
        name = 'consulting-studio-' + provenance['version'] + '.zip'
        write_outputs(args.output, {name: data,
            name + '.sha256': (digest(data) + '  ' + name + '\n').encode(),
            'distribution.json': files['distribution.json']})
        result['archive'] = str(args.output / name)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
