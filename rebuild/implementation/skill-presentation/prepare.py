#!/usr/bin/env python3
"""Build the unpublished, presentation-corrected S/App candidates locally."""
import argparse
import copy
import hashlib
import importlib.util
import json
import posixpath
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SKILLS_VERSION = '1.2.2'
APP_VERSION = '1.1.2'
ARCHIVE = 'consulting-studio-skills.zip'
REBUILD_ARCHIVE = 'consulting-studio-skills-1.2.2-rebuild.zip'
BASE = '1b207ee2d34620b44728522fe83023567a3ceedb'
PUBLIC_BASE = 'a3bf76f9b157c0a4c080258253f16f5a855db39a'
STANDING = 'UNPUBLISHED CANDIDATE; publication, installation, runtime and customer acceptance NOT_RUN'
REBUILD = b'''# Rebuild the unpublished S candidate\n\nPython standard library only. Extract into an empty directory, then run:\n\n    python3 -B implementation/skill-presentation/prepare.py --rebuild-from . --output ../rebuilt\n\nCompare every output with SHA256SUMS. No Git, network, App source or credentials\nare required. This rebuild does not authorize publication or installation.\n'''


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


aligned = load('presentation_aligned_primitives', 'implementation/aligned-release/prepare.py')
content = load('presentation_content', 'implementation/skill-presentation/content.py')
require, encoded, decode = aligned.require, aligned.encoded, aligned.decode
sha = lambda data: hashlib.sha256(data).hexdigest()


def checksums(outputs):
    return ''.join(sha(data) + '  ' + path + '\n' for path, data in sorted(outputs.items())).encode()


def rows(files):
    return {p: dict(sha256=sha(d), bytes=len(d)) for p, d in sorted(files.items())}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode().strip()


def input_set(source_commit=None, rebuild=None):
    if rebuild:
        root = Path(rebuild).absolute()
        context = decode(aligned.regular(root / 'input-context.json'))
        selected = decode(aligned.regular(root / aligned.SELECTION))
        canonical = {r['path']: aligned.regular(root / ('canonical/' + r['path'])) for r in selected['files']}
        tools = {p: aligned.regular(root / p) for p in context['tools']}
        require(rows(tools) == context['tools'], 'Finite rebuild tooling drift')
        expected = {'input-context.json', 'REBUILD.md', *tools, *('canonical/' + p for p in canonical)}
        require(aligned.ex.read_exact_tree(root, expected) == {
            **tools, **{'canonical/' + p: d for p, d in canonical.items()},
            'input-context.json': encoded(context), 'REBUILD.md': REBUILD}, 'Finite input allowlist drift')
    else:
        source_commit = source_commit or git('rev-parse', 'HEAD')
        require(len(source_commit) == 40 and git('rev-parse', source_commit) == source_commit,
                'Exact local source commit required')
        selected, canonical, tools = aligned.inputs()
        # The 93 method/resource bytes are also verified at this candidate's
        # active source, so historical selection pins cannot hide source drift.
        for path, data in canonical.items():
            require(data == subprocess.check_output(['git', 'show', source_commit + ':' + path], cwd=ROOT),
                    'Current canonical resource drift: ' + path)
        tools.update({p: aligned.regular(ROOT / p) for p in (
            'implementation/skill-presentation/prepare.py',
            'implementation/skill-presentation/content.py',
            'implementation/skill-presentation/README.md')})
        context = dict(schema='consulting-studio/presentation-inputs@1', source_commit=source_commit,
            source_tree=git('rev-parse', source_commit + '^{tree}'), baseline=BASE,
            public_baseline=PUBLIC_BASE, tools=rows(tools))
    aligned.Source(selected, canonical)
    return selected, canonical, tools, context


