#!/usr/bin/env python3
"""Apply the exact approved S release license/identity; never install or publish."""
import argparse
import copy
import importlib.util
import io
import json
from pathlib import Path
import sys
import zipfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DOCUMENTS = ('README.md', 'CHANGELOG.md', 'KNOWN-LIMITS.md', 'SUPPORT.md',
             'SECURITY.md', 'OWNER-DECISIONS.md', 'INSTALL-TEST-PLAN.md', 'AUDIT.md')
SELF = 'implementation/s-distribution/prepare.py'
STANDING = 'RELEASE PREPARED, UNPUBLISHED; exact S grant approved; host installation and native behavior NOT_RUN'
PUBLIC_NAME = 'consulting-studio-skills'
VERSION = '0.1.0'
APPROVED_BASE = 'dba54c6644d58cd0ff31177f59e4691bd4343631'
APPROVED_TREE = 'a91be25ea522564a506ea0914ca013bf50e3527e'
APPROVED_SCOPE_SHA256 = '6248cbe9957b91b65e10413abb934b3ac33111f1e542fdd6419732ac6693f4b0'
APPROVED_DELTA_SHA256 = '19b525f388c8fd3f14d4fbb245cadc549cc7ae022c9729c0e49cb49cf25be2b4'
APACHE_SHA256 = 'c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4'
NOTICE_SHA256 = '4235c333ef37e7c6d8a352cda1ab9cd0880d4b5d21ba13892b32a81ee0ac94df'
MODIFICATION = ('Consulting Studio modification, 2026-10-27: local resource locators were packaged; '
                'an explicit working-instruction read was added where applicable. '
                'Exact source identities and changes are recorded in the accompanying manifests.')
