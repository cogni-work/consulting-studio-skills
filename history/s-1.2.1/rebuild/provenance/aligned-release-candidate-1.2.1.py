#!/usr/bin/env python3
"""Prepare local aligned Skills/App candidates; never publish or install.

The frozen exporter and historical release approval remain unchanged. This new
revision consumes a separately pinned, S-only current-source selection. Prior grants/legal bytes remain evidence. The current proposed legal overlay
keeps exact source/license/export approval pending and performs no external write.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SELF = 'implementation/aligned-release/prepare.py'
SELECTION = 'implementation/aligned-release/selection.json'
SOURCE = '02441d561100b22144889ae448bc02e6b25a37a6'
TREE = 'e1aa02f6ac3dc38a4cd76c10efdfad0026a61f21'
SKILLS_VERSION = '1.2.1'
APP_VERSION = '1.1.1'
PRIOR_APP_ADAPTER_SOURCE = 'e8eac2aff9f1ac84355b947a4717fcbb4a532587'
PRIOR_APP_ADAPTER_HASHES = {
    'skills/studio-resume/SKILL.md': '9de9db8d9ecfbd28e310b1d7865a0f6da1c619a90298120d9aea37c56c7e680c',
    'skills/studio-resume/references/runtime-contract.md': 'bd12d1788e51553aebea8584a6a02a58324221d4223a17bc30bc4a5e7b7176bc',
}
APP_ADAPTER_SOURCE = 'd85cc4b2183430383ebba1ca3ab0baf077d2ae26'
APP_ADAPTER_TREE = 'c49f2483b2b7fad4715a2fdcee3d5ab6657c864b'
APP_ADAPTER_PREFIX = 'implementation/embedded-ui/skills/studio-resume/'
RESUME_CORE = 'implementation/skills/studio-resume/references/resume-contract.md'
APP_ADAPTER_HASHES = {
    APP_ADAPTER_PREFIX + 'SKILL.md': '9baad71fe6f54db3b5b160b10815ee9e4888549d4db28922282472cb526c79c2',
    APP_ADAPTER_PREFIX + 'references/runtime-contract.md': '38910803843194f161eb01d8cfd2334b911b85ee0303e85adaaf577b3d45b42a',
    RESUME_CORE: 'cf67f9aa8abcf1cb59777377107a2d2bad7ac5869e6631a604511d99d2f03b26',
}
NAME = 'consulting-studio-skills'
STANDING = 'LOCAL PROPOSED CANDIDATE; exact release/export approval PENDING; installation and acceptance NOT_RUN'
MODIFICATION = ('Consulting Studio packaging modification, 2026-10-28: local resource locators '
                'and explicit governing reads; canonical source and emitted hashes in distribution.json. '
                'Existing license rights retained; current exact release approval pending.')
# Dependencies are verified before importing their code. The new script is the
# review trust root; selection and dependencies are finite, hash-bound inputs.
DEPENDENCIES = {
    'implementation/s-export/export.py': '1649a8783ff4190a80a0fc04bf1e8e9098cdca9a07dc78058c5180189d413116',
    'implementation/business-skills/release.py': '25b27ef1416b17164daaa2366f906b7ffdd818eb3631d37678f1442c7ec04e89',
    'implementation/business-skills/check_packages.py': '34e029ad1cc6f2ae4efc7dcc940517d7b37fd8a931b7bc7d9de62eacc84818f6',
    'implementation/plugin-distribution/release.py': 'd6b57e160bc386df4519d1cfcca6756fa3d0354d2ba876016466c913688c798a',
    'implementation/plugin-setup/package_update.py': '0e3c80d778e4c67508ca379badb3ca92f5703512830360c093fb08cc91976fd9',
    'implementation/plugin-distribution/plugin.json': '4a6d7c007663232cbb2ff7f63a3d1b200abd229afb9ed77873768c2d4004affb',
}
SELECTION_SHA256 = '804ab14e5d72bf435c42bcab4e15d8490eeadb56c2f54c4d883c74be213aeb65'
PUBLIC_BASE = 'fff65b7e5debd215f52bc9228d07bdee535dd762'
PUBLIC_BASE_FILES = {'AUDIT.md': '8068f5a52f0aa05c4ed13463b64d3d88a6add8bf6e5d396e7c26f1a3f1389f70', 'CHANGELOG.md': 'a381c40adb949ee1f91f07b523d74ad140a4cffc922a842522c8958f04587be0', 'INSTALL-TEST-PLAN.md': '30985cabb9bc3f35dd5067aee087cdf6185ba185b3ef6cb4de1a9ac1b7d1dea6', 'KNOWN-LIMITS.md': '75c949b25c8b320f0222e3a124a69c464da5f82d10e3c44e5490427d12036bb5', 'OWNER-DECISIONS.md': '5f56f839040524e5c13a9983521ed934165569052414bcd1ce1ce59267e2432e', 'README.md': '32649a03da36646f2af9cb5f1ee00a3bc0f772b1efedf91f913d1c87d0fa1c91', 'SECURITY.md': '80d76089775f21a4c1ac1950be5c96df8512e641862f46a828d514d4ee2b38f4', 'SUPPORT.md': '98ccd11f5469a2b1ddd167fa85dbf0a1c74050c3af9978c92f9edf5bfa045d79', 'implementation/s-distribution/AUDIT.md': '0f9fc1a7275d3840d8741c8ed09080eb2f40f47eaaa7037669d415654675735d', 'implementation/s-distribution/CHANGELOG.md': 'db94407aec2a6b26a22dfa59c67171c18852c4da8182661f3e18f05aad6c572c', 'implementation/s-distribution/INSTALL-TEST-PLAN.md': '30985cabb9bc3f35dd5067aee087cdf6185ba185b3ef6cb4de1a9ac1b7d1dea6', 'implementation/s-distribution/KNOWN-LIMITS.md': '75c949b25c8b320f0222e3a124a69c464da5f82d10e3c44e5490427d12036bb5', 'implementation/s-distribution/NOTICE-S.proposed.txt': '4235c333ef37e7c6d8a352cda1ab9cd0880d4b5d21ba13892b32a81ee0ac94df', 'implementation/s-distribution/OWNER-DECISIONS.md': '5f56f839040524e5c13a9983521ed934165569052414bcd1ce1ce59267e2432e', 'implementation/s-distribution/README.md': 'bd546b38c5c0d27f644e9169632eaab7812b703471a56f2a18df7255de661e8e', 'implementation/s-distribution/SECURITY.md': '80d76089775f21a4c1ac1950be5c96df8512e641862f46a828d514d4ee2b38f4', 'implementation/s-distribution/SUPPORT.md': '98ccd11f5469a2b1ddd167fa85dbf0a1c74050c3af9978c92f9edf5bfa045d79', 'implementation/s-distribution/approved-scope.json': '6248cbe9957b91b65e10413abb934b3ac33111f1e542fdd6419732ac6693f4b0', 'implementation/s-distribution/approved-source-delta.json': '19b525f388c8fd3f14d4fbb245cadc549cc7ae022c9729c0e49cb49cf25be2b4', 'implementation/s-distribution/prepare.py': '4939cf2a5c0e4fd76b6bd8fba9484c601532f646381d816402bc867101dea628', 'legal/history/NOTICE-S.proposed.txt': '4235c333ef37e7c6d8a352cda1ab9cd0880d4b5d21ba13892b32a81ee0ac94df', 'legal/history/approved-scope.json': '6248cbe9957b91b65e10413abb934b3ac33111f1e542fdd6419732ac6693f4b0', 'legal/history/approved-source-delta.json': '19b525f388c8fd3f14d4fbb245cadc549cc7ae022c9729c0e49cb49cf25be2b4', 'legal/scope.json': '42c230c83766a9f108bc310d0d6ee97e49e9a8e86cf2e6aacca151e6c0a91bd1', 'legal/source-delta.json': '698a80b3abdc5aac38004ca3e88843d3b7c288400ea6873c3be654ac38a0770b'}
PUBLIC_BASE_ALL_SHA256 = '301b0f794efd76236aa65c53aa6d9f5cad7e96cc7e1b7d8179b0851d6f1f2d82'
PUBLIC_NOTICE = b'PROPOSED S NOTICE ONLY \xe2\x80\x94 not adopted; inherited operative NOTICE is unchanged.\n\nConsulting Studio\nCopyright 2026 cogni-work contributors\n\nProduct vision and business architecture are selectively adapted from\ncogni-work/cogni-consulting, commit\n651a17604ab3cb456010b804b334e9c504a3fad9, Apache-2.0.\n\n    cogni-consulting\n    Copyright 2026 Stephan de Haas / cogni-work.ai\n\nProblem-structuring/framework-selection and communication-craft vocabulary derives\nthrough prior method references from insight-wave, commit\nfbce470260b9244b3a687bf1177a593f5f6600e3, including cogni-publishing 0.0.35,\nApache-2.0.\n\n    insight-wave\n    Copyright 2026 Stephan de Haas / cogni-work.ai\n\nTheme-selection/application concepts are informed by Anthropic theme-factory,\ncommit 683bc88e56f3e09ba94f7055977f3d3aa499f202, Apache-2.0.\n\n    Copyright 2026 Anthropic, PBC.\n\nDoc-coauthoring is credited as a conceptual workflow reference at that revision.\nBruce Mau\'s MC24, "Quantify and Visualize," is credited as owner-supplied inspiration.\nNo book pages/images, theme assets, fonts or upstream renderer code are redistributed\nin S. The optional Setup example is labelled fictional; historical rendered\nfixtures/evaluation adapters are excluded.\n\nConsulting Studio modifications, 2026-10-04 and 2026-10-09: independently rewritten\nproduct/business and communication requirements selectively retain the above\nvocabulary, evidence qualifications, human decisions and consulting scope.\n\nConsulting Studio modification, 2026-10-27: S source packaging rewrites required\nresource locators to complete local resources, composes working instructions,\nadds explicit working-instruction reads where applicable and per-file change\nnotices. Canonical source bytes, inherited grants and historical distributions\nremain unchanged. Exact source hashes and transformations accompany the package.\n\nThis proposed notice supplies attribution, not a new grant or approval. Actual\nthird-party rights and existing recipient grants remain preserved. The new\nS-wide first-party Apache proposal requires exact owner adoption separately.\n'
APACHE_SHA256 = 'c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4'
NOTICE_SHA256 = '4235c333ef37e7c6d8a352cda1ab9cd0880d4b5d21ba13892b32a81ee0ac94df'
OPEN_DELTA = tuple(r['path'] for r in json.loads((ROOT / SELECTION).read_bytes())['current_source_delta']) + (SELF, SELECTION)
PUBLIC_STANDING = 'LOCAL PROPOSED S1.2.1 CANDIDATE; current exact scope/license/export approval PENDING; publication, installation and acceptance NOT_RUN'
PUBLIC_MODIFICATION = ('Consulting Studio packaging modification, 2026-10-28: local resource locators '
    'and explicit governing reads; exact canonical and emitted hashes retained. '
    'Prior Apache/NOTICE copies retained; approval of the current delta remains PENDING.')
REBUILD = b'# Finite candidate rebuild inputs\n\nPython3 standard library only; no Git, network, constructor or App required.\n\n    python3 -B implementation/aligned-release/prepare.py --rebuild-from . --public-candidate --output ../s-1.2.1-rebuilt\n\nCompare the four S artifacts and SKILLS-SHA256SUMS. Current scope/license/export\napproval remains PENDING. Prior grants and releases remain unchanged. For the\ncanonical legal-evidence view, omit --public-candidate. No publication, update,\ninstallation, native qualification or customer acceptance follows from a build.\n'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def regular(path):
    path = Path(path).absolute()
    if any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file() or path.stat().st_size > 128 * 1024 * 1024:
        raise ValueError('Nonregular/oversized input: ' + str(path))
    return path.read_bytes()


for _path, _hash in DEPENDENCIES.items():
    if sha(regular(ROOT / _path)) != _hash:
        raise ValueError('Unreviewed packaging dependency: ' + _path)

spec = importlib.util.spec_from_file_location('aligned_frozen_primitives', ROOT / 'implementation/s-export/export.py')
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)
methods, pack, setup = ex.methods, ex.pack, ex.setup
require, encoded, decode = ex.require, ex.encoded, ex.decode


def selection():
    data = regular(ROOT / SELECTION)
    require(sha(data) == SELECTION_SHA256, 'Unreviewed current-source selection')
    result = decode(data)
    require(result['source_commit'] == SOURCE and result['source_tree'] == TREE, 'Source identity drift')
    require(len(result['files']) == 93 and len({r['path'] for r in result['files']}) == 93, 'Finite source inventory drift')
    return result


class Source(methods.RuntimeSource):
    """Finite canonical bytes using the established runtime resolver, without Git."""
    def __init__(self, selected, canonical):
        self.commit, self.tree = SOURCE, TREE
        self.paths = {r['path'] for r in selected['files']}
        require(set(canonical) == self.paths, 'Canonical source allowlist mismatch')
        self.cache = dict(canonical)
        for row in selected['files']:
            data = self.read(row['path'])
            require(sha(data) == row['sha256'] and len(data) == row['bytes'], 'Canonical bytes drift: ' + row['path'])
        self.catalog = decode(self.read('implementation/runtime/method-catalog.json'))
        self.items = {r['name']: r for r in self.catalog['skills']}
        self.methods = {r['name']: r['method_resources'] for r in selected['skills']}
        require(list(self.items) == list(self.methods) and len(self.methods) == 27, 'Catalog drift')
        self.allowed = set(methods.RUNTIME_COMMON + methods.RUNTIME_SUPPORTING)
        self.allowed.update(p for paths in self.methods.values() for p in paths)
        require(len(self.allowed) == 86, 'Business resource closure drift')
        self.allowed.update(p for item in selected['auxiliary_entries'] for p in item['resources'])
        self.business_manifests = {'implementation/skills/' + n + '/SKILL.md': n for n in self.methods}
        self.issues, self.virtual = {}, {}
        for row in selected['skills']:
            paths, edges = methods.closure(self, row['name'])
            require(paths == selected['resource_sets'][row['required_set']] and len(edges) == 474, 'Dependency closure drift')
            require(sha(encoded({p: sha(self.read(p)) for p in paths})) == row['resource_map_sha256'], 'Resource map drift')
        ex.scan_runtime(self.cache)

    def read(self, path):
        require(path in self.cache, 'Unselected canonical read: ' + path)
        return self.cache[path]


def inputs(rebuild=None):
    selected = selection()
    tools = {p: regular(ROOT / p) for p in (*DEPENDENCIES, SELF, SELECTION)}
    if rebuild:
        names = {'canonical/' + r['path'] for r in selected['files']} | set(tools) | {'REBUILD.md'}
        supplied = ex.read_exact_tree(rebuild, names)
        require(all(supplied[p] == data for p, data in tools.items()) and supplied['REBUILD.md'] == REBUILD,
                'Rebuild tooling/guidance drift')
        canonical = {r['path']: supplied['canonical/' + r['path']] for r in selected['files']}
    else:
        require(methods.git('rev-parse', SOURCE + '^{tree}').decode().strip() == TREE, 'Canonical Git tree drift')
        canonical = {r['path']: methods.git('show', SOURCE + ':' + r['path']) for r in selected['files']}
    return selected, canonical, tools


def modification(path, data):
    if path.endswith('.md'):
        text = data.decode()
        end = text.find('\n---\n', 4) + 5 if text.startswith('---\n') else 0
        require(not text.startswith('---\n') or end > 4, 'Unclosed frontmatter')
        return (text[:end] + '\n<!-- ' + MODIFICATION + ' -->\n' + text[end:]).encode()
    require(path.endswith('.json'), 'Unqualified transformed format: ' + path)
    value = decode(data)
    require('distribution_modification_notice' not in value, 'Existing modification key')
    value['distribution_modification_notice'] = MODIFICATION
    return encoded(value)


def build(selected, canonical, tools):
    source = Source(selected, canonical)
    generators = {p: sha(data) for p, data in sorted(tools.items())}
    config = dict(version=SKILLS_VERSION, repository=selected['repository'], standing=STANDING)
    files, mappings, catalog = {}, [], []
    for name in source.methods:
        skill = methods.assemble_runtime(source, name, config, generators)
        manifest = decode(skill['manifest.json'])
        catalog.append(dict(name=name, method_version=manifest['method_version'], modes=manifest['modes']))
        files.update({'skills/' + name + '/' + p: d for p, d in skill.items()})
        mappings.extend(dict(row, output_path='skills/' + name + '/' + row['emitted_path']) for row in manifest['resources'])
    portable = decode(tools['implementation/plugin-distribution/plugin.json'])
    portable.update(name=NAME, version='0.1.3', license='SEE LICENSE AND distribution.json')
    portable['extensions']['com.openai'].pop('onboardingSkill')
    refs = dict(setup.REFERENCE_MAP)
    refs['../../../business-skills/installation-storage-lifecycle.md'] = 'skills/org-specialize/references/source/implementation/runtime/storage-lifecycle.md'
    added, receipt = setup.compose({'plugin.json': encoded(portable), **files}, SKILLS_VERSION,
        setup={p: canonical['implementation/plugin-setup/' + p] for p in setup.SETUP_FILES}, reference_map=refs)
    files.update(added)
    rights = {r['path']: r for r in selected['files']}
    for item in selected['auxiliary_entries']:
        auxiliary, mapped, _ = ex.assemble_auxiliary(source, item, rights, canonical, generators)
        files.update({'skills/' + item['name'] + '/' + p: d for p, d in auxiliary.items()})
        mappings.extend(mapped)
    for path in setup.SETUP_FILES:
        origin = 'implementation/plugin-setup/' + path
        mappings.append(dict(canonical_path=origin, canonical_sha256=sha(canonical[origin]), output_path=path,
                             adaptations=receipt['reference_adaptations'] if path == setup.SETUP_FILES[0] else []))
    for origin, target in [('LICENSE', 'LICENSE'), ('NOTICE', 'NOTICE'),
                           ('implementation/plugin-distribution/runtime-readme.md', 'README.md')]:
        files[target] = canonical[origin]
        mappings.append(dict(canonical_path=origin, canonical_sha256=sha(canonical[origin]), output_path=target, adaptations=[]))
    require({r['canonical_path'] for r in mappings} == set(canonical), 'Incomplete source/output lineage')
    require(len({r['output_path'] for r in mappings}) == len(mappings), 'Output mapping collision')
    for row in mappings:
        path = row['output_path']
        if files[path] != canonical[row['canonical_path']] and Path(path).name not in ('LICENSE', 'NOTICE'):
            files[path] = modification(path, files[path])
        row['emitted_sha256'] = sha(files[path])
    for path in list(files):
        if path.startswith('skills/') and path.endswith('/manifest.json'):
            manifest = decode(files[path]); prefix = path.rsplit('/', 1)[0] + '/'
            manifest['standing'] = STANDING
            manifest['shared_skills_release'] = SKILLS_VERSION
            for row in manifest['resources']:
                row['emitted_sha256'] = sha(files[prefix + row['emitted_path']])
            manifest['files'] = {p: sha(files[prefix + p]) for p in manifest['files']}
            manifest['distribution_modification_notice'] = MODIFICATION
            files[path] = encoded(manifest)
    portable = decode(files['plugin.json'])
    legacy = {k: portable[k] for k in ('name', 'version', 'description', 'author', 'license')}
    legacy.update(interface=portable['extensions']['com.openai']['interface'], skills='./skills',
                  extensions={'com.openai': {'onboardingSkill': setup.ENTRY}})
    files['.codex-plugin/plugin.json'] = encoded(legacy)
    info = dict(schema='consulting-studio/aligned-skills-candidate@1', name=NAME, version=SKILLS_VERSION,
        standing=STANDING, source_commit=SOURCE, source_tree=TREE, selection_sha256=SELECTION_SHA256,
        generator_inputs=generators, business_skills=27, modes=35, auxiliary_skills=list(ex.AUXILIARY_SKILLS),
        methods=catalog, canonical_to_emitted=mappings,
        historical_inventory=selected['historical_inventory'],
        legal=dict(status='CURRENT_EXACT_RELEASE_APPROVAL_PENDING',
            meaning='Canonical LICENSE/NOTICE retained byte-exact, including inherited Apache rights. Historical approval is not approval of this candidate. Public release requires separately reviewed operative legal copies and exact current scope.',
            license_sha256=sha(canonical['LICENSE']), notice_sha256=sha(canonical['NOTICE'])),
        delivery_gates=dict(exact_owner_release_export_approval='PENDING', operative_public_legal_overlay='PENDING'),
        gates={k: 'NOT_RUN' for k in ('independent_package_review', 'publication', 'installation', 'native_execution',
                'S_DIST', 'M_HOST', 'M_DIST', 'update_recovery', 'customer_acceptance')},
        files={p: dict(sha256=sha(d), bytes=len(d)) for p, d in sorted(files.items())})
    files['distribution.json'] = encoded(info)
    ex.full_links(files); methods.check_runtime_instructions(files); ex.scan_runtime(files)
    pack.manifest_checks(files, list(source.methods), SKILLS_VERSION, auxiliary=ex.AUXILIARY_SKILLS)
    return files, info


def app_resume_payload(skills, sources=None):
    """Compose the current App adapter over the exact selected neutral core."""
    if sources is None:
        require(methods.git('rev-parse', APP_ADAPTER_SOURCE + '^{tree}').decode().strip() == APP_ADAPTER_TREE,
                'Current App adapter source tree drift')
        sources = {p: methods.git('show', APP_ADAPTER_SOURCE + ':' + p) for p in APP_ADAPTER_HASHES}
    require(set(sources) == set(APP_ADAPTER_HASHES)
            and all(sha(sources[p]) == h for p, h in APP_ADAPTER_HASHES.items()),
            'Current App adapter source drift')
    core_path = 'skills/studio-resume/references/resume-contract.md'
    shared_rows = [r for r in decode(skills['distribution.json'])['canonical_to_emitted']
                   if r['canonical_path'] == RESUME_CORE]
    require(len(shared_rows) == 1, 'Shared S/App Resume mapping drift')
    shared_path = shared_rows[0]['output_path']
    require(shared_path in skills and skills[shared_path] == sources[RESUME_CORE]
            and shared_rows[0]['emitted_sha256'] == sha(sources[RESUME_CORE]), 'Shared S/App Resume core drift')
    link = b'../../../skills/studio-resume/references/resume-contract.md'
    entry = APP_ADAPTER_PREFIX + 'SKILL.md'
    require(sources[entry].count(link) == 1, 'App Resume shared core locator drift')
    payload, mapping = {}, []
    for origin, data in sorted(sources.items()):
        target = core_path if origin == RESUME_CORE else 'skills/studio-resume/' + origin.removeprefix(APP_ADAPTER_PREFIX)
        emitted = data.replace(link, b'references/resume-contract.md') if origin == entry else data
        payload[target] = emitted
        mapping.append(dict(canonical_path=origin, canonical_sha256=sha(data),
            source_commit=APP_ADAPTER_SOURCE, source_tree=APP_ADAPTER_TREE,
            output_path=target, emitted_sha256=sha(emitted), bytes=len(emitted),
            transformation='Rewrite only shared-core locator' if origin == entry else 'Exact canonical bytes',
            shared_s_output=shared_path if origin == RESUME_CORE else None))
    return payload, mapping


def app_candidate(original, skills, skills_archive):
    """Compose shared methods/current Resume locally; retain exact App settings."""
    require('plugin.json' in original and '.codex-plugin/plugin.json' in original and '.app.json' in original,
            'Expected existing portable App export')
    previous = decode(original['consulting-studio-skills.json'])
    require(set(previous['files']) == set(original) - {'consulting-studio-skills.json'}
            and all(sha(original[p]) == (r['sha256'] if isinstance(r, dict) else r)
                    or p == '.codex-plugin/plugin.json'
                    and sha(original[p]) == '0feae797c0eb13fae811256e1f3650380d04331a6e3b9ca560e1fad2b04c8332'
                    and (r['sha256'] if isinstance(r, dict) else r) == '4f6b3fb5db81c40f37c84490c778596d15c13c189810b8aa054e0f7e6957d033'
                    for p, r in previous['files'].items()),
            'Original App provenance/inventory mismatch')
    portable, legacy = decode(original['plugin.json']), decode(original['.codex-plugin/plugin.json'])
    require(portable['name'] == legacy['name'] and portable['version'] == legacy['version'], 'App identity conflict')
    require(portable['version'] == '1.0.12', 'This candidate requires the reconciled App1.0.12 source profile')
    require(setup.version_tuple(APP_VERSION) > setup.version_tuple(portable['version']), 'App version must increase')
    require(portable['extensions']['com.openai']['apps'] == './.app.json'
            and portable['extensions']['com.openai']['onboardingSkill'] == setup.ENTRY, 'Unexpected App declaration')
    names = {p.split('/')[1] for p in skills if p.startswith('skills/')} - {'studio-resume'}
    common = {p: d for p, d in skills.items() if p.startswith('skills/') and p.split('/')[1] in names}
    old_common = {p for p in original if p.startswith('skills/') and p.split('/')[1] in names}
    require(old_common <= set(common), 'Stale App skill paths need explicit reviewed deletion')
    require({p.split('/')[1] for p in original if p.startswith('skills/')} <= names | {'studio-resume'}, 'Unrecognized App skill/adaptation')
    old_variant = {p: d for p, d in original.items() if p.startswith('skills/studio-resume/')}
    require(set(old_variant) == set(PRIOR_APP_ADAPTER_HASHES)
            and all(sha(old_variant[p]) == h for p, h in PRIOR_APP_ADAPTER_HASHES.items()), 'Prior App adapter source drift')
    resume, resume_mapping = app_resume_payload(skills)
    portable['version'], legacy['version'] = APP_VERSION, APP_VERSION
    overlay = {**common, **resume, 'plugin.json': encoded(portable), '.codex-plugin/plugin.json': encoded(legacy)}
    effective = {**original, **overlay}
    shared_info = decode(skills['distribution.json'])
    app_standing = 'LOCAL APP1.1.1 CANDIDATE WITH S1.2.1 COMMON METHODS AND CURRENT RESUME; exact approval PENDING; live runtime parity, update and host acceptance NOT_RUN'
    provenance = dict(schema='consulting-studio/aligned-app-candidate@1', version=APP_VERSION,
        shared_skills_release=SKILLS_VERSION, shared_skills_archive_sha256=sha(skills_archive),
        shared_skills_variant=shared_info['legal']['status'],
        shared_legal_scope=shared_info['legal'],
        exact_owner_release_export_approval='PENDING',
        app_resume_maintenance_parity='SOURCE_CONTRACT_ALIGNED; LIVE_RUNTIME_NOT_RUN',
        source_commit=SOURCE, source_tree=TREE, standing=app_standing,
        common_skill_files={p: sha(d) for p, d in sorted(common.items())},
        app_resume_variant=dict(version='0.2.1', source_commit=APP_ADAPTER_SOURCE,
            source_tree=APP_ADAPTER_TREE, changed=True,
            mapping=resume_mapping, files={p: sha(d) for p, d in sorted(resume.items())},
            common_core_sha256=sha(resume['skills/studio-resume/references/resume-contract.md']),
            prior=dict(version='0.1.2', source_commit=PRIOR_APP_ADAPTER_SOURCE, files=PRIOR_APP_ADAPTER_HASHES),
            runtime_requirement='Canonical get_studio_resume/open_work_card accept and forward cardId; exact returned project/card/version validation. No deployment or live compatibility inferred.',
            live_parity='NOT_RUN; deployed Site tree unavailable',
            qualification='BLOCKED_FOR_DELIVERY; actual runtime/schema and supported host qualification required under issue228',
            rights='Instruction-source proposal only; exact scope/export adoption PENDING; no GUI/MCP software grant'),
        files={p: sha(d) for p, d in sorted(effective.items()) if p != 'consulting-studio-skills.json'})
    overlay['consulting-studio-skills.json'] = encoded(provenance)
    effective.update(overlay)
    require(effective['.app.json'] == original['.app.json'], 'App binding drift')
    for key in ('plugin.json', '.codex-plugin/plugin.json'):
        before, after = decode(original[key]), decode(effective[key])
        after['version'] = before['version']
        require(before == after, 'Effective App settings drift')
    ex.full_links({p: d for p, d in effective.items() if p.startswith('skills/')})
    receipt = dict(standing=app_standing, old_version=decode(original['plugin.json'])['version'], version=APP_VERSION,
        name=portable['name'], source_commit=SOURCE, shared_skills_release=SKILLS_VERSION,
        shared_skills_archive_sha256=sha(skills_archive), common_skill_files=len(common),
        plugin_id=None, expected_release_id=None, visibility='PRESERVE_EXISTING; fresh backend readback PENDING',
        update='BLOCKED_PENDING_FRESH_PLUGIN_ID_RELEASE_GUARD_USER_PRIVATE_READBACK', deletion_paths=[],
        prior_provenance_serialization_exception=dict(path='.codex-plugin/plugin.json',
            applies_only_when_exact_hash_pair_matches=True,
            actual_sha256=sha(original['.codex-plugin/plugin.json']),
            provenance_sha256=previous['files']['.codex-plugin/plugin.json']),
        original_sha256={p: sha(d) for p, d in sorted(original.items())},
        retained_sha256={p: sha(d) for p, d in sorted(original.items()) if p not in overlay},
        overlay_sha256={p: sha(d) for p, d in sorted(overlay.items())},
        app_resume_mapping=resume_mapping,
        scope='Local partial-update candidate including current Resume instruction adapter; existing App binding/interface/audience retained; no runtime deployment or live compatibility claim')
    return overlay, effective, receipt


def artifacts(selected, canonical, tools):
    files, info = build(selected, canonical, tools)
    archive = pack.zip_bytes(files)
    require(pack.unpack(archive, files) == files, 'S archive fidelity')
    rebuild = {**{'canonical/' + p: d for p, d in canonical.items()}, **tools, 'REBUILD.md': REBUILD}
    outputs = {NAME + '-' + SKILLS_VERSION + '-local-plugin.zip': archive,
            NAME + '-' + SKILLS_VERSION + '-local-rebuild.zip': pack.zip_bytes(rebuild),
            'distribution.json': encoded(info), 'selection.json': encoded(selected)}
    outputs['SKILLS-SHA256SUMS'] = checksums(outputs)
    return outputs


def checksums(outputs):
    return ''.join(sha(d) + '  ' + p + '\n' for p, d in sorted(outputs.items())).encode()


def scope_request(selected, canonical, tools):
    changed = [dict(row, change='changed canonical runtime input')
               for row in selected['current_source_delta']]
    changed.extend(dict(path=p, sha256=sha(tools[p]), change='changed packaging input')
                   for p in (SELF, SELECTION))
    return dict(status='PENDING_CURRENT_EXACT_SCOPE', proposed_versions=dict(S=SKILLS_VERSION, App=APP_VERSION),
        previous_release=selected['previous_release'], components=changed,
        proposed_decision='Approve the exact listed revisions and their generated transformations under Apache-2.0 for S; separately authorize delivery of the reviewed S/App bytes',
        excluded='GUI/MCP/server/App code, private identities/history, customer data, rights changes, installation, runtime qualification and acceptance',
        existing_grants='Preserved; this candidate grants no new rights and withdraws none',
        installation_and_acceptance='NOT_RUN; issue228 remains open')


def public_plugin(selected, canonical, tools):
    """Prepare a reviewable legal-overlay proposal; never claim owner approval."""
    files, info = build(selected, canonical, tools)
    files.pop('distribution.json')
    technical = dict(files)
    apache = canonical['LICENSE'].split(b'PART B: APACHE LICENSE, VERSION 2.0\n\n', 1)[1]
    require(sha(apache) == APACHE_SHA256 and sha(PUBLIC_NOTICE) == NOTICE_SHA256, 'Prior legal payload drift')
    scope = scope_request(selected, canonical, tools)
    legal = dict(status='PENDING_CURRENT_EXACT_SCOPE', proposed_license='Apache-2.0',
        license_sha256=APACHE_SHA256, notice_sha256=NOTICE_SHA256,
        meaning='Prior Apache/NOTICE text retained as existing-grant evidence. Current changed inputs and generated transformations await exact owner approval; this local candidate activates no new grant.',
        approval_request=scope)
    for path, before in list(files.items()):
        if Path(path).name == 'LICENSE':
            files[path] = apache
        elif Path(path).name == 'NOTICE':
            files[path] = PUBLIC_NOTICE
        else:
            files[path] = before.replace(MODIFICATION.encode(), PUBLIC_MODIFICATION.encode())
    for path in ('plugin.json', '.codex-plugin/plugin.json'):
        manifest = decode(files[path]); manifest['license'] = 'SEE LICENSE AND legal/scope.json; current delta approval PENDING'
        files[path] = encoded(manifest)
    files['legal/scope.json'] = encoded(legal)
    for path in list(files):
        if path.startswith('skills/') and path.endswith('/manifest.json'):
            manifest = decode(files[path]); prefix = path.rsplit('/', 1)[0] + '/'
            manifest['standing'] = PUBLIC_STANDING
            manifest['release_identity'] = dict(name=NAME, version=SKILLS_VERSION,
                license='Prior Apache grants preserved; current delta approval PENDING')
            manifest['current_exact_scope_approval'] = 'PENDING'
            for row in manifest['resources']:
                row['emitted_sha256'] = sha(files[prefix + row['emitted_path']])
            manifest['files'] = {p: sha(files[prefix + p]) for p in manifest['files']}
            files[path] = encoded(manifest)
    for row in info['canonical_to_emitted']:
        path = row['output_path']
        row['technical_emitted_sha256'] = row['emitted_sha256']
        row['emitted_sha256'] = sha(files[path])
        if Path(path).name in ('LICENSE', 'NOTICE'):
            row['release_adaptations'] = ['Prior operative legal text retained; current delta grant PENDING; exact canonical input retained in rebuild evidence']
    info.update(schema='consulting-studio/proposed-s-candidate@1', standing=PUBLIC_STANDING,
        approval_request=scope, legal=legal,
        delivery_gates=dict(exact_owner_release_export_approval='PENDING', operative_public_legal_overlay='PROPOSED_ONLY'),
        release_adaptations=[dict(path=p, previous_sha256=sha(technical[p]), sha256=sha(d),
            reason='Proposed legal/manifest/notice copy; no new approval or grant')
            for p, d in sorted(files.items()) if p in technical and d != technical[p]],
        files={p: dict(sha256=sha(d), bytes=len(d)) for p, d in sorted(files.items())})
    files['distribution.json'] = encoded(info)
    ex.full_links(files); methods.check_runtime_instructions(files); ex.scan_runtime(files)
    pack.manifest_checks(files, [r['name'] for r in selected['skills']], SKILLS_VERSION, auxiliary=ex.AUXILIARY_SKILLS)
    return files, info


def public_artifacts(selected, canonical, tools, base=None):
    """Build proposed S bytes and a preserved public-tree proposal locally."""
    plugin, info = public_plugin(selected, canonical, tools)
    rebuild = {**{'canonical/' + p: d for p, d in canonical.items()}, **tools, 'REBUILD.md': REBUILD}
    outputs = {NAME + '-' + SKILLS_VERSION + '-plugin.zip': pack.zip_bytes(plugin),
        NAME + '-' + SKILLS_VERSION + '-rebuild.zip': pack.zip_bytes(rebuild),
        'distribution.json': encoded(info), 'selection.json': encoded(selected)}
    outputs['SKILLS-SHA256SUMS'] = checksums(outputs)
    if base is None:
        return outputs
    base = Path(base)
    names = {p.relative_to(base).as_posix() for p in base.rglob('*')
             if '.git' not in p.relative_to(base).parts and not p.is_dir()}
    previous = ex.read_exact_tree(base, names)
    require(sha(encoded({p: sha(d) for p, d in sorted(previous.items())})) == PUBLIC_BASE_ALL_SHA256,
            'Public base changed; reconcile remote owner edits before preparing another tree')
    require(all(sha(previous[p]) == h for p, h in PUBLIC_BASE_FILES.items()), 'Public retained source drift')
    old_owned = {p for p in previous if p.startswith(('plugin/', 'rebuild/'))}
    current_owned = {'plugin/' + p for p in plugin} | {'rebuild/' + p for p in rebuild}
    require(old_owned <= current_owned, 'Stale public paths require separately reviewed removal')
    repo = dict(previous)
    repo['legal/history/s-1.1.0-scope.json'] = previous['legal/scope.json']
    repo['legal/history/s-1.1.0-source-delta.json'] = previous['legal/source-delta.json']
    # Preserve all owner prose; only exact current release links are proposed.
    repo['README.md'] = previous['README.md'].replace(b'/v1.1.0/', b'/v1.2.1/').replace(
        b'/tag/v1.1.0', b'/tag/v1.2.1').replace(b'1.1.0-plugin.zip', b'1.2.1-plugin.zip').replace(
        b'Download the 1.1.0 plugin ZIP', b'Download the 1.2.1 plugin ZIP')
    repo['AUDIT.md'] = ('''# Local proposed S1.2.1 candidate, 2026-10-28

Current exact scope/license/export approval is PENDING. This tree is a local review
candidate; no public release or host operation has occurred. It incorporates
issue232/PR233 from the exact source in legal/scope.json: Setup0.1.8,
Librarian0.2.2, neutral/shared Resume0.2.1 and11 updated business methods.
All27 methods/35 modes remain. The93 canonical inputs include29 changed revisions
and64 unchanged inputs. The complete31-input delta includes the updated generator
and selection; no GUI/MCP/server source or private App input is included.
Prior grants, attribution and releases remain unchanged. Historical1.1.0 approval
is retained under legal/history, separately from the current pending scope.

Rebuild the proposed plugin with Python3 standard library only:

    python3 -B rebuild/implementation/aligned-release/prepare.py --rebuild-from rebuild --public-candidate --output ../s-1.2.1-rebuilt

Compare its four S artifacts with SKILLS-SHA256SUMS. Rebuilding the repository
asset additionally requires the exact prior public tree. Source/package checks
establish no native execution, fresh-chat continuity, installation, recovery or
customer acceptance. Those observations remain NOT_RUN under issue228.

---

''').encode() + previous['AUDIT.md']
    repo['CHANGELOG.md'] = ('''# Proposed1.2.1 - 2026-10-28

- Apply existing project structure and maintain references to originals.
- Research retains sources/candidates separately from accepted synthesis.
- Neutral Resume reads fresh accepted work and uncertain maintenance state.
- Same27 methods/35 modes; Setup0.1.8, Librarian0.2.2, Resume0.2.1.
- Exact current source/license/export approval PENDING; no publication or host PASS.

''').encode() + previous['CHANGELOG.md']
    repo['legal/README.md'] = ('''# Current candidate scope

This local S1.2.1 candidate has no current owner release/export or new-license
approval. scope.json and source-delta.json identify the exact proposed inputs.
LICENSE and NOTICE retain the same bytes already distributed with1.1.0. Existing
recipient grants remain in force. Their presence grants no new rights over the
current changed inputs. Canonical mixed legal inputs in rebuild are evidence only.
The exact prior1.1.0 scope/delta and earlier approval history remain byte-exact under
history. No App/GUI/MCP/server code, private identity or customer content is included.
''').encode()
    repo.update({'plugin/' + p: d for p, d in plugin.items()})
    repo.update({'rebuild/' + p: d for p, d in rebuild.items()})
    repo['SKILLS-SHA256SUMS'] = outputs['SKILLS-SHA256SUMS']
    request = scope_request(selected, canonical, tools)
    repo['legal/source-delta.json'] = encoded(dict(schema='consulting-studio/proposed-s-source-delta@1',
        approval_request=request, components=request['components'], previous_public_base=PUBLIC_BASE,
        canonical_inputs=93, changed_runtime_inputs=29, unchanged_runtime_inputs=64,
        generated_outputs='Exact source transformations, dependency graphs, method manifests, prominent notices, legal proposal and repository/rebuild metadata; no additional selected canonical component'))
    repo['legal/scope.json'] = encoded(dict(schema='consulting-studio/proposed-s-scope@1',
        approval_request=request, name=NAME, version=SKILLS_VERSION, proposed_license='Apache-2.0',
        source_commit=SOURCE, source_tree=TREE, selection_sha256=SELECTION_SHA256,
        canonical_components=[dict(path=p, sha256=sha(d)) for p, d in sorted(canonical.items())],
        rebuild_tools=[dict(path=p, sha256=sha(d)) for p, d in sorted(tools.items())],
        source_delta=dict(path='legal/source-delta.json', sha256=sha(repo['legal/source-delta.json'])),
        legal=info['legal'], existing_grants='Preserved; no current delta license activation',
        history={p: sha(d) for p, d in sorted(repo.items()) if p.startswith('legal/history/')}))
    manifest = dict(schema='consulting-studio/proposed-s-repository@1', candidate_version=SKILLS_VERSION,
        canonical_commit=SOURCE, canonical_tree=TREE, public_base=PUBLIC_BASE,
        approval_request=request, standing=PUBLIC_STANDING,
        plugin_sha256=sha(outputs[NAME + '-' + SKILLS_VERSION + '-plugin.zip']),
        counts=dict(canonical_inputs=93, rebuild_inputs=len(rebuild), business_skills=27, modes=35, auxiliary_skills=3),
        gates={k: 'NOT_RUN' for k in ('publication', 'installation', 'native_execution', 'S_DIST', 'M_HOST', 'M_DIST', 'customer_acceptance')},
        files={p: dict(sha256=sha(d), bytes=len(d)) for p, d in sorted(repo.items()) if p != 'repository.json'})
    repo['repository.json'] = encoded(manifest)
    require(set(previous) <= set(repo), 'Public file removal is outside this candidate')
    ex.full_links({p: d for p, d in repo.items() if not p.startswith('rebuild/')})
    archive = pack.zip_bytes(repo)
    require(pack.unpack(archive, repo) == repo, 'Public repository proposal fidelity')
    outputs.update({NAME + '-' + SKILLS_VERSION + '-repository.zip': archive, 'repository.json': encoded(manifest)})
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rebuild-from', type=Path)
    parser.add_argument('--app-source', type=Path, help='Private complete existing App export/cache; no backend freshness inferred')
    parser.add_argument('--public-candidate', action='store_true', help='Proposed legal overlay; current exact approval remains PENDING')
    parser.add_argument('--public-base', type=Path, help='Exact finite existing-public source/document snapshot for repository asset')
    parser.add_argument('--app-candidate-skills', action='store_true', help='Use exact proposed S-candidate bytes in the separate private App candidate')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not (args.rebuild_from and args.app_source), 'S rebuild route excludes private App source')
    require(not (args.public_candidate and args.app_source), 'Public S route excludes private App input')
    require(args.public_candidate or args.public_base is None, '--public-base requires --public-candidate')
    require(not args.app_candidate_skills or args.app_source and not args.public_candidate and args.public_base is None,
            '--app-candidate-skills requires only the private App candidate route')
    for origin in (args.rebuild_from, args.app_source, args.public_base):
        if origin:
            require(args.output.absolute() != origin.absolute() and origin.absolute() not in args.output.absolute().parents,
                    'Output must be outside source inputs')
    selected, canonical, tools = inputs(args.rebuild_from)
    outputs = public_artifacts(selected, canonical, tools, args.public_base) if args.public_candidate or args.app_candidate_skills else artifacts(selected, canonical, tools)
    if args.app_source:
        # read_exact_tree rejects symlinks/nonregular entries before the bounded
        # shared reader reads bytes. Cache is evidence, never a backend guard.
        names = {p.relative_to(args.app_source).as_posix() for p in args.app_source.rglob('*') if not p.is_dir()}
        require(len(names) <= pack.MAX_MEMBERS, 'App source file-count limit')
        original = ex.read_exact_tree(args.app_source, names)
        skills, _ = public_plugin(selected, canonical, tools) if args.app_candidate_skills else build(selected, canonical, tools)
        shared_archive = NAME + '-' + SKILLS_VERSION + ('-plugin.zip' if args.app_candidate_skills else '-local-plugin.zip')
        overlay, effective, receipt = app_candidate(original, skills, outputs[shared_archive])
        for label, payload in [('update', overlay), ('complete-inspection', effective), ('prior-snapshot', original)]:
            data = pack.zip_bytes(payload)
            require(pack.unpack(data, payload) == payload, 'App archive fidelity')
            outputs['app-' + APP_VERSION + '-' + label + '.zip'] = data
        outputs['app-preservation.json'] = encoded(receipt)
    if args.public_candidate and args.public_base:
        published = (NAME + '-' + SKILLS_VERSION + '-plugin.zip',
                     NAME + '-' + SKILLS_VERSION + '-repository.zip', 'repository.json')
        outputs['SHA256SUMS'] = checksums({p: outputs[p] for p in published})
    else:
        outputs['SHA256SUMS'] = checksums(outputs)
    ex.write_outputs(args.output, outputs)
    print(json.dumps(dict(output=str(args.output), skills_version=SKILLS_VERSION, app_version=APP_VERSION if args.app_source else None,
                         publication='NOT_RUN', installation='NOT_RUN'), sort_keys=True))


if __name__ == '__main__':
    main()
