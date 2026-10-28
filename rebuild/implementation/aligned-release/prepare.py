#!/usr/bin/env python3
"""Prepare local aligned Skills/App candidates; never publish or install.

The frozen exporter and historical release approval remain unchanged. This new
revision consumes a separately pinned, S-only current-source selection. Existing
legal bytes are retained: this is not the later approved public legal overlay.
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
SOURCE = 'd673a8d1f2c22bbf07ef66bc29fe07e452526d19'
TREE = '14d0d32312eff656a1ff14e9beb2db4c9701c3a1'
SKILLS_VERSION = '1.1.0'
APP_VERSION = '1.0.12'
APP_ADAPTER_SOURCE = 'e8eac2aff9f1ac84355b947a4717fcbb4a532587'
APP_ADAPTER_HASHES = {
    'skills/studio-resume/SKILL.md': '9de9db8d9ecfbd28e310b1d7865a0f6da1c619a90298120d9aea37c56c7e680c',
    'skills/studio-resume/references/runtime-contract.md': 'bd12d1788e51553aebea8584a6a02a58324221d4223a17bc30bc4a5e7b7176bc',
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
SELECTION_SHA256 = '321b4458231fc8afaa8b976c26e32f4704bd1bccefd8ef951dbad01d52230a86'
PUBLIC_BASE = '033b83abf2a2a338687dd1b739465bca77e8d8b5'
PUBLIC_BASE_FILES = {'AUDIT.md': '18a4c915e6937218c28df4b446aabca1428ed2be764ebb2566492c477a8a8e3d',
 'CHANGELOG.md': 'db94407aec2a6b26a22dfa59c67171c18852c4da8182661f3e18f05aad6c572c',
 'INSTALL-TEST-PLAN.md': '30985cabb9bc3f35dd5067aee087cdf6185ba185b3ef6cb4de1a9ac1b7d1dea6',
 'KNOWN-LIMITS.md': '75c949b25c8b320f0222e3a124a69c464da5f82d10e3c44e5490427d12036bb5',
 'OWNER-DECISIONS.md': '5f56f839040524e5c13a9983521ed934165569052414bcd1ce1ce59267e2432e',
 'README.md': 'd458adb2e7e11292ce60a772d81d151f0bcd5d85b46ce2d2a0f316d0cc121cf8',
 'SECURITY.md': '80d76089775f21a4c1ac1950be5c96df8512e641862f46a828d514d4ee2b38f4',
 'SUPPORT.md': '98ccd11f5469a2b1ddd167fa85dbf0a1c74050c3af9978c92f9edf5bfa045d79',
 'implementation/s-distribution/AUDIT.md': '0f9fc1a7275d3840d8741c8ed09080eb2f40f47eaaa7037669d415654675735d',
 'implementation/s-distribution/CHANGELOG.md': 'db94407aec2a6b26a22dfa59c67171c18852c4da8182661f3e18f05aad6c572c',
 'implementation/s-distribution/INSTALL-TEST-PLAN.md': '30985cabb9bc3f35dd5067aee087cdf6185ba185b3ef6cb4de1a9ac1b7d1dea6',
 'implementation/s-distribution/KNOWN-LIMITS.md': '75c949b25c8b320f0222e3a124a69c464da5f82d10e3c44e5490427d12036bb5',
 'implementation/s-distribution/NOTICE-S.proposed.txt': '4235c333ef37e7c6d8a352cda1ab9cd0880d4b5d21ba13892b32a81ee0ac94df',
 'implementation/s-distribution/OWNER-DECISIONS.md': '5f56f839040524e5c13a9983521ed934165569052414bcd1ce1ce59267e2432e',
 'implementation/s-distribution/README.md': 'bd546b38c5c0d27f644e9169632eaab7812b703471a56f2a18df7255de661e8e',
 'implementation/s-distribution/SECURITY.md': '80d76089775f21a4c1ac1950be5c96df8512e641862f46a828d514d4ee2b38f4',
 'implementation/s-distribution/SUPPORT.md': '98ccd11f5469a2b1ddd167fa85dbf0a1c74050c3af9978c92f9edf5bfa045d79',
 'implementation/s-distribution/approved-scope.json': '6248cbe9957b91b65e10413abb934b3ac33111f1e542fdd6419732ac6693f4b0',
 'implementation/s-distribution/approved-source-delta.json': '19b525f388c8fd3f14d4fbb245cadc549cc7ae022c9729c0e49cb49cf25be2b4',
 'implementation/s-distribution/prepare.py': '4939cf2a5c0e4fd76b6bd8fba9484c601532f646381d816402bc867101dea628',
 'legal/history/NOTICE-S.proposed.txt': '4235c333ef37e7c6d8a352cda1ab9cd0880d4b5d21ba13892b32a81ee0ac94df',
 'legal/history/approved-scope.json': '6248cbe9957b91b65e10413abb934b3ac33111f1e542fdd6419732ac6693f4b0',
 'legal/history/approved-source-delta.json': '19b525f388c8fd3f14d4fbb245cadc549cc7ae022c9729c0e49cb49cf25be2b4'}
PUBLIC_NOTICE = b'PROPOSED S NOTICE ONLY \xe2\x80\x94 not adopted; inherited operative NOTICE is unchanged.\n\nConsulting Studio\nCopyright 2026 cogni-work contributors\n\nProduct vision and business architecture are selectively adapted from\ncogni-work/cogni-consulting, commit\n651a17604ab3cb456010b804b334e9c504a3fad9, Apache-2.0.\n\n    cogni-consulting\n    Copyright 2026 Stephan de Haas / cogni-work.ai\n\nProblem-structuring/framework-selection and communication-craft vocabulary derives\nthrough prior method references from insight-wave, commit\nfbce470260b9244b3a687bf1177a593f5f6600e3, including cogni-publishing 0.0.35,\nApache-2.0.\n\n    insight-wave\n    Copyright 2026 Stephan de Haas / cogni-work.ai\n\nTheme-selection/application concepts are informed by Anthropic theme-factory,\ncommit 683bc88e56f3e09ba94f7055977f3d3aa499f202, Apache-2.0.\n\n    Copyright 2026 Anthropic, PBC.\n\nDoc-coauthoring is credited as a conceptual workflow reference at that revision.\nBruce Mau\'s MC24, "Quantify and Visualize," is credited as owner-supplied inspiration.\nNo book pages/images, theme assets, fonts or upstream renderer code are redistributed\nin S. The optional Setup example is labelled fictional; historical rendered\nfixtures/evaluation adapters are excluded.\n\nConsulting Studio modifications, 2026-10-04 and 2026-10-09: independently rewritten\nproduct/business and communication requirements selectively retain the above\nvocabulary, evidence qualifications, human decisions and consulting scope.\n\nConsulting Studio modification, 2026-10-27: S source packaging rewrites required\nresource locators to complete local resources, composes working instructions,\nadds explicit working-instruction reads where applicable and per-file change\nnotices. Canonical source bytes, inherited grants and historical distributions\nremain unchanged. Exact source hashes and transformations accompany the package.\n\nThis proposed notice supplies attribution, not a new grant or approval. Actual\nthird-party rights and existing recipient grants remain preserved. The new\nS-wide first-party Apache proposal requires exact owner adoption separately.\n'
APACHE_SHA256 = 'c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4'
NOTICE_SHA256 = '4235c333ef37e7c6d8a352cda1ab9cd0880d4b5d21ba13892b32a81ee0ac94df'
OPEN_DELTA = (
    'implementation/plugin-setup/skills/setup/SKILL.md',
    'implementation/plugin-setup/skills/setup/agents/openai.yaml',
    'implementation/plugin-setup/skills/setup/references/optional-synthetic-example.md',
    SELF, SELECTION,
)
PUBLIC_STANDING = 'OWNER-APPROVED S1.1.0 RELEASE PREPARED; publication separately recorded; installation and acceptance NOT_RUN'
PUBLIC_MODIFICATION = ('Consulting Studio packaging modification, 2026-10-28: local resource locators '
    'and explicit governing reads; canonical source and emitted hashes in distribution.json. '
    'Owner-approved S1.1.0 Apache/NOTICE overlay; existing recipient grants retained.')
REBUILD = b'# Finite Skills rebuild inputs\n\nInspect the complete input inventory and extract into an empty directory.\nPython3 standard library only; no Git, constructor, network or App required.\n\nFor the retained local technical view:\n\n    python3 -B implementation/aligned-release/prepare.py --rebuild-from . --output ../aligned-technical\n\nFor the owner-approved public1.1.0 legal overlay:\n\n    python3 -B implementation/aligned-release/prepare.py --rebuild-from . --public-release --output ../s-1.1.0-rebuilt\n\nUse a new output outside the input tree, with no symlink ancestors. Compare the\nfour selected-route S artifacts and SKILLS-SHA256SUMS with the reviewed original.\nThe technical route retains canonical legal evidence; the public route applies\nthe exact approved Apache/NOTICE copies and current five-path owner approval.\nA combined private App/S SHA256SUMS contains additional private files and differs\nfrom the standalone S checksum list. No App inputs or archives are included here.\nThese commands build files only; publication, plugin update, installation and\nactual host/customer acceptance remain separate operations and evidence.\n'


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
            require(paths == selected['resource_sets'][row['required_set']] and len(edges) == 453, 'Dependency closure drift')
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


def app_candidate(original, skills, skills_archive):
    """Update common skills; retain the compatible App adapter and App settings."""
    require('plugin.json' in original and '.codex-plugin/plugin.json' in original and '.app.json' in original,
            'Expected existing portable App export')
    previous = decode(original['consulting-studio-skills.json'])
    require(set(previous['files']) == set(original) - {'consulting-studio-skills.json'}
            and all(sha(original[p]) == (r['sha256'] if isinstance(r, dict) else r) for p, r in previous['files'].items()),
            'Original App provenance/inventory mismatch')
    portable, legacy = decode(original['plugin.json']), decode(original['.codex-plugin/plugin.json'])
    require(portable['name'] == legacy['name'] and portable['version'] == legacy['version'], 'App identity conflict')
    require(portable['version'] == '1.0.11', 'This candidate requires the reconciled App1.0.11 source profile')
    require(setup.version_tuple(APP_VERSION) > setup.version_tuple(portable['version']), 'App version must increase')
    require(portable['extensions']['com.openai']['apps'] == './.app.json'
            and portable['extensions']['com.openai']['onboardingSkill'] == setup.ENTRY, 'Unexpected App declaration')
    names = {p.split('/')[1] for p in skills if p.startswith('skills/')} - {'studio-resume'}
    common = {p: d for p, d in skills.items() if p.startswith('skills/') and p.split('/')[1] in names}
    old_common = {p for p in original if p.startswith('skills/') and p.split('/')[1] in names}
    require(old_common <= set(common), 'Stale App skill paths need explicit reviewed deletion')
    require({p.split('/')[1] for p in original if p.startswith('skills/')} <= names | {'studio-resume'}, 'Unrecognized App skill/adaptation')
    old_variant = {p: d for p, d in original.items() if p.startswith('skills/studio-resume/')}
    require(set(old_variant) == set(APP_ADAPTER_HASHES)
            and all(sha(old_variant[p]) == h for p, h in APP_ADAPTER_HASHES.items()), 'Compatible App adapter source drift')
    # Current canonical adapter0.2.0 requires cardId. The preserved existing App
    # tools expose no cardId argument, so no App deployment or adapter upgrade is
    # inferred from a shared Skills update. Keep this exact0.1.2 variant instead.
    portable['version'], legacy['version'] = APP_VERSION, APP_VERSION
    overlay = {**common, 'plugin.json': encoded(portable), '.codex-plugin/plugin.json': encoded(legacy)}
    effective = {**original, **overlay}
    shared_info = decode(skills['distribution.json'])
    approved_shared = shared_info['legal']['status'] == 'APPROVED_RELEASE_SPECIFIC'
    app_standing = ('OWNER-APPROVED APP1.0.12 CANDIDATE WITH PUBLIC SKILLS1.1.0; update and host acceptance NOT_RUN'
                    if approved_shared else STANDING)
    provenance = dict(schema='consulting-studio/aligned-app-candidate@1', version=APP_VERSION,
        shared_skills_release=SKILLS_VERSION, shared_skills_archive_sha256=sha(skills_archive),
        shared_skills_variant='approved public release' if approved_shared else 'historical local technical candidate',
        source_commit=SOURCE, source_tree=TREE, standing=app_standing,
        common_skill_files={p: sha(d) for p, d in sorted(common.items())},
        app_resume_variant=dict(version='0.1.2', source_commit=APP_ADAPTER_SOURCE,
            files=APP_ADAPTER_HASHES, changed=False,
            reason='Preserved App API lacks cardId required by canonical adapter0.2.0; separate runtime-qualified adoption required'),
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
        original_sha256={p: sha(d) for p, d in sorted(original.items())},
        retained_sha256={p: sha(d) for p, d in sorted(original.items()) if p not in overlay},
        overlay_sha256={p: sha(d) for p, d in sorted(overlay.items())},
        scope='Partial update only; no App source, binding, interface, visibility, access or deployment change')
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


def owner_approval():
    return dict(status='APPROVED_RELEASE_SPECIFIC', approved_at='2026-10-28T11:30Z', time_precision='minute',
        source='Product owner directly approved Skills1.1.0, separate App1.0.12 and the five identified open source paths',
        open_paths=list(OPEN_DELTA), scope='Three changed Setup sources and two new packaging source inputs under Apache-2.0; existing public sources and rights retained',
        excluded='GUI/MCP/server/App code, private bindings/history, customer content and credentials',
        private_app_update='Separately coordinated; no plugin update operation in this generator',
        installation_and_acceptance='NOT_AUTHORIZED_OR_ESTABLISHED_BY_THIS_RELEASE')


def public_plugin(selected, canonical, tools):
    """Apply only the approved current legal/metadata overlay, retaining source."""
    files, info = build(selected, canonical, tools)
    files.pop('distribution.json')
    apache = canonical['LICENSE'].split(b'PART B: APACHE LICENSE, VERSION 2.0\n\n', 1)[1]
    require(sha(apache) == APACHE_SHA256 and sha(PUBLIC_NOTICE) == NOTICE_SHA256, 'Approved legal payload drift')
    technical = dict(files)
    for path, before in list(files.items()):
        data = before
        if Path(path).name == 'LICENSE':
            data = apache
        elif Path(path).name == 'NOTICE':
            data = PUBLIC_NOTICE
        else:
            data = data.replace(MODIFICATION.encode(), PUBLIC_MODIFICATION.encode())
        files[path] = data
    for path in ('plugin.json', '.codex-plugin/plugin.json'):
        manifest = decode(files[path]); manifest['license'] = 'Apache-2.0'
        files[path] = encoded(manifest)
    for path in list(files):
        if path.startswith('skills/') and path.endswith('/manifest.json'):
            manifest = decode(files[path]); prefix = path.rsplit('/', 1)[0] + '/'
            manifest['standing'] = PUBLIC_STANDING
            manifest['release_identity'] = dict(name=NAME, version=SKILLS_VERSION, license='Apache-2.0')
            for row in manifest['resources']:
                row['emitted_sha256'] = sha(files[prefix + row['emitted_path']])
            manifest['files'] = {p: sha(files[prefix + p]) for p in manifest['files']}
            files[path] = encoded(manifest)
    for row in info['canonical_to_emitted']:
        path = row['output_path']
        row['technical_emitted_sha256'] = row['emitted_sha256']
        row['emitted_sha256'] = sha(files[path])
        if Path(path).name in ('LICENSE', 'NOTICE'):
            row['release_adaptations'] = ['Owner-approved operative legal copy; exact canonical input retained in rebuild evidence']
    info.update(schema='consulting-studio/approved-s-release-plugin@1', standing=PUBLIC_STANDING,
        owner_approval=owner_approval(), legal=dict(status='APPROVED_RELEASE_SPECIFIC', license='Apache-2.0',
            license_sha256=APACHE_SHA256, notice_sha256=NOTICE_SHA256,
            meaning='Operative copies apply the approved exact Apache text and S NOTICE; historical proposal wording is superseded by this new owner adoption without altering attribution. Canonical rebuild legal inputs retain their original evidence meaning.'),
        delivery_gates=dict(exact_owner_release_export_approval='APPROVED_RELEASE_SPECIFIC', operative_public_legal_overlay='APPLIED'),
        release_adaptations=[dict(path=p, previous_sha256=sha(technical[p]), sha256=sha(d),
            reason='Approved operative legal/manifest copy or updated prominent packaging notice; canonical source unchanged')
            for p, d in sorted(files.items()) if d != technical[p]],
        files={p: dict(sha256=sha(d), bytes=len(d)) for p, d in sorted(files.items())})
    files['distribution.json'] = encoded(info)
    ex.full_links(files); methods.check_runtime_instructions(files); ex.scan_runtime(files)
    pack.manifest_checks(files, [r['name'] for r in selected['skills']], SKILLS_VERSION, auxiliary=ex.AUXILIARY_SKILLS)
    return files, info


def public_artifacts(selected, canonical, tools, base=None):
    """Create approved S assets, optionally with a finite existing-public document tree."""
    plugin, info = public_plugin(selected, canonical, tools)
    rebuild = {**{'canonical/' + p: d for p, d in canonical.items()}, **tools, 'REBUILD.md': REBUILD}
    outputs = {NAME + '-' + SKILLS_VERSION + '-plugin.zip': pack.zip_bytes(plugin),
        NAME + '-' + SKILLS_VERSION + '-rebuild.zip': pack.zip_bytes(rebuild),
        'distribution.json': encoded(info), 'selection.json': encoded(selected)}
    outputs['SKILLS-SHA256SUMS'] = checksums(outputs)
    if base is None:
        return outputs
    retained = {p: regular(Path(base) / p) for p in PUBLIC_BASE_FILES}
    require(all(sha(retained[p]) == h for p, h in PUBLIC_BASE_FILES.items()), 'Public base changed; reconcile remote owner edits before release')
    repo = dict(retained)
    repo['README.md'] = repo['README.md'].replace(b'/v0.1.0/', b'/v1.1.0/').replace(
        b'/tag/v0.1.0', b'/tag/v1.1.0').replace(b'0.1.0-plugin.zip', b'1.1.0-plugin.zip').replace(
        b'Download the 0.1.0 plugin ZIP', b'Download the 1.1.0 plugin ZIP')
    audit = ('''# Current S release 1.1.0, 2026-10-28\n\nSetup0.1.7 adds Installation prüfen; the27 business methods and Librarian0.2.1\nretain their canonical sources. The owner approved the three changed Setup inputs\nand two new packaging inputs under Apache-2.0 on2026-10-28 at11:30UTC.\nThe exact current scope and generated legal overlay are recorded in legal/scope.json.\nPublic0.1.0 and its tag/assets remain immutable historical evidence.\n\nRebuild the current plugin without Git, network, private history or an App:\n\n    python3 -B rebuild/implementation/aligned-release/prepare.py --rebuild-from rebuild --public-release --output ../s-1.1.0-rebuilt\n\nCompare the four S artifacts with SKILLS-SHA256SUMS at this repository's root.\nThe repository ZIP separately preserves current public documentation and unchanged\nhistorical public source/history; two builds from the pinned public base reproduce\nits bytes. The old implementation/s-distribution generator below describes0.1.0.\nNo installation, native qualification, update/recovery or customer acceptance is\nestablished by source/package checks or publication. Issue228 remains open.\n\n---\n\n''').encode()
    repo['AUDIT.md'] = audit + repo['AUDIT.md']
    repo['CHANGELOG.md'] = ('''# 1.1.0 - 2026-10-28\n\n- Setup0.1.7 exposes Installation prüfen for a bounded, evidence-backed session check.\n- Same27 business methods/35 modes, Librarian0.2.1 and neutral Resume0.2.0.\n- Unified future public/test Skills train; App versions remain separate.\n- Five-path open source extension and exact Apache/NOTICE overlay adopted by the owner.\n- Installation, runtime qualification and acceptance remain separate and NOT_RUN.\n\n''').encode() + repo['CHANGELOG.md']
    apache = canonical['LICENSE'].split(b'PART B: APACHE LICENSE, VERSION 2.0\n\n', 1)[1]
    repo.update({'LICENSE': apache, 'NOTICE': PUBLIC_NOTICE,
        'legal/LICENSE-Apache-2.0.txt': apache, 'legal/NOTICE-S.txt': PUBLIC_NOTICE})
    repo['legal/README.md'] = ('''# Current release scope\n\nThe current1.1.0 overlay applies the complete Apache text and unchanged S NOTICE.\nThe new owner adoption at2026-10-28 11:30UTC covers exactly the five canonical\npaths in scope.json. Existing grants and attribution remain preserved.\nThe exact2026-10-27 approval evidence under history retains its original meaning;\nit is not rewritten into approval of new bytes. Canonical LICENSE/NOTICE in rebuild\nare exact historical evidence, not the operative public legal copies.\nNo App/GUI/MCP/server software or private material is licensed or shipped here.\n''').encode()
    repo.update({'plugin/' + p: d for p, d in plugin.items()})
    repo.update({'rebuild/' + p: d for p, d in rebuild.items()})
    repo['SKILLS-SHA256SUMS'] = outputs['SKILLS-SHA256SUMS']
    delta = [dict(path=p, sha256=sha(canonical[p] if p in canonical else tools[p]),
        change='changed canonical runtime source' if p in canonical else 'new packaging source input') for p in OPEN_DELTA]
    repo['legal/source-delta.json'] = encoded(dict(schema='consulting-studio/s-release-source-delta@1',
        approval=owner_approval(), components=delta, previous_public_base=PUBLIC_BASE,
        canonical_inputs=93, unchanged_runtime_inputs=90,
        generated_outputs='Legal copies, manifests, release metadata/notices and finite rebuild snapshot derive from these approved inputs; no additional canonical source component'))
    repo['legal/scope.json'] = encoded(dict(schema='consulting-studio/s-release-scope@1',
        approval=owner_approval(), name=NAME, version=SKILLS_VERSION, license='Apache-2.0',
        source_commit=SOURCE, source_tree=TREE, selection_sha256=SELECTION_SHA256,
        canonical_components=[dict(path=p, sha256=sha(d)) for p, d in sorted(canonical.items())],
        rebuild_tools=[dict(path=p, sha256=sha(d)) for p, d in sorted(tools.items())],
        source_delta=dict(path='legal/source-delta.json', sha256=sha(repo['legal/source-delta.json'])),
        legal=dict(license_sha256=APACHE_SHA256, notice_sha256=NOTICE_SHA256),
        history={p: sha(d) for p, d in retained.items() if p.startswith('legal/history/')},
        existing_grants='Preserved; no withdrawal or new GUI/MCP/App grant',
        generated_transformations=['Operative exact legal copies', 'Current public release links; latest owner README deletion retained',
            'Current release/audit metadata ahead of retained public history', 'Current hashes and prominent packaging notices']))
    manifest = dict(schema='consulting-studio/approved-s-repository@1', candidate_version=SKILLS_VERSION,
        canonical_commit=SOURCE, canonical_tree=TREE, public_base=PUBLIC_BASE,
        approval=owner_approval(), standing=PUBLIC_STANDING,
        plugin_sha256=sha(outputs[NAME + '-' + SKILLS_VERSION + '-plugin.zip']),
        source_delta_sha256=sha(repo['legal/source-delta.json']),
        counts=dict(canonical_inputs=93, rebuild_inputs=len(rebuild), business_skills=27, modes=35, auxiliary_skills=3),
        gates={k: 'NOT_RUN' for k in ('publication', 'installation', 'native_execution', 'S_DIST', 'M_HOST', 'M_DIST', 'customer_acceptance')},
        files={p: dict(sha256=sha(d), bytes=len(d)) for p, d in sorted(repo.items())})
    repo['repository.json'] = encoded(manifest)
    ex.full_links({p: d for p, d in repo.items() if not p.startswith('rebuild/')})
    archive = pack.zip_bytes(repo)
    require(pack.unpack(archive, repo) == repo, 'Public repository archive fidelity')
    outputs.update({NAME + '-' + SKILLS_VERSION + '-repository.zip': archive, 'repository.json': encoded(manifest)})
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rebuild-from', type=Path)
    parser.add_argument('--app-source', type=Path, help='Private complete existing App export/cache; no backend freshness inferred')
    parser.add_argument('--public-release', action='store_true', help='Apply owner-approved1.1.0 legal overlay; no publication operation')
    parser.add_argument('--public-base', type=Path, help='Exact finite existing-public source/document snapshot for repository asset')
    parser.add_argument('--app-public-skills', action='store_true', help='Use exact public-release Skills bytes in the separate private App candidate')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not (args.rebuild_from and args.app_source), 'S rebuild route excludes private App source')
    require(not (args.public_release and args.app_source), 'Public S route excludes private App input')
    require(args.public_release or args.public_base is None, '--public-base requires --public-release')
    require(not args.app_public_skills or args.app_source and not args.public_release and args.public_base is None,
            '--app-public-skills requires only the private App candidate route')
    for origin in (args.rebuild_from, args.app_source, args.public_base):
        if origin:
            require(args.output.absolute() != origin.absolute() and origin.absolute() not in args.output.absolute().parents,
                    'Output must be outside source inputs')
    selected, canonical, tools = inputs(args.rebuild_from)
    outputs = public_artifacts(selected, canonical, tools, args.public_base) if args.public_release or args.app_public_skills else artifacts(selected, canonical, tools)
    if args.app_source:
        # read_exact_tree rejects symlinks/nonregular entries before the bounded
        # shared reader reads bytes. Cache is evidence, never a backend guard.
        names = {p.relative_to(args.app_source).as_posix() for p in args.app_source.rglob('*') if not p.is_dir()}
        require(len(names) <= pack.MAX_MEMBERS, 'App source file-count limit')
        original = ex.read_exact_tree(args.app_source, names)
        skills, _ = public_plugin(selected, canonical, tools) if args.app_public_skills else build(selected, canonical, tools)
        shared_archive = NAME + '-' + SKILLS_VERSION + ('-plugin.zip' if args.app_public_skills else '-local-plugin.zip')
        overlay, effective, receipt = app_candidate(original, skills, outputs[shared_archive])
        for label, payload in [('update', overlay), ('complete-inspection', effective), ('prior-snapshot', original)]:
            data = pack.zip_bytes(payload)
            require(pack.unpack(data, payload) == payload, 'App archive fidelity')
            outputs['app-' + APP_VERSION + '-' + label + '.zip'] = data
        outputs['app-preservation.json'] = encoded(receipt)
    if args.public_release and args.public_base:
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