REPO_ZIP = PUBLIC_NAME + '-' + VERSION + '-repository.zip'
PLUGIN_ZIP = PUBLIC_NAME + '-' + VERSION + '-plugin.zip'
# Exact prior own-source proposal reconstructed from PR218's frozen selection,
# tooling and authored repository inputs. This is evidence, never a grant.
PRIOR_SCOPE_BASE = '689f566c62e62c08b2259fc8268d51755bc46f99'
PRIOR_SCOPE_SHA256 = '95c788fd8b59720f82828ad7b8f8985be53c756c875dfd39025dda0a023428cd'
PRIOR_NORMALIZED_29_SHA256 = '5edc01d67c17a9a61b869db87dc5a0d9e59167605438d94e01e0ac7a8ff61540'
PRIOR_OWN_SOURCES = {'implementation/business-skills/check_packages.py': '34e029ad1cc6f2ae4efc7dcc940517d7b37fd8a931b7bc7d9de62eacc84818f6',
 'implementation/business-skills/release.py': '390d13c9bad337aa8bda6bc8520f96e8c7e153840d8391ca88b3dc3f408d8e8a',
 'implementation/plugin-distribution/plugin.json': '4a6d7c007663232cbb2ff7f63a3d1b200abd229afb9ed77873768c2d4004affb',
 'implementation/plugin-distribution/release.py': 'eba742770d15e858381dfef25096a3c6baccd121f3f8cbf8c72abfdae4d73aed',
 'implementation/plugin-distribution/runtime-readme.md': '9e540f820626e50e0544c05c1e1746dd5280325ef1636809cca6d6d848634ac4',
 'implementation/plugin-setup/package_update.py': '0e3c80d778e4c67508ca379badb3ca92f5703512830360c093fb08cc91976fd9',
 'implementation/plugin-setup/skills/setup/SKILL.md': '51d1452fa11d899ab479e15ce7e37aea2d797d97fe9644637954d43e38d7edd9',
 'implementation/plugin-setup/skills/setup/agents/openai.yaml': 'ab0f6232a7d85b3b0ab26e248e2515db90491eb801b0685f40d5f6fe7263eeae',
 'implementation/plugin-setup/skills/setup/references/optional-synthetic-example.md': '6cfa51ab5c0e2eca886de9cc295761a3162f589aec9c770e849682ca65b709ad',
 'implementation/plugin-setup/skills/setup/references/pages-setup.md': '01c0934af1cf438c0b70efbe6520f1bf3bd4ed3cbd51f4aa0a280f74672dfe84',
 'implementation/runtime/binding-catalog.json': 'd49b54b2de35cdbfd7cebd1652605d1d6d3874901832879e2668cba718e63ddf',
 'implementation/runtime/entity-lineage.md': 'b28c8e7334832eb74a34f516cb10f589c822aca7debb11bd1c73be51970a5060',
 'implementation/runtime/method-catalog.json': 'ab091c43ff0808411017878411edac3bd51c02844b138c0861a8257097de97d3',
 'implementation/runtime/requirements.md': 'ad4bdd895c553223337d4c0719b363df9c6a39c4e6ad01e601795c029c5e1094',
 'implementation/runtime/storage-lifecycle.md': 'cf6a451cd2b50fea805a6e4f34549978865e795c36b7e631847756d03dd47dae',
 'implementation/s-distribution/AUDIT.md': 'ddab72c797f6e3330ce80ec42db42546c2962b57c1a2f1fa34119916f22d0a33',
 'implementation/s-distribution/CHANGELOG.md': '091beb0e1521334fc01549773cb86a0fd6dd9ceeae18c16f2c5385ca005b0cef',
 'implementation/s-distribution/INSTALL-TEST-PLAN.md': '5135e4565fb218b2ce27c931b7ae5cc6fb024e79510199951f22c45cd5ed631f',
 'implementation/s-distribution/KNOWN-LIMITS.md': '3d7da914424924eeaeda6a17740e380c7d9c3a734575e26ad149e860d86dc4eb',
 'implementation/s-distribution/NOTICE-S.proposed.txt': '4235c333ef37e7c6d8a352cda1ab9cd0880d4b5d21ba13892b32a81ee0ac94df',
 'implementation/s-distribution/OWNER-DECISIONS.md': '316485fbdf1cfdc836377e4afd69351288c1ef05a3e907b33f1b04450d8b2520',
 'implementation/s-distribution/README.md': '4e61138bdd8465cf149dafa917bb6a967b6e1f6d6267f6deed71c054c7cbfc99',
 'implementation/s-distribution/SECURITY.md': '607c4d282feb842ac9ba8ce1fc100af3a68882c5e4205589b7f5667956022cd8',
 'implementation/s-distribution/SUPPORT.md': 'f7780284fa9ead5e5c89fa86465b40f784535f698c9be6d39dc83d6ce7ff77d5',
 'implementation/s-distribution/prepare.py': '1d607df5cae4dd2aaf4200b5297a0d61307f39acdb6b360f622630389999159f',
 'implementation/s-export/export.py': 'f904dfd06f4ec8582e2a2a9c17962c675722fa7602f1ee073c71bedf3b1eb330',
 'implementation/working-character/instructions.md': '3615768cb46db36a5bb362f77db7f8a67450f2cfb6f5508a094a569fb36df788',
 'implementation/workspace-bindings/architecture.md': '0de6465aa39a4f07bdec2a37b49d090a9960daef67db872b493e5dd7d1adb413',
 'implementation/workspace-bindings/contract.md': 'd4bb8aaaea4e3955834057fa65f80192e9f20861abb8a7606442ef7dfd2ee718'}