def build_s(selected, canonical, tools, context):
    aligned.SKILLS_VERSION = SKILLS_VERSION
    files, info = aligned.public_plugin(selected, canonical, tools)
    files.pop('distribution.json')
    files, evidence = content.finalize(files, profile='S')
    info = copy.deepcopy(info)
    for row in info['canonical_to_emitted']:
        row['output_path'] = evidence.get('relocations', {}).get(row['output_path'], row['output_path'])
        row['emitted_sha256'] = sha(files[row['output_path']])
    info.update(schema='consulting-studio/presentation-candidate@1', version=SKILLS_VERSION,
        standing=STANDING, source_commit=context['source_commit'], source_tree=context['source_tree'],
        method_source=dict(commit=selected['source_commit'], tree=selected['source_tree'],
            verified_at_candidate_source=True), generator_inputs={p: sha(d) for p, d in sorted(tools.items())},
        presentation=dict(record='metadata/skill-presentation.json', coverage=evidence['coverage'],
            changed_files=len(evidence['changed_files']), relocated_files=len(evidence['relocations'])),
        delivery_gates=dict(publication='NOT_AUTHORIZED', installation='NOT_AUTHORIZED',
            exact_current_release_review='PENDING'))
    info['legal'] = dict(status='UNPUBLISHED_CANDIDATE_NO_NEW_GRANT',
        prior_public_source=PUBLIC_BASE, license_sha256=sha(files['LICENSE']), notice_sha256=sha(files['NOTICE']),
        retained='Existing license, attribution and exact relocated per-file legal records retained; no new grant or withdrawal',
        provenance_review='The 93 selected inputs contain 91 Consulting Studio instruction/configuration files plus LICENSE/NOTICE. No modified third-party-authored instruction resource was identified; conceptual credits do not establish copied third-party source.',
        release_gate='Current publication is not authorized; historical release authority is not reused')
    files['legal/scope.json'] = encoded(info['legal'])
    files['metadata/skill-presentation.json'] = encoded(evidence)
    files['MODIFICATIONS.md'] = ("# Unpublished presentation correction\n\n"
        "Packaging comments and nonfunctional build records are excluded from skills. "
        "Functional method instructions and resource navigation remain. Exact source and emitted "
        "hashes, per-file changes and relocated original notices are recorded in distribution.json "
        "and metadata/skill-presentation.json. Display names use the unchanged technical skill names.\n\n"
        "The selected instruction changes concern first-party Consulting Studio text and generated "
        "packaging notes. No modified third-party-authored instruction resource was identified. No new license "
        "grant, publication, installation or host qualification follows from this local build.\n").encode()
    # Recheck functional navigation after legal/metadata relocation as well as the
    # complete skill closure. Provenance is never fed back into instruction text.
    aligned.ex.full_links(files)
    content.validate(files)
    info['files'] = rows(files)
    files['distribution.json'] = encoded(info)
    return files, info


def s_inputs(source_commit=None, *, rebuild=None):
    selected, canonical, tools, context = input_set(source_commit, rebuild)
    files, info = build_s(selected, canonical, tools, context)
    inputs = {**tools, **{'canonical/' + p: d for p, d in canonical.items()},
        'input-context.json': encoded(context), 'REBUILD.md': REBUILD}
    outputs = {ARCHIVE: aligned.pack.zip_bytes(files), REBUILD_ARCHIVE: aligned.pack.zip_bytes(inputs),
        'distribution.json': files['distribution.json'], 'selection.json': encoded(selected)}
    require(aligned.pack.unpack(outputs[ARCHIVE], files) == files, 'S archive byte fidelity')
    outputs['SHA256SUMS'] = checksums(outputs)
    return outputs, files, info


