#!/usr/bin/env python3
"""Generate a local S technical candidate; never authorize delivery.

The operational archive and its finite rebuild inputs are separate artifacts.
Rebuilds read only the selected canonical bytes, public runtime catalog and the
listed packaging tools. No Git, constructor, npm, server or network is needed.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat
import sys
from urllib.parse import unquote, urlsplit

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
SELF = 'implementation/s-export/export.py'
INVENTORY_COMMIT = 'af366eb93a8aaa06be220d67e1fdc9fd2c276bf6'
INVENTORY_TREE = 'f78e2cb6c31fec1ff35a0b8fb9f5c06a1f47d471'
INVENTORY_SHA256 = '7a93d9f135d3729c11277378f3760bb6c3e13b5c03d819456bf307a3aca61964'
SELECTION_SHA256 = 'e9dc1747aea1d8d1a5c07f55d3458e0739daab5e61ce81bef4649d9810e855b4'
BUILD_INPUTS = {
    'implementation/business-skills/release.py': '25b27ef1416b17164daaa2366f906b7ffdd818eb3631d37678f1442c7ec04e89',
    'implementation/business-skills/check_packages.py': '34e029ad1cc6f2ae4efc7dcc940517d7b37fd8a931b7bc7d9de62eacc84818f6',
    'implementation/plugin-distribution/release.py': 'd6b57e160bc386df4519d1cfcca6756fa3d0354d2ba876016466c913688c798a',
    'implementation/plugin-setup/package_update.py': '0e3c80d778e4c67508ca379badb3ca92f5703512830360c093fb08cc91976fd9',
    'implementation/plugin-distribution/plugin.json': '4a6d7c007663232cbb2ff7f63a3d1b200abd229afb9ed77873768c2d4004affb',
}


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Verify build dependencies before importing any of their Python code. The
# reviewed exporter itself is the trust root; its digest is recorded externally.
for _path, _sha in BUILD_INPUTS.items():
    _file = ROOT / _path
    if any(p.is_symlink() for p in (_file, *_file.parents)) or not _file.is_file() or \
            _file.stat().st_size > 8 * 1024 * 1024 or hashlib.sha256(_file.read_bytes()).hexdigest() != _sha:
        raise ValueError('Unreviewed/nonregular packaging dependency before import: ' + _path)

pack = load('s_export_pack', 'implementation/plugin-distribution/release.py')
methods, links, setup = pack.methods, pack.links, pack.setup
require, digest, encoded = methods.require, methods.digest, methods.encoded
STANDING = 'LOCAL TECHNICAL CANDIDATE ONLY; rights and export unapproved; installation and native behavior NOT_RUN'
EXPORT_VERSION = '0.2.0'
S_SOURCE_FILES = 93
AUXILIARY_SKILLS = ('setup', 'workspace-bindings', 'studio-resume')
CANDIDATE = 'consulting-studio-S-local-candidate.zip'
REBUILD = 'consulting-studio-S-rebuild-inputs.zip'
DESCRIPTOR = 'rebuild.json'
INSTRUCTIONS = b'''# Local S candidate rebuild\n\nThis is a generated, read-only input snapshot, not another editable method source.\nChange the canonical repository, revise and review the inventory, then regenerate.\n\nAfter inspecting the archive inventory, extract it into an empty local directory.\nFrom that directory, run (Python 3 standard library only):\n\n    python3 -B implementation/s-export/export.py --rebuild-from . --output /tmp/s-rebuilt\n\nNo Git checkout/history, constructor, M purchase, npm, Studio MCP server or network\nis needed. The resulting archive hashes must match the originating evidence.\nThe operational ZIP contains skills/resources only; packaging Python is separate.\nThe supplied tooling itself has pending distribution rights and export authority.\nLocal reproducibility establishes no public release, grant, installation or host\nqualification. LICENSE/NOTICE are the exact inherited inventory payload; no new\nS grant or delivery-specific notice subset has been activated. All delivery stops\nuntil the actual owner/legal/export decisions and review cover these exact bytes.\nThe source Git commit/tree and inventory are provenance, not available public URLs.\n'''
LIMITS = b'''# Local technical candidate\n\nThis generated S package is for local inspection and checks only. Rights and\nexport decisions remain pending. It activates no new license or installation.\nThe plugin version label is retained from the inspected metadata; the exact\narchive, generator and resource hashes identify this separate technical candidate.\n\nFor an eventual separately authorized self-install, first verify the actual host's\nsupported plugin/skill import route, workspace eligibility, intended audience and\nresource format. Inspect the exact inventory and preserve applicable LICENSE and\nNOTICE. No importer API, automatic updates or cross-surface compatibility is\nassumed. Import, enablement, connectors and workspace-agent adoption need separate\nobserved evidence and their actual authority. This work runs none of those steps.\n\nThe package exposes 27 business methods and three separate auxiliary entries: Setup,\nWorkspace Librarian (workspace-bindings), and Resume (studio-resume). Each method has its\ncomplete local governing resources. Read its working instructions before use.\nSetup can inspect existing settings and offer agreed changes; its workflow check\ncan be skipped, use permitted supplied content or use the optional labelled\nsynthetic example. Do not create homes, save settings or send material merely to\nvalidate this archive. A later authorized host check should exercise a selected\nordinary request, required-resource readback, actual output and applicable reader\nchecks; record method availability, enablement, connector authority, saving,\nreadback, continuity and owner acceptance separately.\n\nResearch, storage, rendering and inspection require actually available authorized\nhost tools and permitted inputs. This package supplies no execution engine,\nconnectors, credentials, customer settings, Studio MCP server or GUI. An unread\nrequired resource blocks its dependent operation. Continue permitted independent\nwork with the limit explicit. Fresh install, native behavior, all standard routes,\nworkspace availability, update/rollback and owner acceptance remain NOT_RUN.\n\nDistribution metadata records every canonical transformation and generated file.\nThe separate finite rebuild-input ZIP and its REBUILD.md explain local Python-only\nreproduction. They are build inputs with their own pending distribution rights,\nnot another editable method source. No public availability is established.\n'''


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def decode(data):
    return json.loads(data, object_pairs_hook=unique)


def safe_path(path):
    pack.safe_path(path)
    require('%' not in path and not any(part.casefold() in
        {'.git', '.env', 'credentials', 'secrets'} for part in PurePosixPath(path).parts),
        'Unsafe/private path: ' + path)
    return path


def check_paths(paths):
    folded = set()
    for path in paths:
        safe_path(path)
        require(path.casefold() not in folded, 'Duplicate/case-colliding path: ' + path)
        folded.add(path.casefold())


def regular_read(path, limit=pack.MAX_MEMBER_BYTES):
    path = Path(path).absolute()
    require(not any(p.is_symlink() for p in (path, *path.parents)), 'Input/ancestor symlink: ' + str(path))
    require(path.is_file() and stat.S_ISREG(path.stat().st_mode), 'Nonregular input: ' + str(path))
    require(path.stat().st_size <= limit, 'Input byte limit: ' + str(path))
    return path.read_bytes()


def read_exact_tree(root, expected):
    """Walking is for rejection only; the finite expected set controls every read."""
    root = Path(root).absolute()
    require(not any(p.is_symlink() for p in (root, *root.parents)), 'Input/ancestor symlink')
    require(root.is_dir(), 'Missing input directory')
    check_paths(expected)
    actual = set()
    directories = {str(parent) for p in expected for parent in PurePosixPath(p).parents if str(parent) != '.'}
    for path in root.rglob('*'):
        name = safe_path(path.relative_to(root).as_posix())
        require(not path.is_symlink(), 'Input symlink: ' + name)
        if path.is_dir():
            require(name in directories, 'Unexpected input directory: ' + name)
        else:
            require(stat.S_ISREG(path.stat().st_mode), 'Nonregular input: ' + name)
            actual.add(name)
    require(actual == set(expected), 'Complete input file allowlist mismatch')
    result = {}
    for path in sorted(expected):
        # Canonical inputs have the member cap. Artifact comparisons know exact
        # expected sizes and permit the separately bounded whole ZIP size.
        value = expected.get(path) if isinstance(expected, dict) else None
        limit = pack.MAX_MEMBER_BYTES if not isinstance(value, bytes) else min(len(value), pack.MAX_ARCHIVE_BYTES)
        result[path] = regular_read(root / path, limit=limit)
    return result


def selection(inventory):
    rows = [row for row in inventory['files'] if row['placement'] == 'S']
    return dict(schema='consulting-studio/s-selection@1', repository=inventory['repository'],
        inventory_commit=INVENTORY_COMMIT, inventory_tree=INVENTORY_TREE,
        inventory_sha256=INVENTORY_SHA256, source_commit=inventory['source_commit'], source_tree=inventory['source_tree'],
        files=rows, skills=inventory['skills'], resource_sets=inventory['resource_sets'],
        auxiliary_entries=inventory['auxiliary_entries'], helper_adapter_boundary=inventory['helper_adapter_boundary'],
        rights_profiles={key: inventory['rights_profiles'][key] for key in sorted({r['rights_profile'] for r in rows})},
        gates=[gate for gate in inventory['gates'] if 'S' in gate['offers']], legacy_apache=inventory['legacy_apache'])


def check_selection(selected):
    require(digest(encoded(selected)) == SELECTION_SHA256, 'Unreviewed S selection/rights/catalog projection')
    paths = [r['path'] for r in selected['files']]
    check_paths(paths)
    require(len(paths) == S_SOURCE_FILES, 'Incomplete versioned S source selection')


def audit_checkout():
    """Private canonical audit before producing the portable, S-only projection."""
    require(methods.git('rev-parse', INVENTORY_COMMIT + '^{tree}').decode().strip() == INVENTORY_TREE,
            'Inventory implementation tree drift')
    for name in ('inventory.py', 'policy.json', 'npm-evidence.json', 'npm-reconciliation.json'):
        relative = 'implementation/release-inventory/' + name
        require(regular_read(ROOT / relative) == methods.git('show', INVENTORY_COMMIT + ':' + relative),
                'Unreviewed inventory validator/input: ' + relative)
    audit = load('s_export_audit', 'implementation/release-inventory/inventory.py')
    path = 'implementation/release-inventory/inventory.json'
    data = methods.git('show', INVENTORY_COMMIT + ':' + path)
    require(digest(data) == INVENTORY_SHA256 and regular_read(ROOT / path) == data, 'Inventory snapshot drift')
    # Reuse the reviewed, fail-closed validator; no approval override is supported.
    inventory = decode(data)
    audit.validate_inventory(inventory, current_base=inventory['source_commit'])
    selected = selection(inventory)
    check_selection(selected)
    source = methods.RuntimeSource(selected['source_commit'])
    canonical = {row['path']: source.read(row['path']) for row in selected['files']}
    blockers = audit.selection_blockers(inventory, list(canonical.items()), current_base=source.commit,
        offer='S', notice_payload={p: canonical[p] for p in ('LICENSE', 'NOTICE')})
    require(blockers, 'Unexpected delivery clearance; review a new selection explicitly')
    return selected, canonical


def scan_runtime(files):
    """Exact fidelity is primary; these denials also guard future reviewed inputs."""
    private = re.compile(r'(?i)(?:https?://)?(?:chatgpt\.com/(?:c|share|g)/|chat\.openai\.com/|'
        r'[^/\s]+\.sharepoint\.com/|[^/\s]+\.slack\.com/|notion\.so/|'
        r'localhost(?::\d+)?/|127\.0\.0\.1(?::\d+)?/)|'
        r'(?i:sk-(?:proj-)?[A-Za-z0-9_-]{16,}|AKIA[A-Z0-9]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)|'
        r'(?i:(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[=:]\s*["\']?[^\s"\']{8,})')
    for path, data in files.items():
        require(not private.search(data.decode('utf-8')), 'Private/live/credential content: ' + path)
        # All legal URLs are retained only inside the exact pinned legal payload.
        if PurePosixPath(path).name not in ('LICENSE', 'NOTICE'):
            text = data.decode()
            if path == 'plugin.json':
                metadata = decode(data)
                require(metadata.pop('$schema') == setup.SCHEMA, 'Unreviewed plugin schema')
                text = encoded(metadata).decode()
            require(not re.search(r'(?i)(?:https?|wss?)://', text), 'External operational locator: ' + path)


class SelectedRuntimeSource(methods.RuntimeSource):
    """The same runtime resolver over exact selected bytes, without constructor reads."""
    def __init__(self, selected, canonical):
        check_selection(selected)
        self.commit, self.tree = selected['source_commit'], selected['source_tree']
        self.paths = {row['path'] for row in selected['files']}
        require(set(canonical) == self.paths, 'Canonical source allowlist mismatch')
        self.cache = dict(canonical)
        for row in selected['files']:
            data = self.cache[row['path']]
            require(digest(data) == row['sha256'] and len(data) == row['bytes'], 'Canonical source bytes drift: ' + row['path'])
            if row['path'].endswith('.json'):
                decode(data)
        self.catalog = decode(self.read('implementation/runtime/method-catalog.json'))
        self.items = {row['name']: row for row in self.catalog['skills']}
        self.methods = {row['name']: row['method_resources'] for row in selected['skills']}
        require(list(self.items) == list(self.methods) and len(self.items) == 27
                and sum(len(row['modes']) for row in self.items.values()) == 35, 'Runtime catalog/mode drift')
        self.allowed = set(methods.RUNTIME_COMMON + methods.RUNTIME_SUPPORTING)
        self.allowed.update(p for paths in self.methods.values() for p in paths)
        require(len(self.allowed) == 86, 'Incomplete business operational resource closure')
        self.allowed.update(p for entry in selected['auxiliary_entries'] for p in entry['resources'])
        self.business_manifests = {'implementation/skills/' + name + '/SKILL.md': name for name in self.methods}
        self.issues, self.virtual = {}, {}
        scan_runtime(self.cache)
        for row in selected['skills']:
            paths, edges = methods.closure(self, row['name'])
            require(paths == selected['resource_sets'][row['required_set']], 'Resource closure drift: ' + row['name'])
            require(digest(encoded({p: digest(self.read(p)) for p in paths})) == row['resource_map_sha256'],
                    'Resource closure hashes drift')
            require(len(edges) == 453 and all(e['target'] in self.allowed for e in edges if e['location'] != 'evaluation-only'),
                    'Unresolved required runtime read')

    def read(self, path):
        require(path in self.cache, 'Unselected canonical read: ' + path)
        return self.cache[path]


def tool_inputs():
    tools = {p: regular_read(ROOT / p) for p in (*BUILD_INPUTS, SELF)}
    require(all(digest(tools[p]) == sha for p, sha in BUILD_INPUTS.items()), 'Unreviewed packaging input drift')
    return tools


def descriptor(selected, tools):
    return dict(schema='consulting-studio/s-rebuild@1', selection=selected,
        generator_inputs={p: digest(data) for p, data in sorted(tools.items())},
        tooling_scope='Separate build-only source; not operational S. Distribution rights/export authority pending.',
        standing=STANDING)


def declared_version(path, data):
    if path.endswith('.json'):
        value = decode(data)
        return next((value[key] for key in ('version', 'contract_version', 'profile_version') if key in value), None)
    if path.endswith('.md'):
        text = data.decode()
        match = re.search(r'\b\d+\.\d+\.\d+\b', text if path.endswith('/SKILL.md') else text.splitlines()[0])
        return match.group() if match else None
    return None


def input_files(selected, canonical, tools):
    return {**{'canonical/' + p: data for p, data in canonical.items()}, **tools,
            DESCRIPTOR: encoded(descriptor(selected, tools)), 'REBUILD.md': INSTRUCTIONS}


def read_rebuild(root):
    info = decode(regular_read(Path(root) / DESCRIPTOR))
    check_selection(info['selection'])
    tools = tool_inputs()
    require(info == descriptor(info['selection'], tools), 'Rebuild descriptor/tooling drift')
    paths = {'canonical/' + row['path'] for row in info['selection']['files']} | set(tools) | {DESCRIPTOR, 'REBUILD.md'}
    files = read_exact_tree(root, paths)
    require(files['REBUILD.md'] == INSTRUCTIONS and all(files[p] == tools[p] for p in tools), 'Rebuild tooling/guidance drift')
    canonical = {row['path']: files['canonical/' + row['path']] for row in info['selection']['files']}
    return info['selection'], canonical


def full_links(files):
    links.check_links(files)
    def destination(origin, locator):
        links.destination(files, origin, locator)
        parts = urlsplit(locator.strip('<>'))
        if parts.scheme or parts.netloc or not parts.fragment:
            return
        path = posixpath.normpath(posixpath.join(posixpath.dirname(origin), unquote(parts.path))) if parts.path else origin
        if path.endswith('.json'):
            pointer = unquote(parts.fragment)
            require(pointer.startswith('/'), 'Unsupported JSON locator fragment: ' + locator)
            value = decode(files[path])
            for component in pointer[1:].split('/'):
                require(not re.search(r'~(?![01])', component), 'Invalid JSON pointer escape')
                key = component.replace('~1', '/').replace('~0', '~')
                if isinstance(value, list):
                    require(re.fullmatch(r'0|[1-9][0-9]*', key) and int(key) < len(value), 'Missing JSON pointer: ' + locator)
                    value = value[int(key)]
                else:
                    require(isinstance(value, dict) and key in value, 'Missing JSON pointer: ' + locator)
                    value = value[key]
    # Also validate declared JSON pointer fragments in ordinary links and JSON
    # locator fields. Existing validators already check Markdown heading anchors.
    def inspect(value, origin, pointer=''):
        if isinstance(value, dict):
            for key, member in value.items():
                if methods.json_locator(pointer, key) and isinstance(member, str):
                    destination(origin, member)
                else:
                    inspect(member, origin, pointer + '/' + key)
        elif isinstance(value, list):
            for index, member in enumerate(value):
                inspect(member, origin, pointer + '/' + str(index))
        elif isinstance(value, str):
            for pattern in (methods.LINK, methods.REFERENCE_LINK, methods.HTML_LINK):
                for match in pattern.finditer(value):
                    destination(origin, match.group(2))
    for path, data in files.items():
        if path.endswith('.md'):
            inspect(data.decode(), path)
        elif path.endswith('.json') and PurePosixPath(path).name != 'manifest.json':
            inspect(decode(data), path)
    # Existing package validation covers Markdown/HTML/JSON. Also close each
    # declared standalone-code read using the canonical adaptation record.
    for path, data in files.items():
        if path.endswith('/manifest.json') and path.startswith('skills/'):
            manifest = decode(data)
            base = posixpath.dirname(path)
            for resource in manifest['resources']:
                for adaptation in resource['adaptations']:
                    if adaptation['classification'] == 'bundled governing/resource read':
                        destination(base + '/' + resource['emitted_path'], adaptation['result'])



def assemble_auxiliary(source, item, rights, canonical, generators):
    """Generate an entry from canonical instructions; retain no editable method copy."""
    name = item['name']
    paths, edges = methods.runtime_entry_closure(source, item['resources'])
    require(paths == item['required_paths'] and edges == item['dependency_edges'], 'Auxiliary closure drift: ' + name)
    mapping = {p: methods.emitted_path(p, name).replace('/narrow-pilot-contract-', '/supported-input-contract-')
               .replace('/narrow-pilot-boundary-', '/supported-input-boundary-') for p in paths}
    require(mapping[item['entry']] == 'SKILL.md' and len(set(mapping.values())) == len(mapping),
            'Auxiliary entry/canonical mapping collision')
    files, resources, mapped = {}, [], []
    for path in paths:
        output = mapping[path]
        data, adaptations = methods.rewrite(source, path, output, mapping)
        files[output] = data
        row = dict(canonical_path=path, canonical_sha256=digest(canonical[path]), emitted_path=output,
                   emitted_sha256=digest(data), adaptations=adaptations, role='open auxiliary entry or governing resource')
        resources.append(row)
        mapped.append(dict(**row, output_path='skills/' + name + '/' + output,
            rights_profile=rights[path]['rights_profile'], declared_version=declared_version(path, canonical[path]),
            transformations=['deterministic local locator rewriting'] if adaptations else ['exact canonical bytes']))
    manifest = dict(schema='consulting-studio/s-auxiliary-entry@1', name=name, display_name=item['display_name'],
        entry_version=declared_version(item['entry'], canonical[item['entry']]), source_commit=source.commit,
        source_tree=source.tree, resources=resources, dependency_edges=edges, canonical_to_emitted=mapping,
        generator_inputs=generators, gates=dict(native_import='NOT_RUN', resource_readback='NOT_RUN',
            fresh_session_use='NOT_RUN', owner_acceptance='NOT_RUN'),
        standing=STANDING, files={p: digest(data) for p, data in sorted(files.items())})
    files['manifest.json'] = encoded(manifest)
    generated = dict(path='skills/' + name + '/manifest.json', role='generated auxiliary entry/resource inventory', inputs=paths)
    return files, mapped, generated

def build(selected, canonical, tools):
    require(set(tools) == set(BUILD_INPUTS) | {SELF} and
            all(digest(tools[p]) == sha for p, sha in BUILD_INPUTS.items()) and
            tools[SELF] == regular_read(ROOT / SELF), 'Unreviewed build input selection/bytes')
    source = SelectedRuntimeSource(selected, canonical)
    generators = {p: digest(data) for p, data in sorted(tools.items())}
    portable_path = 'implementation/plugin-distribution/plugin.json'
    portable = decode(tools[portable_path])
    config = dict(version=portable['version'], repository=selected['repository'], standing=STANDING)
    files, catalog, mapping, generated = {}, [], [], []
    rights = {row['path']: row for row in selected['files']}
    for name in source.methods:
        skill = methods.assemble_runtime(source, name, config, generators)
        links.check_links(skill)
        manifest = decode(skill['manifest.json'])
        require(set(manifest['files']) == set(skill) - {'manifest.json'} and
                all(digest(skill[p]) == sha for p, sha in manifest['files'].items()), 'Method manifest drift')
        catalog.append(dict(name=name, method_version=manifest['method_version'], modes=manifest['modes'],
            resources=len(manifest['resources']), manifest_sha256=digest(skill['manifest.json'])))
        for row in manifest['resources']:
            output = 'skills/' + name + '/' + row['emitted_path']
            transformations = ['deterministic local locator rewriting'] if row['adaptations'] else ['exact canonical bytes']
            if row['emitted_path'] == 'SKILL.md':
                transformations.append('insert explicit working-instructions read after canonical frontmatter')
            mapping.append(dict(**row, output_path=output, rights_profile=rights[row['canonical_path']]['rights_profile'],
                declared_version=declared_version(row['canonical_path'], canonical[row['canonical_path']]),
                transformations=transformations))
        generated.extend(dict(path='skills/' + name + '/' + p, role=role, inputs=sorted(source.allowed)) for p, role in (
            ('references/governing.md', 'generated common-instruction composition'),
            ('manifest.json', 'generated method/version/resource inventory')))
        files.update({'skills/' + name + '/' + p: data for p, data in skill.items()})
    predecessor = copy.deepcopy(portable)
    # The existing composer's historical predecessor label (0.1.3) is only a
    # structural input. This creates no upgrade, installed-state or approval receipt.
    predecessor['version'] = '0.1.3'
    del predecessor['extensions']['com.openai']['onboardingSkill']
    reference_map = dict(setup.REFERENCE_MAP)
    reference_map['../../../business-skills/installation-storage-lifecycle.md'] = (
        'skills/org-specialize/references/source/implementation/runtime/storage-lifecycle.md')
    setup_sources = {'implementation/plugin-setup/' + p: p for p in setup.SETUP_FILES}
    overlay, receipt = setup.compose({'plugin.json': encoded(predecessor), **files}, config['version'],
        setup={p: canonical[origin] for origin, p in setup_sources.items()}, reference_map=reference_map)
    require(decode(overlay['plugin.json']) == portable, 'Setup manifest composition drift')
    files.update(overlay)
    for item in selected['auxiliary_entries']:
        auxiliary, aux_mapping, aux_generated = assemble_auxiliary(source, item, rights, canonical, generators)
        files.update({'skills/' + item['name'] + '/' + p: data for p, data in auxiliary.items()})
        mapping.extend(aux_mapping)
        generated.append(aux_generated)
    files['plugin.json'] = tools[portable_path]
    legacy = {key: portable[key] for key in ('name', 'version', 'description', 'author', 'license')}
    legacy.update(interface=portable['extensions']['com.openai']['interface'], skills='./skills',
                  extensions={'com.openai': {'onboardingSkill': setup.ENTRY}})
    files['.codex-plugin/plugin.json'] = encoded(legacy)
    files['LOCAL-CANDIDATE.md'] = LIMITS
    for origin, output in {**setup_sources, 'LICENSE': 'LICENSE', 'NOTICE': 'NOTICE',
            'implementation/plugin-distribution/runtime-readme.md': 'README.md'}.items():
        if origin not in setup_sources:
            files[output] = canonical[origin]
        mapping.append(dict(canonical_path=origin, canonical_sha256=digest(canonical[origin]),
            output_path=output, emitted_path=output, emitted_sha256=digest(files[output]),
            rights_profile=rights[origin]['rights_profile'], role='S auxiliary or legal payload',
            declared_version=declared_version(origin, canonical[origin]),
            transformations=['Setup local locator composition'] if output == 'skills/setup/SKILL.md' else ['exact canonical bytes'],
            adaptations=receipt['reference_adaptations'] if output == 'skills/setup/SKILL.md' else []))
    generated.extend([
        dict(path='plugin.json', role='exact build-input plugin metadata; historical version label, no new release', inputs=[portable_path]),
        dict(path='.codex-plugin/plugin.json', role='generated portable compatibility metadata', inputs=[portable_path]),
        dict(path='LOCAL-CANDIDATE.md', role='generated self-install/check guidance and honest local limits', inputs=[SELF]),
    ])
    generated.append(dict(path='distribution.json', role='generated complete export evidence; hash external',
        inputs=['rebuild.json', *sorted(tools)]))
    for row in generated:
        row.update(rights='Derived inputs retain applicable grants; new metadata distribution rights/export pending',
                   notice_paths=['LICENSE', 'NOTICE'])
    # Each output is either a mapped canonical byte transformation or explicit
    # generated metadata. No independent editable method tree is retained in Git.
    check_paths(files)
    require({row['canonical_path'] for row in mapping} == set(canonical), 'Incomplete canonical-to-emitted mapping')
    mapped_outputs = {row['output_path'] for row in mapping}
    require(len(mapped_outputs) == len(mapping), 'Canonical-to-emitted collision')
    require(mapped_outputs.isdisjoint({r['path'] for r in generated}) and
            mapped_outputs | {r['path'] for r in generated if r['path'] != 'distribution.json'} == set(files),
            'Unclassified generated output')
    methods.check_runtime_instructions(files)
    scan_runtime(files)
    pack.manifest_checks(files, list(source.methods), config['version'], auxiliary=AUXILIARY_SKILLS)
    full_links(files)
    provenance = dict(schema='consulting-studio/s-export@1', offer='S', standing=STANDING,
        source_repository=selected['repository'], source_commit=source.commit, source_tree=source.tree,
        inventory_commit=selected['inventory_commit'], inventory_tree=selected['inventory_tree'],
        inventory_sha256=selected['inventory_sha256'], selection_sha256=SELECTION_SHA256,
        generator_inputs=generators, business_skills=27, modes=35, business_resources=73,
        resources_per_method=86, dependency_edges_per_method=453, canonical_files=len(canonical),
        export_version=EXPORT_VERSION, auxiliary_skills=list(AUXILIARY_SKILLS),
        auxiliary_entries=selected['auxiliary_entries'], helper_adapter_boundary=selected['helper_adapter_boundary'], methods=catalog, canonical_to_emitted=mapping,
        generated_files=generated,
        rights_profiles=selected['rights_profiles'], delivery_gates=selected['gates'],
        license_scope=dict(inherited_methods='Existing Apache-2.0 recipient grants remain usable; no proprietary relabelling',
            current_source='Exact inventory LICENSE/NOTICE bytes including prospective Part A and preserved Part B; no new S grant activated',
            tooling='Separate build-only inputs; rights/export remain pending', legacy_apache=selected['legacy_apache']),
        prerequisites=['Actually available authorized host tools for research, storage, rendering and inspection',
            'Permitted supplied evidence and exact applicable adopted customer rules/settings in their authorized home'],
        exclusions='Every unselected path denied; no GUI/MCP/server, fonts, dependencies, fixtures, adapters, private/live bindings or credentials',
        optional_provenance='Inventory/source Git pins are evidence only; excluded authoring material is not a required read',
        public_rebuild='Locally testable from the finite separate input ZIP without private constructor catalogs; public distribution UNAPPROVED',
        gates={p: 'NOT_RUN' for p in ('clean_install', 'native_execution', 'workspace_availability', 'wa_adoption', 'owner_acceptance')},
        files={p: dict(sha256=digest(data), bytes=len(data)) for p, data in sorted(files.items())})
    files['distribution.json'] = encoded(provenance)
    return files, provenance


def validate(data, expected):
    files = pack.unpack(data, expected)
    require(files == expected, 'Exact emitted S allowlist/source/composition drift')
    info = decode(files['distribution.json'])
    require(set(info['files']) == set(files) - {'distribution.json'}, 'Full emitted inventory drift')
    require(all(digest(files[p]) == row['sha256'] and len(files[p]) == row['bytes']
                for p, row in info['files'].items()), 'Emitted digest/size drift')
    require(all(value == 'NOT_RUN' for value in info['gates'].values()), 'Invented runtime acceptance')
    return info


def artifacts(selected, canonical, tools):
    files, info = build(selected, canonical, tools)
    candidate = pack.zip_bytes(files)
    validate(candidate, files)
    inputs = input_files(selected, canonical, tools)
    check_paths(inputs)
    rebuild = pack.zip_bytes(inputs)
    require(pack.unpack(rebuild, inputs) == inputs, 'Rebuild archive fidelity drift')
    outputs = {CANDIDATE: candidate, REBUILD: rebuild, 'distribution.json': files['distribution.json']}
    evidence = dict(schema='consulting-studio/s-export-evidence@1', standing=STANDING,
        inventory_commit=INVENTORY_COMMIT, inventory_sha256=INVENTORY_SHA256, selection_sha256=SELECTION_SHA256,
        source_commit=info['source_commit'], source_tree=info['source_tree'],
        counts={k: info[k] for k in ('business_skills', 'modes', 'business_resources', 'resources_per_method', 'canonical_files')},
        files={p: dict(sha256=digest(data), bytes=len(data)) for p, data in sorted(outputs.items())},
        rebuild_inputs={p: dict(sha256=digest(data), bytes=len(data),
            role='selected canonical source' if p.startswith('canonical/') else 'build-only tooling' if p in tools else 'generated rebuild metadata')
            for p, data in sorted(inputs.items())},
        delivery='BLOCKED', open_gates=[g['id'] for g in selected['gates'] if g['status'] != 'approved'])
    outputs['export-evidence.json'] = encoded(evidence)
    for name in (CANDIDATE, REBUILD):
        outputs[name + '.sha256'] = (digest(outputs[name]) + '  ' + name + '\n').encode()
    return outputs


def write_outputs(output, outputs):
    output = Path(output).absolute()
    require(not any(p.is_symlink() for p in (output, *output.parents)), 'Output/ancestor symlink')
    if output.exists():
        require(read_exact_tree(output, outputs) == outputs, 'Conflicting prior output; inspect before retry')
        return
    output.mkdir(parents=True)
    for path, data in outputs.items():
        (output / safe_path(path)).write_bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rebuild-from', type=Path, help='Finite extracted input snapshot; no Git access')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output', type=Path, help='Write LOCAL technical candidate and rebuild inputs')
    mode.add_argument('--check', type=Path, help='Validate exact artifact directory against canonical regeneration')
    mode.add_argument('--gate', action='store_true', help='Report the blocking delivery gates; never writes output')
    mode.add_argument('--verify', action='store_true', help='Validate the complete local candidate in memory; no output writes')
    args = parser.parse_args()
    selected, canonical = read_rebuild(args.rebuild_from) if args.rebuild_from else audit_checkout()
    tools = tool_inputs()
    outputs = artifacts(selected, canonical, tools)
    if args.check:
        require(read_exact_tree(args.check, outputs) == outputs, 'Artifact directory differs from complete canonical regeneration')
    if args.output:
        write_outputs(args.output, outputs)
    print(json.dumps(dict(standing=STANDING, skills=27, modes=35, business_resources=73, canonical_files=S_SOURCE_FILES,
        resources_per_method=86, candidate_sha256=digest(outputs[CANDIDATE]), rebuild_sha256=digest(outputs[REBUILD]),
        delivery='BLOCKED', open_gates=[g['id'] for g in selected['gates'] if g['status'] != 'approved']), sort_keys=True))
    return 1 if args.gate else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, TypeError, OSError) as error:
        sys.exit('FAIL: ' + str(error))