def exporter(rebuild=None):
    base = Path(rebuild).absolute() if rebuild else ROOT
    spec = importlib.util.spec_from_file_location('s_repository_export', base / 'implementation/s-export/export.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def modification_notice(path, data):
    """Prominent per-file notices; canonical inputs and legal texts stay exact."""
    if path.endswith('.md'):
        text = data.decode()
        offset = 0
        if text.startswith('---\n'):
            boundary = text.find('\n---\n', 4)
            if boundary < 0:
                raise ValueError('Unclosed frontmatter: ' + path)
            offset = boundary + len('\n---\n')
        return (text[:offset] + '\n<!-- ' + MODIFICATION + ' -->\n' + text[offset:]).encode()
    if path.endswith('.json'):
        value = json.loads(data)
        if not isinstance(value, dict) or 'distribution_modification_notice' in value:
            raise ValueError('Unsupported JSON modification notice: ' + path)
        value['distribution_modification_notice'] = MODIFICATION
        return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()
    raise ValueError('Unqualified changed source format: ' + path)


def approval():
    return dict(status='APPROVED_RELEASE_SPECIFIC', approved_at='2026-10-27T14:59:59Z',
        source='Product owner directly approved the exact expanded scope on 2026-10-27, '
               'following the 13:50 UTC initial grant/publication approval and 13:52 UTC timing instruction',
        approved_base=APPROVED_BASE, approved_tree=APPROVED_TREE,
        approved_scope_sha256=APPROVED_SCOPE_SHA256, approved_source_delta_sha256=APPROVED_DELTA_SHA256,
        meaning='31 exact S own sources plus two separate App adapter instruction sources; '
                'release-specific legal copies, public identity and consequent hash regeneration only')


def publication_authority():
    return dict(status='AUTHORIZED_AFTER_FINAL_CHECKS_AND_PARENT_INSTRUCTION',
        not_before='2026-10-27T16:00:00Z', local_time='2026-10-27T17:00:00+01:00 Europe/Berlin',
        repository='cogni-work/' + PUBLIC_NAME, executed=False, parent_only=True,
        marketplace='NOT_AUTHORIZED', workspace_installation='NOT_AUTHORIZED')


def approved_evidence(ex):
    evidence = {}
    for name, sha in (('approved-scope.json', APPROVED_SCOPE_SHA256),
                      ('approved-source-delta.json', APPROVED_DELTA_SHA256)):
        data = ex.regular_read(HERE / name)
        ex.require(ex.digest(data) == sha, 'Exact approved evidence drift: ' + name)
        evidence[name] = data
    scope = ex.decode(evidence['approved-scope.json'])
    delta = ex.decode(evidence['approved-source-delta.json'])
    ex.require(len(scope['canonical_components']) == 93 and len(scope['rebuild_tools']) == 6
               and len(scope['new_repository_components']) == 10
               and len(delta['s_components']) == 31
               and len(delta['separate_open_m_adapter_components']) == 2, 'Approved finite scope drift')
    return evidence, scope, delta


def legal_material(ex, canonical):
    apache = canonical['LICENSE'].split(b'PART B: APACHE LICENSE, VERSION 2.0\n\n', 1)[1]
    notice = ex.regular_read(HERE / 'NOTICE-S.proposed.txt')
    ex.require(ex.digest(apache) == APACHE_SHA256, 'Approved Apache text drift')
    ex.require(ex.digest(notice) == NOTICE_SHA256, 'Approved S notice text drift')
    return apache, notice


def plugin_candidate(ex, upstream, canonical):
    files = copy.deepcopy(upstream)
    original = ex.decode(files.pop('distribution.json'))
    apache, notice = legal_material(ex, canonical)
    for row in original['canonical_to_emitted']:
        path = row['output_path']
        if files[path] != canonical[row['canonical_path']] and path not in ('LICENSE', 'NOTICE'):
            files[path] = modification_notice(path, files[path])
    # Only operative legal copies change. Canonical rebuild inputs stay exact.
    for path in files:
        if Path(path).name in ('LICENSE', 'NOTICE'):
            files[path] = apache if Path(path).name == 'LICENSE' else notice
    for path in ('plugin.json', '.codex-plugin/plugin.json'):
        manifest = ex.decode(files[path])
        manifest.update(name=PUBLIC_NAME, version=VERSION, license='Apache-2.0')
        files[path] = ex.encoded(manifest)
    for path in sorted(files):
        if not (path.startswith('skills/') and path.endswith('/manifest.json')):
            continue
        before = files[path]
        manifest = ex.decode(before)
        prefix = path.rsplit('/', 1)[0] + '/'
        manifest['standing'] = STANDING
        if 'bundle_version' in manifest:
            manifest['bundle_version'] = VERSION
        manifest['release_identity'] = dict(name=PUBLIC_NAME, version=VERSION, license='Apache-2.0')
        for row in manifest['resources']:
            row['emitted_sha256'] = ex.digest(files[prefix + row['emitted_path']])
        manifest['files'] = {p: ex.digest(files[prefix + p]) for p in manifest['files']}
        manifest['distribution_modification_notice'] = MODIFICATION
        files[path] = ex.encoded(manifest)
    del files['LOCAL-CANDIDATE.md']
    files['INSTALL.md'] = ('''# Consulting Studio skills 0.1.0\n\n
This is the release-specific skills-only package under Apache-2.0 and the
accompanying exact approved S NOTICE. Its historical proposal wording is superseded
by the explicit owner adoption recorded in distribution.json. Attribution and all
legal wording are retained verbatim. No individual response deadline is promised.

The package contains 27 business methods, 35 modes and three separate entries:
Setup, Workspace Librarian and provider-neutral Resume. Read each selected root
instruction and its required child resources through the actual available reader.
It supplies no GUI, MCP server, execution engine, credentials or customer bindings.

Verify the exact ZIP checksum and public name/version before separately authorized
installation. Use only the supported format and controls actually exposed by the
chosen host. Missing eligibility or import support is a bounded blocker. Repository
publication, marketplace distribution, installation, enablement, complete resource
reading, actual execution and human acceptance are separate events.

Preserve the prior approved package, configuration, adaptations, notes and issued
work before explicit update adoption. Observe changed bytes in a fresh session.
Recovery needs a supported exact prior-version restoration and readback; it does
not reverse issued outputs or external effects. Native install/update/recovery and
owner acceptance remain NOT_RUN. No automatic updates or cross-host compatibility
are claimed. Historical exporter evidence under provenance is not operative policy.
''').encode()
    files['provenance/exporter-distribution.json'] = upstream['distribution.json']
    files['MODIFICATIONS.md'] = ('# S packaging modifications, 2026-10-27\n\n' + MODIFICATION + '\n\n'
        'The upstream distribution is retained under provenance as historical input evidence.\n'
        'The current distribution manifest records the exact notice overlay and current bytes.\n'
        'Canonical input bytes, method contents/versions and historical grants are unchanged.\n'
        'Operative legal copies apply the exact approved Apache text and S NOTICE; public package metadata is consulting-studio-skills 0.1.0.\n'
        'The NOTICE proposal-status wording is historical and superseded by the recorded owner adoption; its bytes are retained exactly.\n').encode()
    changes = [dict(path=p, upstream_sha256=ex.digest(upstream[p]), sha256=ex.digest(data),
                    reason='Approved release legal/identity application or prominent packaging notice; method meaning retained')
               for p, data in sorted(files.items()) if p in upstream and data != upstream[p]]
    current_mapping = []
    for row in original['canonical_to_emitted']:
        path = row['output_path']
        current = dict(row, emitted_sha256=ex.digest(files[path]),
                       upstream_emitted_sha256=ex.digest(upstream[path]))
        if files[path] != upstream[path]:
            current['release_adaptations'] = ['exact approved release legal copy' if Path(path).name in
                ('LICENSE', 'NOTICE') else 'prominent per-file modification notice; method contents retained']
            if Path(path).name in ('LICENSE', 'NOTICE'):
                current['transformations'] = ['exact approved release legal copy; canonical bytes retained as rebuild evidence']
        current_mapping.append(current)
    delivery_gates = copy.deepcopy(original['delivery_gates'])
    for gate in delivery_gates:
        if gate['id'] in ('s-license', 'export-authority'):
            gate.update(status='APPROVED_RELEASE_SPECIFIC', evidence='Exact owner approval recorded in this distribution',
                        condition='Only the approved finite S release; public effects remain parent-coordinated after final checks and timing gate')
    info = dict(schema='consulting-studio/s-repository-plugin@1', standing=STANDING,
        upstream_distribution=dict(path='provenance/exporter-distribution.json', sha256=ex.digest(upstream['distribution.json']),
            meaning='Complete versioned canonical-to-emitted source mapping before the explicit notice overlay'),
        name=PUBLIC_NAME, version=VERSION, approval=approval(), publication_authority=publication_authority(),
        release_generator=dict(path=SELF, sha256=ex.digest(ex.regular_read(HERE / 'prepare.py'))),
        changes=changes, removed_files=['LOCAL-CANDIDATE.md'],
        generated_files=[p for p in files if p not in upstream] + ['distribution.json'],
        canonical_to_emitted=current_mapping,
        source_commit=original['source_commit'], source_tree=original['source_tree'],
        inventory_sha256=original['inventory_sha256'], business_skills=27, modes=35,
        auxiliary_skills=list(ex.AUXILIARY_SKILLS),
        gates=original['gates'], delivery_gates=delivery_gates,
        license='Apache-2.0', legal=dict(license_sha256=ex.digest(apache), notice_sha256=ex.digest(notice),
            notice_status='Exact approved notice bytes retained; historical proposal framing superseded by explicit owner adoption'),
        files={p: dict(sha256=ex.digest(data), bytes=len(data)) for p, data in sorted(files.items())})
    files['distribution.json'] = ex.encoded(info)
    ex.full_links(files)
    ex.methods.check_runtime_instructions(files)
    ex.pack.manifest_checks(files, [row['name'] for row in original['methods']], ex.decode(files['plugin.json'])['version'], auxiliary=ex.AUXILIARY_SKILLS)
    ex.scan_runtime(files)
    return files, info


def candidate(ex, selected, canonical, tools):
    # The existing exporter and inventory remain the sole method/source selector.
    artifacts = ex.artifacts(selected, canonical, tools)
    # artifacts() has already validated this freshly generated archive. Do not
    # repeat the expensive method/source assembly to retrieve its exact files.
    with zipfile.ZipFile(io.BytesIO(artifacts[ex.CANDIDATE])) as archive:
        upstream = {name: archive.read(name) for name in archive.namelist()}
    plugin, plugin_info = plugin_candidate(ex, upstream, canonical)
    inputs = ex.input_files(selected, canonical, tools)
    ex.require(len(inputs) == 101, 'Expected complete 101-file standalone rebuild')
    authored = {SELF: HERE.joinpath('prepare.py').read_bytes()}
    authored.update({'implementation/s-distribution/' + name: HERE.joinpath(name).read_bytes() for name in DOCUMENTS})
    files = {'plugin/' + path: data for path, data in plugin.items()}
    files.update({'rebuild/' + path: data for path, data in inputs.items()})
    files.update(authored)
    files.update({name: authored['implementation/s-distribution/' + name] for name in DOCUMENTS})
    evidence, approved_scope, approved_delta = approved_evidence(ex)
    apache, notice = legal_material(ex, canonical)
    files['LICENSE'], files['NOTICE'] = apache, notice
    files['implementation/s-distribution/NOTICE-S.proposed.txt'] = notice
    files['legal/LICENSE-Apache-2.0.txt'], files['legal/NOTICE-S.txt'] = apache, notice
    files['legal/history/NOTICE-S.proposed.txt'] = notice
    for name, data in evidence.items():
        files['implementation/s-distribution/' + name] = data
        files['legal/history/' + name] = data
    files['legal/README.md'] = b"""# Exact release-specific S grant


The owner approved the exact expanded 31-source S scope and two separately
identified open App adapter instruction sources on 2026-10-27 at 14:59:59 UTC.
The full approved Apache text and S NOTICE are operative. The exact NOTICE bytes
retain historical proposal-status wording; explicit owner adoption in scope.json
supersedes that status wording without changing attribution or legal text.
Historical proposal scope/delta/notice bytes are preserved under history.
Canonical rebuild LICENSE/NOTICE retain their original evidence meaning.
This grant does not license excluded M software or authorize marketplace/host work.
"""
    approved_canonical = {r['path']: r['sha256'] for r in approved_scope['canonical_components']}
    approved_tools = {r['path']: r['sha256'] for r in approved_scope['rebuild_tools']}
    ex.require(approved_canonical == {p: ex.digest(data) for p, data in canonical.items()},
               'Canonical inputs differ from exact approved scope')
    ex.require(approved_tools == {p: ex.digest(data) for p, data in tools.items()},
               'Rebuild inputs differ from exact approved scope')
    current_authored = {p: ex.digest(data) for p, data in authored.items()}
    current_authored['implementation/s-distribution/NOTICE-S.proposed.txt'] = ex.digest(notice)
    ex.require(set(current_authored) == {r['path'] for r in approved_scope['new_repository_components']},
               'New authored component outside approved scope')
    current_sources = {r['path']: r['sha256'] for r in approved_scope['canonical_components']
                       if r['grant_scope'] == 'new identified first-party Apache grant proposed'}
    current_sources.update(approved_tools)
    current_sources.update(current_authored)
    ex.require(set(current_sources) == {r['path'] for r in approved_delta['s_components']}
               and len(current_sources) == 31, 'Release source scope expansion')
    delta = copy.deepcopy(approved_delta)
    delta.update(status='APPROVED_RELEASE_SPECIFIC', owner_approval=approval(),
        publication_authority=publication_authority(),
        standing='Exact expanded scope approved; only release legal/identity/approval metadata and consequent hashes are applied')
    delta['s_components'] = [dict(row, new_sha256=current_sources[row['path']],
        approved_source_sha256=row['new_sha256'],
        approved_change=row['change'],
        change='added' if row['old_sha256'] is None else 'unchanged'
               if row['old_sha256'] == current_sources[row['path']] else 'changed',
        release_application='legal/identity/release-metadata-only' if current_sources[row['path']] != row['new_sha256'] else 'exact approved bytes')
        for row in approved_delta['s_components']]
    delta['proposed_normalized_source_map_sha256'] = ex.digest(ex.encoded(current_sources))
    files['legal/source-delta.json'] = ex.encoded(delta)
    scope = copy.deepcopy(approved_scope)
    scope.update(status='APPROVED_RELEASE_SPECIFIC', license='Apache-2.0', approval=approval(),
        publication_authority=publication_authority(),
        prior_29_source_approval='Superseded by explicit approval of the expanded exact 31 S sources plus two separate App adapter instructions',
        new_repository_components=[dict(path=p, sha256=sha) for p, sha in sorted(current_authored.items())],
        source_delta=dict(path='legal/source-delta.json', sha256=ex.digest(files['legal/source-delta.json'])),
        approved_evidence={name: dict(path='legal/history/' + name, sha256=ex.digest(data))
                           for name, data in evidence.items()},
        release_identity=dict(name=PUBLIC_NAME, version=VERSION, repository='cogni-work/' + PUBLIC_NAME),
        release_legal=dict(license_sha256=ex.digest(apache), notice_sha256=ex.digest(notice),
            notice_status='Owner adoption supersedes historical proposal framing; exact approved bytes retained'),
        evidence_only_paths=['rebuild/canonical/LICENSE', 'rebuild/canonical/NOTICE', 'legal/history/'],
        separate_open_adapter_disposition='The two exact instruction hashes are approved Apache-2.0; '
             'they are not S payload inputs. No App/GUI/MCP/server software is shipped or granted by this S release.')
    for row in scope['canonical_components']:
        if row['grant_scope'] == 'new identified first-party Apache grant proposed':
            row['grant_scope'] = 'new identified first-party Apache grant approved'
    scope['delta']['helper_adapter'] = 'Two exact separately identified App adapter instruction sources approved Apache-2.0; no M software grant'
    files['legal/scope.json'] = ex.encoded(scope)
    ex.check_paths(files)
    info = dict(schema='consulting-studio/s-repository-candidate@1', standing=STANDING,
        candidate_version=VERSION, repository_name='cogni-work/' + PUBLIC_NAME,
        public_identity=dict(name=PUBLIC_NAME, version=VERSION, license='Apache-2.0', status='APPROVED_RELEASE_SPECIFIC'),
        approval=approval(), publication_authority=publication_authority(),
        license_scope=dict(path='legal/scope.json', sha256=ex.digest(files['legal/scope.json'])),
        canonical_commit=selected['source_commit'], canonical_tree=selected['source_tree'],
        inventory_commit=ex.INVENTORY_COMMIT, inventory_sha256=ex.INVENTORY_SHA256,
        counts=dict(canonical_inputs=93, rebuild_inputs=101, plugin_files=len(plugin),
                    business_skills=27, auxiliary_skills=3,
                    method_mappings=len(ex.decode(upstream['distribution.json'])['canonical_to_emitted']),
                    notice_overlay_files=len(plugin_info['changes'])),
        exporter_artifacts={p: dict(sha256=ex.digest(data), bytes=len(data)) for p, data in artifacts.items()},
        gates=dict(new_s_grant='APPROVED_RELEASE_SPECIFIC', publication='NOT_EXECUTED_PARENT_COORDINATED',
                   fresh_independent_install='NOT_RUN', native_update='NOT_RUN', native_recovery='NOT_RUN',
                   independent_final_review='RECORDED_SEPARATELY', owner_acceptance='NOT_RUN'),
        files={p: dict(sha256=ex.digest(data), bytes=len(data)) for p, data in sorted(files.items())})
    files['repository.json'] = ex.encoded(info)
    ex.full_links({p: data for p, data in files.items() if not p.startswith('rebuild/')})
    repo_zip, plugin_zip = ex.pack.zip_bytes(files), ex.pack.zip_bytes(plugin)
    ex.require(ex.pack.unpack(repo_zip, files) == files, 'Repository ZIP fidelity')
    ex.require(ex.pack.unpack(plugin_zip, plugin) == plugin, 'Plugin ZIP fidelity')
    outputs = {REPO_ZIP: repo_zip, PLUGIN_ZIP: plugin_zip, 'repository.json': files['repository.json']}
    outputs.update({'exporter-artifacts/' + p: data for p, data in artifacts.items()})
    outputs['SHA256SUMS'] = ''.join(ex.digest(outputs[p]) + '  ' + p + '\n'
        for p in sorted((REPO_ZIP, PLUGIN_ZIP, 'repository.json'))).encode()
    outputs['BUILD-SHA256SUMS'] = ''.join(ex.digest(data) + '  ' + p + '\n'
        for p, data in sorted(outputs.items())).encode()
    return files, outputs


def write_tree(ex, root, files):
    root = Path(root).absolute()
    if root.exists():
        ex.require(ex.read_exact_tree(root, files) == files, 'Conflicting prior output; inspect before retry')
        return
    ex.require(not any(p.is_symlink() for p in (root, *root.parents)), 'Output/ancestor symlink')
    root.mkdir(parents=True)
    for path, data in files.items():
        target = root / ex.safe_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rebuild-from', type=Path, help='Exact extracted101-input snapshot; no Git/network')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output', type=Path)
    mode.add_argument('--check', type=Path)
    mode.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    ex = exporter(args.rebuild_from)
    selected, canonical = ex.read_rebuild(args.rebuild_from) if args.rebuild_from else ex.audit_checkout()
    files, outputs = candidate(ex, selected, canonical, ex.tool_inputs())
    complete = {'repo/' + p: data for p, data in files.items()} | outputs
    if args.output:
        write_tree(ex, args.output, complete)
    if args.check:
        ex.require(ex.read_exact_tree(args.check, complete) == complete, 'Complete repository candidate differs')
    print(json.dumps(dict(standing=STANDING, repo_zip_sha256=ex.digest(outputs[REPO_ZIP]),
        plugin_zip_sha256=ex.digest(outputs[PLUGIN_ZIP]), repository_sha256=ex.digest(outputs['repository.json']),
        canonical_inputs=93, rebuild_inputs=101, publication='BLOCKED'), sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, IndexError) as error:
        sys.exit('FAIL: ' + str(error))