def app_inputs(original, source_commit, s_outputs, skills, s_info):
    """Prepare complete local App bytes from a pinned cache, never an update."""
    portable, legacy = decode(original['plugin.json']), decode(original['.codex-plugin/plugin.json'])
    require(portable['version'] == legacy['version'] == '1.1.1', 'Exact prior App1.1.1 source required')
    require(portable['name'] == legacy['name'], 'App identity mismatch')
    require(portable['extensions']['com.openai']['onboardingSkill'] == './skills/setup/SKILL.md', 'App onboarding drift')
    require('.app.json' in original, 'Existing App binding required')
    names = set(s_info['auxiliary_skills']) | {row['name'] for row in s_info['methods']}
    require({p.split('/')[1] for p in original if p.startswith('skills/')} <= names, 'Unknown App adaptation requires review')
    common = {p: d for p, d in skills.items() if p.startswith('skills/') and not p.startswith('skills/studio-resume/')}
    # Compare the complete cleaned instruction payload. This permits only the
    # enumerated packaging corrections and rejects unknown human adaptations.
    cleaned_original, previous_evidence = content.finalize(original, profile='App')
    previous_common = {p: d for p, d in cleaned_original.items()
                       if p.startswith('skills/') and not p.startswith('skills/studio-resume/')}
    require(previous_common == common, 'Unreconciled App instruction adaptation')
    resume, mapping = aligned.app_resume_payload(skills)
    require({p: d for p, d in cleaned_original.items() if p.startswith('skills/studio-resume/')} == resume,
            'Unreconciled App Resume adaptation')
    effective = {p: d for p, d in cleaned_original.items()
                 if not p.startswith('skills/') and p != 'consulting-studio-skills.json'}
    effective.update(common)
    effective.update(resume)
    for p in ('plugin.json', '.codex-plugin/plugin.json'):
        value = decode(original[p]); value['version'] = APP_VERSION
        effective[p] = encoded(value)
    effective, evidence = content.finalize(effective, profile='App')
    # Preserve the exact original App legal copies, which may differ from S.
    # Current shared manifests are refreshed against those actual payload bytes.
    for p, d in skills.items():
        if p.startswith('metadata/skills/') and '/studio-resume/' not in p:
            effective[p] = d
    for p, data in list(effective.items()):
        if p.startswith('metadata/skills/') and p.endswith('/manifest.json'):
            manifest = decode(data); prefix = manifest['payload_root'] + '/'
            def actual(relative):
                target = posixpath.normpath(prefix + relative)
                require(target in effective, 'Missing App manifest payload: ' + target)
                return sha(effective[target])
            manifest['files'] = {path: actual(path) for path in manifest['files']}
            for resource in manifest['resources']:
                resource['emitted_sha256'] = actual(resource['emitted_path'])
            effective[p] = encoded(manifest)
    evidence['previous_app_cleanup'] = previous_evidence
    info = dict(schema='consulting-studio/presentation-app-candidate@1', version=APP_VERSION,
        source_commit=source_commit, source_tree=git('rev-parse', source_commit + '^{tree}'), standing=STANDING,
        previous_version='1.1.1', previous_source_sha256=sha(aligned.pack.zip_bytes(original)),
        shared_s_version=SKILLS_VERSION, shared_s_archive_sha256=sha(s_outputs[ARCHIVE]),
        presentation=dict(record='metadata/skill-presentation.json', coverage=content.validate(effective)),
        app_resume_mapping=mapping, shared_legal=s_info['legal'],
        preserved_settings='All manifest fields except version and all App binding bytes retained',
        deletion_paths=sorted(p for p in original if p not in effective),
        update='NOT_AUTHORIZED; complete local inspection artifact only, no partial-update claim',
        host_qualification='NOT_RUN; chat routing and runtime parity unproven')
    for p in ('plugin.json', '.codex-plugin/plugin.json'):
        before, after = decode(original[p]), decode(effective[p]); after['version'] = before['version']
        require(before == after, 'App settings changed: ' + p)
    require(effective['.app.json'] == original['.app.json'], 'App binding changed')
    aligned.ex.full_links({p: d for p, d in effective.items() if p.startswith('skills/')})
    content.validate(effective)
    effective['metadata/skill-presentation.json'] = encoded(evidence)
    info['files'] = rows(effective)
    effective['consulting-studio-skills.json'] = encoded(info)
    return effective, info


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-commit')
    parser.add_argument('--rebuild-from', type=Path)
    parser.add_argument('--app-source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not (args.rebuild_from and args.app_source), 'Standalone S rebuild excludes private App input')
    if not args.rebuild_from:
        require(args.source_commit == git('rev-parse', 'HEAD'), 'Pin current committed source')
        require(not git('status', '--porcelain', '--untracked-files=all'), 'Commit and review source before final build')
    outputs, files, info = s_inputs(args.source_commit, rebuild=args.rebuild_from)
    if args.app_source:
        original = aligned.setup.read_package(args.app_source)
        effective, app_info = app_inputs(original, args.source_commit, outputs, files, info)
        outputs['consulting-studio-App-' + APP_VERSION + '-complete-candidate.zip'] = aligned.pack.zip_bytes(effective)
        outputs['app-distribution.json'] = encoded(app_info)
        outputs['SHA256SUMS'] = checksums({p: d for p, d in outputs.items() if p != 'SHA256SUMS'})
    aligned.ex.write_outputs(args.output, outputs)
    print(json.dumps(dict(version=SKILLS_VERSION, App=APP_VERSION if args.app_source else None,
        archive_sha256=sha(outputs[ARCHIVE]), status=STANDING), sort_keys=True))


if __name__ == '__main__':
    main()
