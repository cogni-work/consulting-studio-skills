#!/usr/bin/env python3
"""Build individually importable source candidates from one pinned canonical tree.

Only tracked allowlisted common, supporting and 27 canonical method resources
are inputs. No installed state, private instance record or customer content is read.
"""
import argparse
import ast
import hashlib
import io
import json
import posixpath
import re
import subprocess
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CONSTRUCTOR = 'implementation/build-consulting-studio/'
COMMON = (
    'README.md', 'AGENTS.md', 'ARCHITECTURE.md', 'LICENSE', 'NOTICE',
    'docs/product/vision.md', 'docs/product/builder-handoff.md',
    'docs/product/acceptance.md', 'docs/product/open-questions.md',
    'docs/product/specification-maintenance.md', 'docs/product/deployment-service.md',
    'docs/architecture/journey.md', 'docs/architecture/business-objects.md',
    'docs/architecture/knowledge.md', 'docs/architecture/decisions.md',
    'docs/architecture/communication.md',
    'implementation/business-skills/architecture.md',
    'implementation/working-character/instructions.md',
    'implementation/contracts/entity-lineage.md',
    'implementation/contracts/entity_lineage.py',
    'implementation/workspace-bindings/architecture.md',
    'implementation/workspace-bindings/contract.md',
    'implementation/workspace-bindings/skill-contracts.json',
    'implementation/skills/workspace-bindings/SKILL.md',
    'implementation/business-skills/installation-storage-lifecycle.md',
    CONSTRUCTOR + 'references/native-acceptance.md',
)
# Supporting procedures are readable dependencies, never registered business skills.
# Keep a finite inventory: an unknown supporting read must fail closed.
SUPPORTING = (
    'implementation/skills/workspace-bindings/SKILL.md',
    'implementation/skills/workspace-bindings/references/provider-routes.md',
    'implementation/skills/workspace-bindings/references/record-format.md',
    'implementation/skills/workspace-bindings/scripts/resolve_binding.py',
)
INSTALLATION = tuple('implementation/business-skills/' + name for name in (
    'installation-storage-lifecycle.md', 'installation.md',
    'installation-record-template.md', 'installation-questionnaire.md',
    'installation_mapping.py', 'check_installation.py', 'README.md',
    'release.json', 'release.py', 'check_packages.py'))
CATALOGS = tuple(CONSTRUCTOR + 'references/' + name for name in (
    'skill-catalog.json', 'component-manifest.json', 'roadmap.json', 'scenario-coverage.json'))
# Canonical inline-link labels may wrap across lines; keep their exact bytes.
# Destinations retain the existing single-line syntax and closure rules.
LINK = re.compile(r'\[([^\]]*)\]\(([^)\n]+)\)')
REFERENCE_LINK = re.compile(
    r'(?m)^( {0,3}\[(?!\^)[^\]\n]+\]:[ \t]*(?:\n[ \t]*)?)(<[^>\n]+>|\S+)')
# The supported definition form above is deliberately finite. Definitions inside
# Markdown containers or indented blocks must not silently evade closure checks.
REFERENCE_MARKER = re.compile(
    r'(?m)^(?:[ \t]+|>[ \t]*|(?:[-+*]|[0-9]{1,9}[.)])[ \t]+)*'
    r'(\[(?!\^)[^\]\n]+\]:)')
HTML_LINK = re.compile(r'''(?i)(\b(?:href|src)\s*=\s*["'])([^"']+)(["'])''')
CODE = re.compile(r'(?<!`)`([^`\n]+)`(?!`)')
PATH_FIELDS = {'common_contract', 'semantic_contract', 'source_candidate',
               'contract_ref', 'compatibility_ref', 'coverage_ref'}
OPTIONAL_PREFIXES = (
    'implementation/runs/', 'implementation/fixtures/', 'implementation/tests/',
    'implementation/build-ledger/', 'implementation/native-preview/',
    'implementation/plugin/', 'implementation/agent/', 'implementation/working-character/',
    'implementation/workspace-bindings/evidence/',
    'tooling/', '.github/',
)
OPTIONAL_FILES = {'docs/provenance.md', 'docs/migration.md', 'docs/consolidation.md',
                  'docs/architecture/app-storage-and-pages.md',
                  'docs/architecture/work-sessions-proposal.md',
                  'implementation/embedded-ui/README.md',
                  'implementation/embedded-ui/work-sessions/result-lines.md',
                  'implementation/embedded-ui/work-sessions/original-chat-index-slice.md',
                  'implementation/README.md', 'implementation/working-character/README.md'}
EVALUATION_LOCATORS = {('implementation/skills/evidence-check/references/check-contract.md',
                       '../../fixtures/alder-harbor/evidence-check-v1/source-records.md#')}


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + '\n').encode()


def json_locator(pointer, key):
    return key in PATH_FIELDS or pointer + '/' + key == '/scenario_coverage/ref'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


class Source:
    """Complete authoring source for constructor and installation inventory tools."""
    def __init__(self, commit):
        self.commit = git('rev-parse', commit + '^{commit}').decode().strip()
        self.tree = git('rev-parse', self.commit + '^{tree}').decode().strip()
        self.paths = set(git('ls-tree', '-r', '--name-only', self.commit).decode().splitlines())
        self.cache = {}
        self.catalog = json.loads(self.read(CATALOGS[0]))
        self.components = json.loads(self.read(CATALOGS[1]))
        self.roadmap = json.loads(self.read(CATALOGS[2]))
        self.items = {i['name']: i for i in self.components['items']}
        self.issues = {i['issue']: i for i in self.roadmap['items']}
        self.virtual = {CONSTRUCTOR + f"references/contracts/{i['issue']}-{i['name']}.md": i
                        for i in self.roadmap['items']}
        names = [i['name'] for i in self.catalog['skills']]
        require(names == [i['name'] for i in self.components['items']], 'Skill identity/order drift')
        self.methods = {name: sorted(p for p in self.paths if p.startswith('implementation/skills/' + name + '/'))
                        for name in names}
        self.business_manifests = {'implementation/skills/' + name + '/SKILL.md': name for name in names}
        require(len(names) == 27 and sum(len(i['modes'] or [None]) for i in self.items.values()) == 35,
                '27-skill/35-mode coverage drift')
        require(sum(map(len, self.methods.values())) == 88, '88 business resource inventory drift')
        for name, paths in self.methods.items():
            require('implementation/skills/' + name + '/SKILL.md' in paths, 'Missing method manifest')
            require(all(p.endswith(('.md', '.json', '.py')) for p in paths), 'Unexpected method resource type')
        self.allowed = set(COMMON + CATALOGS + SUPPORTING + INSTALLATION) | set(self.virtual)
        self.allowed.update(p for paths in self.methods.values() for p in paths)
        # Authoring tools also follow maintained operational references.
        self.allowed.update(p for p in self.paths if p.startswith('implementation/runtime/'))

    def read(self, path):
        if path not in self.cache:
            if hasattr(self, 'virtual') and path in self.virtual:
                row = self.virtual[path]
                self.cache[path] = ('# ' + row['title'] + '\n\n' + row['contract']).encode()
            else:
                require(path in self.paths, 'Unread canonical dependency: ' + path)
                mode = git('ls-tree', self.commit, '--', path).decode().split()[0]
                require(mode in ('100644', '100755'), 'Canonical dependency is not a regular file: ' + path)
                self.cache[path] = git('show', self.commit + ':' + path)
        return self.cache[path]

    def resolve(self, origin, locator):
        parts = urlsplit(locator.strip('<>'))
        path = unquote(parts.path)
        prefix = '/cogni-work/consulting-studio/'
        if parts.netloc == 'github.com' and path.startswith(prefix):
            issue = re.fullmatch(prefix + r'issues/(\d+)', path)
            if issue and int(issue.group(1)) in self.issues:
                row = self.issues[int(issue.group(1))]
                path = CONSTRUCTOR + f"references/contracts/{row['issue']}-{row['name']}.md"
            elif path.startswith(prefix + 'blob/main/'):
                path = path.removeprefix(prefix + 'blob/main/')
            else:
                return None, parts.fragment
        elif parts.scheme or parts.netloc:
            return None, parts.fragment
        elif not path:
            return origin, parts.fragment
        elif path == 'README.md' and origin.startswith('implementation/business-skills/'):
            path = 'implementation/business-skills/README.md'
        elif path.startswith(('implementation/', 'docs/')) or path in ('README.md', 'AGENTS.md', 'ARCHITECTURE.md', 'LICENSE', 'NOTICE'):
            pass
        elif path.startswith('references/source/'):
            path = path.removeprefix('references/source/')
        elif path.startswith('references/contracts/'):
            path = CONSTRUCTOR + path
        elif path.startswith('references/') and origin in CATALOGS:
            path = CONSTRUCTOR + path
        else:
            path = posixpath.normpath(posixpath.join(posixpath.dirname(origin), path))
        historical = CONSTRUCTOR + 'references/source/'
        if path.startswith(historical):
            path = path.removeprefix(historical)
        # Imported issue contracts use the constructor's source/ namespace.
        if path.startswith(CONSTRUCTOR + 'references/source/'):
            path = path.removeprefix(CONSTRUCTOR + 'references/source/')
        require(not path.startswith('../') and not PurePosixPath(path).is_absolute(), 'Locator leaves canonical tree: ' + locator)
        return path, parts.fragment

    def classification(self, path):
        if path is None:
            return 'optional external reference'
        if path in self.allowed:
            return 'bundled governing/resource read'
        if path in OPTIONAL_FILES or path.startswith(OPTIONAL_PREFIXES) or path.startswith(CONSTRUCTOR):
            require(path in self.paths or any(p.startswith(path.rstrip('/') + '/') for p in self.paths),
                    'Missing optional provenance target: ' + path)
            return 'optional provenance; excluded adapter/build/host route'
        raise ValueError('Unclassified required dependency: ' + path)


RUNTIME_COMMON = (
    'LICENSE', 'NOTICE',
    'implementation/runtime/requirements.md',
    'implementation/runtime/entity-lineage.md',
    'implementation/runtime/storage-lifecycle.md',
    'implementation/runtime/method-catalog.json',
    'implementation/working-character/instructions.md',
    'implementation/workspace-bindings/architecture.md',
    'implementation/workspace-bindings/contract.md',
    'implementation/runtime/binding-catalog.json',
)
RUNTIME_SUPPORTING = tuple(p for p in SUPPORTING if p.endswith('.md'))
RUNTIME_REPLACEMENTS = {
    'ARCHITECTURE.md': ('implementation/runtime/requirements.md', 'working-context'),
    'docs/product/vision.md': ('implementation/runtime/requirements.md', 'working-context'),
    'docs/architecture/business-objects.md': ('implementation/runtime/requirements.md', 'business-records'),
    'docs/architecture/knowledge.md': ('implementation/runtime/requirements.md', 'evidence-and-knowledge'),
    'docs/architecture/communication.md': ('implementation/runtime/requirements.md', 'communication'),
    'docs/architecture/decisions.md': ('implementation/runtime/requirements.md', 'human-decisions'),
    'docs/architecture/journey.md': ('implementation/runtime/requirements.md', 'business-lifecycle'),
    'docs/product/acceptance.md': ('implementation/runtime/requirements.md', 'verification'),
    'docs/product/builder-handoff.md': ('implementation/runtime/requirements.md', 'verification'),
    'docs/product/open-questions.md': ('implementation/runtime/requirements.md', 'unresolved-inputs'),
    'docs/product/deployment-service.md': ('implementation/runtime/requirements.md', 'permissions-and-adoption'),
    'docs/product/specification-maintenance.md': ('implementation/runtime/requirements.md', 'method-and-settings-changes'),
    'implementation/contracts/entity-lineage.md': ('implementation/runtime/entity-lineage.md', ''),
    'implementation/workspace-bindings/skill-contracts.json': ('implementation/runtime/binding-catalog.json', ''),
    'implementation/business-skills/installation-storage-lifecycle.md': ('implementation/runtime/storage-lifecycle.md', ''),
}
RUNTIME_SECTION_REPLACEMENTS = {
    ('docs/architecture/knowledge.md', 'five-logical-information-areas'):
        ('implementation/runtime/storage-lifecycle.md', 'five-logical-information-areas'),
    ('docs/architecture/knowledge.md', 'creation-revision-and-closure-across-areas'):
        ('implementation/runtime/storage-lifecycle.md', 'creation-revision-and-closure-across-areas'),
    ('docs/architecture/knowledge.md', 'proposed-ordinary-examples'):
        ('implementation/runtime/storage-lifecycle.md', 'ordinary-location-examples'),
    ('docs/architecture/knowledge.md', 'reuse-revocation-and-exit'):
        ('implementation/runtime/storage-lifecycle.md', 'reuse-revocation-and-exit'),
    ('docs/architecture/knowledge.md', 'market-and-firm-domain-requirements'):
        ('implementation/runtime/requirements.md', 'selected-domain-requirements'),
    ('docs/architecture/knowledge.md', 'correction-and-dependent-uses'):
        ('implementation/runtime/entity-lineage.md', 'responsibility-and-authorized-correction'),
    ('docs/architecture/decisions.md', 'current-consumption-and-responsibility'):
        ('implementation/skills/sales-pursuit-event/references/time-authority-model-0.1.15.md', ''),
}

RUNTIME_DEVELOPMENT_PROSE = re.compile(
    r'\b(?:source candidate|source component|revalidation candidate|'
    r'Epic\s+\d+|(?-i:BOOTSTRAP)|Builder must supply|PR\s*#?\d+|'
    r'distribution adaptation|canonical procedure retained|'
    r'private draft of (?:the supplied complete|Consulting Studio)|'
    r'bounded synthetic supplied-source workflow)\b'
    r'|github\.com/cogni-work/consulting-studio/(?:issues|pull)/', re.I)


def check_runtime_instructions(files):
    """Reject known build prose in instructions, including nested metadata.

    Ordinary business issues, work milestones, quoted evidence and version/source
    identity fields are not classified as development history by their names.
    Legal records are preserved byte-for-byte and are not rewritten here.
    """
    for path, data in files.items():
        if path.endswith(('.md', '.json')):
            require(not RUNTIME_DEVELOPMENT_PROSE.search(data.decode()),
                    'Development prose in runtime instruction: ' + path)
            def check_references(value):
                if isinstance(value, dict):
                    for member in value.values():
                        check_references(member)
                elif isinstance(value, list):
                    for member in value:
                        check_references(member)
                elif isinstance(value, str):
                    supported = {m.start(1) + m.group(1).index('[')
                                 for m in REFERENCE_LINK.finditer(value)}
                    require(all(m.start(1) in supported for m in REFERENCE_MARKER.finditer(value)),
                            'Unsupported runtime reference definition; use a top-level definition or inline link: ' + path)
            check_references(json.loads(data) if path.endswith('.json') else data.decode())


class RuntimeSource(Source):
    """Operational method resources, separate from the complete authoring closure."""
    runtime = True

    def __init__(self, commit):
        super().__init__(commit)
        self.canonical_methods = self.methods
        self.methods = {name: [p for p in paths if p.endswith(('.md', '.json'))]
                        for name, paths in self.methods.items()}
        self.virtual = {}
        self.allowed = set(RUNTIME_COMMON + RUNTIME_SUPPORTING)
        self.allowed.update(p for paths in self.methods.values() for p in paths)
        runtime_catalog = json.loads(self.read('implementation/runtime/method-catalog.json'))
        require([row['name'] for row in runtime_catalog['skills']] == list(self.methods),
                'Runtime method identity/order drift')
        by_issue = {row['issue']: row['name'] for row in self.components['items']}
        for row in runtime_catalog['skills']:
            name = row['name']
            procedure = self.read('implementation/skills/' + name + '/SKILL.md').decode()
            version = re.search(r'\b\d+\.\d+\.\d+\b', procedure)
            require(version and version.group() == row['method_version'], 'Runtime method version drift: ' + name)
            require(row['modes'] == (self.items[name]['modes'] or [None]), 'Runtime mode drift: ' + name)
            item = self.items[name]
            dependencies = [dict(mode=entry['mode'],
                compatible_inputs_from=[by_issue[i] for i in entry['requires_components']])
                for entry in item['input_contracts']]
            require(row['input_dependencies'] == dependencies, 'Runtime input dependency drift: ' + name)
            decisions = [{key: dep[key] for key in ('gate', 'mode', 'actions') if key in dep}
                         for dep in item['dependencies'] if dep['kind'] == 'business_authority']
            require(row['human_decisions'] == decisions, 'Runtime human decision drift: ' + name)
        bindings = json.loads(self.read('implementation/runtime/binding-catalog.json'))
        expected = json.loads(self.read('implementation/workspace-bindings/skill-contracts.json'))
        expected['standing'] = bindings['standing']
        expected['semantic_contract'] = 'implementation/runtime/entity-lineage.md'
        for row in expected['skills']:
            row.pop('issue')
            if 'source_candidate' in row:
                row['contract_ref'] = row.pop('source_candidate')
        require(bindings == expected, 'Runtime binding role/permission contract drift')

    def resolve(self, origin, locator):
        path, fragment = super().resolve(origin, locator)
        parts = urlsplit(locator.strip('<>'))
        require(path is not None or parts.netloc != 'github.com'
                or not parts.path.startswith('/cogni-work/consulting-studio/'),
                'Unclassified repository instruction reference: ' + locator)
        if (path, fragment) in RUNTIME_SECTION_REPLACEMENTS:
            return RUNTIME_SECTION_REPLACEMENTS[(path, fragment)]
        if path in RUNTIME_REPLACEMENTS:
            path, section = RUNTIME_REPLACEMENTS[path]
            # A runtime reference names the maintained operational section, never
            # a historical numbered acceptance criterion or construction heading.
            fragment = section or fragment
        return path, fragment

    def classification(self, path):
        if path is None:
            return 'external source reference'
        require(path in self.allowed, 'Non-runtime dependency: ' + path)
        return 'bundled governing/resource read'


def locators(source, origin):
    """Enumerate Markdown plus declared JSON locators and standalone code paths."""
    data = source.read(origin)
    if origin.endswith('.py') or origin in ('LICENSE', 'NOTICE'):
        return []
    text = data.decode()
    if origin.endswith('.json'):
        result = []
        def walk(value, pointer=''):
            if isinstance(value, dict):
                for key, member in value.items():
                    address = pointer + '/' + key
                    if json_locator(pointer, key) and isinstance(member, str):
                        result.append((address, member))
                    elif key != 'contract' or origin != CATALOGS[2]:
                        # Only roadmap contracts have a separately walked derived file.
                        walk(member, address)
            elif isinstance(value, list):
                for i, member in enumerate(value):
                    walk(member, pointer + '/' + str(i))
            elif isinstance(value, str):
                result.extend((pointer + ':markdown', m.group(2)) for m in LINK.finditer(value))
                result.extend((pointer + ':markdown-reference', m.group(2)) for m in REFERENCE_LINK.finditer(value))
                result.extend((pointer + ':html', m.group(2)) for m in HTML_LINK.finditer(value))
        walk(json.loads(text))
        return result
    result = [('markdown', m.group(2)) for m in LINK.finditer(text)]
    result.extend(('markdown-reference', m.group(2)) for m in REFERENCE_LINK.finditer(text))
    result.extend(('html', m.group(2)) for m in HTML_LINK.finditer(text))
    for m in CODE.finditer(text):
        value = m.group(1)
        if (origin, value) in EVALUATION_LOCATORS:
            result.append(('evaluation-only', value))
            continue
        if re.fullmatch(r'(?:\.{1,2}/|references/|scripts/|implementation/|docs/)[\w./-]+(?:#[\w-]+)?', value):
            path, _ = source.resolve(origin, value)
            if path in source.allowed or path in source.paths:
                result.append(('code', value))
    return result


def closure(source, skill):
    base = RUNTIME_COMMON + RUNTIME_SUPPORTING if getattr(source, 'runtime', False) else COMMON + CATALOGS + SUPPORTING + INSTALLATION
    paths = set(base) | set(source.methods[skill])
    edges = []
    done = set()
    while paths - done:
        origin = sorted(paths - done)[0]
        done.add(origin)
        for location, locator in locators(source, origin):
            if location == 'evaluation-only':
                edges.append(dict(origin=origin, location=location, locator=locator, target=None,
                    fragment='', classification='preserved synthetic evaluation vocabulary; not a required resource read',
                    applies_to='Frozen correspondence example only; fixture namespace is not an offline read route'))
                continue
            target, fragment = source.resolve(origin, locator)
            kind = source.classification(target)
            edges.append(dict(origin=origin, location=location, locator=locator, target=target,
                              fragment=fragment, classification=kind,
                              applies_to='As required by the canonical read/context; no upstream invocation implied'))
            if kind == 'bundled governing/resource read':
                paths.add(target)
                if target in source.business_manifests:
                    paths.update(source.methods[source.business_manifests[target]])
                elif target == SUPPORTING[0]:
                    paths.update(RUNTIME_SUPPORTING if getattr(source, 'runtime', False) else SUPPORTING)
    return sorted(paths), edges



def runtime_entry_closure(source, entry_paths):
    """Close a finite auxiliary entry without registering it as a business method."""
    require(getattr(source, 'runtime', False), 'Auxiliary entries require runtime source')
    paths, done, edges = set(entry_paths), set(), []
    require(paths and paths <= source.allowed, 'Unselected auxiliary entry resource')
    while paths - done:
        origin = sorted(paths - done)[0]
        done.add(origin)
        for location, locator in locators(source, origin):
            require(location != 'evaluation-only', 'Auxiliary entry cannot depend on evaluation vocabulary')
            target, fragment = source.resolve(origin, locator)
            kind = source.classification(target)
            edges.append(dict(origin=origin, location=location, locator=locator, target=target,
                              fragment=fragment, classification=kind))
            if kind == 'bundled governing/resource read':
                paths.add(target)
                if target in source.business_manifests:
                    paths.update(source.methods[source.business_manifests[target]])
                elif target == SUPPORTING[0]:
                    paths.update(RUNTIME_SUPPORTING)
    return sorted(paths), edges

def emitted_path(path, skill):
    own = 'implementation/skills/' + skill + '/SKILL.md'
    if path == own:
        return 'SKILL.md'
    if path in ('LICENSE', 'NOTICE'):
        return path
    if '/references/contracts/' in path and path.startswith(CONSTRUCTOR):
        return path.removeprefix(CONSTRUCTOR)
    if path.startswith(CONSTRUCTOR) and path in CATALOGS:
        return path.removeprefix(CONSTRUCTOR)
    emitted = 'references/source/' + path
    if emitted.endswith('/SKILL.md'):
        emitted = emitted.removesuffix('SKILL.md') + 'procedure.md'
    return emitted


def rewrite(source, origin, output, mapping):
    adaptations = []
    def target(locator, location, context_origin=origin):
        path, fragment = source.resolve(context_origin, locator)
        kind = source.classification(path)
        if path in mapping:
            value = posixpath.relpath(mapping[path], posixpath.dirname(output))
            if fragment:
                value += '#' + fragment
        elif path is not None:
            value = 'https://github.com/cogni-work/consulting-studio/blob/' + source.commit + '/' + path
            if fragment:
                value += '#' + fragment
        else:
            value = locator
        adaptations.append(dict(location=location, original=locator, result=value, classification=kind,
                                canonical_origin=context_origin))
        return value, kind
    def markdown(text, context_origin=origin):
        def link(match):
            value, kind = target(match.group(2), 'markdown', context_origin)
            label = match.group(1)
            if kind.startswith('optional'):
                label += ' (optional provenance)'
            return '[' + label + '](' + value + ')'
        def code(match):
            locator = match.group(1)
            if (context_origin, locator) in EVALUATION_LOCATORS:
                adaptations.append(dict(location='evaluation-only', original=locator, result=locator,
                    classification='preserved synthetic evaluation vocabulary; not a required resource read',
                    canonical_origin=context_origin))
                return match.group(0)
            if re.fullmatch(r'(?:\.{1,2}/|references/|scripts/|implementation/|docs/)[\w./-]+(?:#[\w-]+)?', locator):
                path, _ = source.resolve(context_origin, locator)
                if path in mapping:
                    return '`' + target(locator, 'code', context_origin)[0] + '`'
                if path in source.paths:
                    value, _ = target(locator, 'code', context_origin)
                    return '[source path (optional provenance)](' + value + ')'
            return match.group(0)
        def reference(match):
            value, _ = target(match.group(2), 'markdown-reference', context_origin)
            if match.group(2).startswith('<'):
                value = '<' + value + '>'
            return match.group(1) + value
        def html(match):
            value, _ = target(match.group(2), 'html', context_origin)
            return match.group(1) + value + match.group(3)
        return CODE.sub(code, HTML_LINK.sub(html, REFERENCE_LINK.sub(reference, LINK.sub(link, text))))
    data = source.read(origin)
    if origin.endswith('.md'):
        return markdown(data.decode()).encode(), adaptations
    if origin.endswith('.json'):
        def walk(value, pointer=''):
            if isinstance(value, dict):
                return {key: target(member, pointer + '/' + key)[0]
                        if json_locator(pointer, key) and isinstance(member, str)
                        else markdown(member, CONSTRUCTOR + f"references/contracts/{value['issue']}-{value['name']}.md")
                        if key == 'contract' and origin == CATALOGS[2]
                        else walk(member, pointer + '/' + key) for key, member in value.items()}
            if isinstance(value, list):
                return [walk(member, pointer + '/' + str(i)) for i, member in enumerate(value)]
            if isinstance(value, str) and (LINK.search(value) or REFERENCE_LINK.search(value) or HTML_LINK.search(value)):
                return markdown(value)
            return value
        return encoded(walk(json.loads(data))), adaptations
    return data, adaptations


def runtime_dependencies(source, skill, paths=None):
    if paths is None:
        paths = closure(source, skill)[0]
    scripts = [p for p in source.methods[skill] if p.endswith('.py')]
    imports, references = set(), set()
    for path in scripts:
        tree = ast.parse(source.read(path).decode())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(i.name for i in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                references.update(re.findall(r'implementation/(?:fixtures|runs|tests)/[\w./-]+', node.value))
    result = dict(scripts=scripts, python_imports=sorted(imports),
                  excluded_repository_inputs=sorted(references),
                  script_execution='BLOCKED in standalone distribution' if scripts else 'No bundled execution engine',
                  scope='Canonical adapter bytes are inspectable reference code; they are not a native runtime/tool capability.',
                  settling_condition='Supply the exact compatible permitted inputs and an observed authorized host route; for adapter replay use its pinned repository checkout and original runtime.')
    result['supporting_reference_scripts'] = [p for p in paths if p.endswith('.py')
                                              and p in SUPPORTING + INSTALLATION]
    result['supporting_reference_scope'] = (
        'Workspace Librarian selection helper uses Python standard library and supplied private JSON; '
        'resolve its scripts path from the emitted supporting procedure folder, not the business skill root. '
        'It selects-needs-live-check only and performs no app operation or persistence. '
        'Installation/build helpers are inspectable reference code requiring their pinned repository layout/history. '
        'No native execution/tool capability, app access or approval is established by these files. '
        'Pinned installation/distribution documents preserve their historical 0.1.0 baseline; '
        'this bundle\'s identity is the current manifest and external installation/adoption evidence remains separate.')
    if scripts:
        result['requirements'] = ['Python 3 and the canonical adapter input contracts',
            'Original repository layout where inferred by parents[4]; fixtures/run receipts and upstream inputs are excluded',
            'Exact permitted current source/artifact/settings reads; no method grants connectors or business authority']
    else:
        result['requirements'] = ['Permitted supplied inputs can support independent unretained work',
            'Discovery, research, storage, readback and navigation need their applicable available authorized tools']
    if skill == 'publishing-render':
        result['requirements'] += ['Git repository/history',
            'Fixture build_report.py, build_deck.mjs, inputs.json and exact #46/source receipts',
            'Configured Python/document libraries and Node/presentation modules',
            'LibreOffice (soffice), Poppler pdftoppm/pdftotext/pdfinfo; Chromium where required by the selected route',
            'CODEX_PRIMARY_RUNTIME_PYTHON, CODEX_PRIMARY_RUNTIME_NODE, CODEX_PRIMARY_RUNTIME_NODE_MODULES and applicable runtime paths',
            '/opt/codex/skills/builtins/documents and /opt/codex/skills/builtins/presentations']
    if skill == 'publishing-inspect':
        result['requirements'] += ['Git repository/history; pypdf (pinned original tests: 6.19.0)',
            'Poppler pdftotext/pdftoppm; fixture inputs and exact artifact/source/run/interface receipts',
            'Digest-bound actual author pixel observations; extraction alone is not visual inspection']
    if skill == 'my-improvements':
        result['requirements'] += ['Sibling proposal_format.py (bundled)',
            'Actual Git repository with inspectable baseline commit/tree/document objects']
    return result


def assemble(source, skill, config, generator_inputs):
    if getattr(source, 'runtime', False):
        return assemble_runtime(source, skill, config, generator_inputs)
    require(skill in source.items, 'Unknown business skill: ' + skill)
    paths, edges = closure(source, skill)
    mapping = {path: emitted_path(path, skill) for path in paths}
    require(len(set(mapping.values())) == len(mapping), 'Canonical-to-emitted collision')
    files, resources = {}, []
    for path in paths:
        output = mapping[path]
        data, adaptations = rewrite(source, path, output, mapping)
        files[output] = data
        row = dict(canonical_path=path, canonical_sha256=digest(source.read(path)),
                   emitted_path=output, emitted_sha256=digest(data), adaptations=adaptations,
                   role='own method resource' if path in source.methods[skill] else
                        'supporting procedure/resource' if path in SUPPORTING else
                        'installation lifecycle resource' if path in INSTALLATION else 'governing/upstream resource')
        if path.endswith('.json'):
            obj = json.loads(source.read(path))
            row['declared_version'] = next((obj[key] for key in ('version', 'contract_version', 'profile_version') if key in obj), None)
        elif path.endswith('.md'):
            marker = re.search(r'\d+\.\d+\.\d+', source.read(path).decode().splitlines()[0])
            if path.endswith('/SKILL.md'):
                marker = re.search(r'\b\d+\.\d+\.\d+\b', source.read(path).decode())
            row['declared_version'] = marker.group() if marker else None
        else:
            row['declared_version'] = None
        if path in source.virtual:
            row['derived_from'] = dict(path=CATALOGS[2], sha256=digest(source.read(CATALOGS[2])),
                                       issue=source.virtual[path]['issue'], transformation='title and exact contract text')
        resources.append(row)
    procedure = source.read('implementation/skills/' + skill + '/SKILL.md').decode()
    version = re.search(r'\b\d+\.\d+\.\d+\b', procedure)
    require(version, 'Unversioned canonical procedure: ' + skill)
    modes = source.items[skill]['modes'] or [None]
    runtime = runtime_dependencies(source, skill, paths)
    governing = ('# Governing composition\n\n'
        'Use this individual method directly or as the workspace agent\'s consumer at the same pinned method/resource versions. '
        'Compatible supplied inputs do not require prior skill invocation.\n\n'
        'Read applicable requirements and the current working character through the local resources below. '
        'Distribution architecture extends the common communication/evidence/authority rules to direct use of all 27 methods; '
        'the preserved character source originally names four WA methods. This is an explicit composition adaptation, not a canonical source rewrite.\n\n')
    for path in COMMON:
        if path.endswith('.md'):
            governing += '- [' + path + '](' + posixpath.relpath(mapping[path], 'references') + ')\n'
    governing += ('\nRead the [dependency and runtime inventory](../manifest.json) for exact resources, mode identity and adaptation limits. '
        'Canonical Python adapters are reference code with excluded fixtures/runtimes; no script execution is claimed. '
        'Use an actually available authorized production route before claiming rendering/inspection.\n\n'
        'Customer policy, domain/method/design settings, private/client evidence and live bindings remain external authorized inputs. '
        'Adopt exact separate adaptation versions/digests and compatible core identity deliberately; unread/conflicting required references block the affected lane. '
        'Preserve additions, notes/dissent, wiki and issued work. Method availability, enablement, connectors, direct use, WA consumption, independent review and owner acceptance remain separate gates.\n')
    governing += ('\nFor requested home setup or lifecycle work, apply the bundled Workspace Librarian procedure and storage guide. '
        'Reuse compatible homes; prepare the concrete approval proposal, then perform only authorized supported operations with home and mapping readback. '
        'Its selection helper is inspectable reference code, not a bundled native tool or evidence of access. '
        'An existing valid mapping requires no mandatory Librarian invocation.\n')
    files['references/governing.md'] = governing.encode()
    # Keep the canonical frontmatter and procedure; add only explicit composition.
    entry = files['SKILL.md'].decode()
    boundary = entry.find('\n---\n', 4)
    require(entry.startswith('---\n') and boundary >= 0, 'Missing canonical skill frontmatter')
    insertion = boundary + len('\n---\n')
    entry = entry[:insertion] + ('\nRead [governing composition](references/governing.md) before applying this method. '
        'Use the local required resources and exact inventory; native operations and customer adaptation adoption remain separate.\n') + entry[insertion:]
    files['SKILL.md'] = entry.encode()
    next(r for r in resources if r['emitted_path'] == 'SKILL.md')['emitted_sha256'] = digest(files['SKILL.md'])
    gates = {name: 'NOT_RUN' for name in ('native_import', 'resource_readback', 'workspace_availability',
        'per_user_enablement', 'direct_use', 'wa_consumption', 'update_rollback', 'independent_review',
        'owner_acceptance', 'all_standard_component_modes')}
    manifest = dict(schema_version=1, name=skill, issue=source.items[skill]['issue'],
        bundle_version=config['version'], method_version=version.group(), modes=modes,
        source_repository=config['repository'], source_commit=source.commit, source_tree=source.tree,
        generator_inputs=generator_inputs, canonical_to_emitted=mapping,
        resources=resources, dependency_edges=edges, runtime_dependencies=runtime,
        core_adaptation_compatibility=dict(core_commit=source.commit, core_tree=source.tree,
            customer_adaptations='EXTERNAL; no customer material packaged or adopted',
            adoption='Exact separate source home/version/digest/scope and current owner adoption required',
            conflict='Block affected use; preserve customer additions and issued work',
            updates='Explicit old/new comparison, affected rechecks and adoption; no automatic propagation'),
        composition_adaptations=['Canonical frontmatter/procedure retained; explicit local governing reads added',
            'Common character composed across direct and WA use under approved A52/B24 architecture',
            'Required local/JSON/bare locators rewritten; upstream manifests emitted as procedure resources',
            'Excluded historical/fixture/build routes pinned and labeled optional provenance; adapter execution blocked'],
        gates=gates, standing=config['standing'],
        files={p: digest(data) for p, data in sorted(files.items())})
    files['manifest.json'] = encoded(manifest)
    return files


def assemble_runtime(source, skill, config, generator_inputs):
    require(skill in source.items, 'Unknown business skill: ' + skill)
    paths, edges = closure(source, skill)
    mapping = {path: emitted_path(path, skill).replace('/narrow-pilot-contract-', '/supported-input-contract-')
               .replace('/narrow-pilot-boundary-', '/supported-input-boundary-') for path in paths}
    require(len(set(mapping.values())) == len(mapping), 'Canonical-to-emitted collision')
    files, resources = {}, []
    for path in paths:
        output = mapping[path]
        check_runtime_instructions({path: source.read(path)})
        data, adaptations = rewrite(source, path, output, mapping)
        files[output] = data
        resources.append(dict(canonical_path=path, canonical_sha256=digest(source.read(path)),
            emitted_path=output, emitted_sha256=digest(data), adaptations=adaptations,
            role='method' if path in source.methods[skill] else 'supporting procedure' if path in RUNTIME_SUPPORTING else 'common instruction'))
    procedure = source.read('implementation/skills/' + skill + '/SKILL.md').decode()
    version = re.search(r'\b\d+\.\d+\.\d+\b', procedure)
    require(version, 'Unversioned canonical procedure: ' + skill)
    governing = ('# Working instructions\n\n'
        'Apply this method directly or within the workspace agent using the same selected method and resource versions. '
        'Compatible supplied inputs do not require another skill to have run.\n\n'
        'Read and apply the common working instructions and the domain requirements selected for this task. '
        'Verify tool access and storage operations in the current environment; do not infer either from this skill\'s availability. '
        'An unread required instruction blocks only its dependent operation; continue useful permitted supplied-evidence work.\n\n')
    for path in RUNTIME_COMMON:
        if path.endswith(('.md', '.json')):
            governing += '- [' + path.rsplit('/', 1)[-1] + '](' + posixpath.relpath(mapping[path], 'references') + ')\n'
    governing += ('\nUse the bundled Workspace Librarian procedure and lifecycle guide when a location needs attention. '
        'Reuse a valid current mapping directly; a mandatory setup step is unnecessary. '
        'Prepare exact proposed effects, reuse specific authority, and perform only supported authorized operations. '
        'Verify home content and mapping persistence through separate readback.\n\n'
        'Keep client/firm policy, selected domain requirements, adaptations, private evidence and live locations in their authorized homes. '
        'Apply exact adopted versions and preserve human originals, notes, dissent, issued work and confidential boundaries. '
        'Keep preparation, saving, review, adoption, release and acceptance distinct.\n')
    files['references/governing.md'] = governing.encode()
    entry = files['SKILL.md'].decode()
    boundary = entry.find('\n---\n', 4)
    require(entry.startswith('---\n') and boundary >= 0, 'Missing canonical skill frontmatter')
    insertion = boundary + len('\n---\n')
    files['SKILL.md'] = (entry[:insertion] + '\nRead [working instructions](references/governing.md) before applying this method.\n' + entry[insertion:]).encode()
    next(r for r in resources if r['emitted_path'] == 'SKILL.md')['emitted_sha256'] = digest(files['SKILL.md'])
    modes = source.items[skill]['modes'] or [None]
    gates = {name: 'NOT_RUN' for name in ('native_import', 'resource_readback', 'workspace_availability',
        'per_user_enablement', 'direct_use', 'wa_consumption', 'update_rollback', 'independent_review',
        'owner_acceptance', 'all_standard_component_modes')}
    manifest = dict(schema_version=2, name=skill, bundle_version=config['version'], method_version=version.group(), modes=modes,
        source_repository=config['repository'], source_commit=source.commit, source_tree=source.tree,
        generator_inputs=generator_inputs, canonical_to_emitted=mapping, resources=resources, dependency_edges=edges,
        runtime_dependencies=dict(requirements=['Use only actually available authorized sources and tools',
            'Read exact selected domain, policy, method and settings versions',
            'Verify saves, mapping persistence and intended-reader navigation through their actual supported routes']),
        core_adaptation_compatibility=dict(core_commit=source.commit, core_tree=source.tree,
            customer_adaptations='External exact adopted versions and scope required',
            adoption='Current owner adoption required', conflict='Block affected use; preserve additions and issued work',
            updates='Compare versions, recheck affected work and obtain applicable adoption'),
        gates=gates, standing=config['standing'], files={p: digest(data) for p, data in sorted(files.items())})
    files['manifest.json'] = encoded(manifest)
    return files


def archive_bytes(skill, files):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, data in sorted(files.items()):
            info = zipfile.ZipInfo(skill + '/' + path, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, data)
    return stream.getvalue()


def build(source, config, generator_inputs, skills=None):
    names = [i['name'] for i in source.catalog['skills']]
    if skills is not None:
        require(set(skills) <= set(names) and len(set(skills)) == len(skills), 'Invalid selected identities')
        names = [name for name in names if name in skills]
    archives, rows = {}, []
    for skill in names:
        files = assemble(source, skill, config, generator_inputs)
        data = archive_bytes(skill, files)
        name = skill + '-' + config['version'] + '.zip'
        archives[name] = data
        manifest = json.loads(files['manifest.json'])
        row = dict(name=skill, modes=manifest['modes'],
            method_version=manifest['method_version'], bundle_version=config['version'],
            archive=name, archive_sha256=digest(data), manifest_sha256=digest(files['manifest.json']),
            source_commit=source.commit, source_tree=source.tree,
            procedure_source_sha256=digest(source.read('implementation/skills/' + skill + '/SKILL.md')),
            procedure_emitted_sha256=digest(files['SKILL.md']), resource_count=len(manifest['resources']),
            own_business_resources=len(source.methods[skill]),
            core_adaptation_compatibility=manifest['core_adaptation_compatibility'],
            runtime_dependencies=manifest['runtime_dependencies'], gates=manifest['gates'])
        if 'issue' in manifest:
            row['issue'] = manifest['issue']
        rows.append(row)
    inventory = dict(schema_version=1, version=config['version'], source_commit=source.commit,
        source_tree=source.tree, generator_inputs=generator_inputs, skills=len(rows),
        modes=sum(len(row['modes']) for row in rows),
        business_resources=sum(row['own_business_resources'] for row in rows), items=rows,
        standing=config['standing'])
    if not getattr(source, 'runtime', False):
        inventory['constructor'] = 'Separate preserved 0.7.14; not rebuilt or imported'
    return archives, inventory


def inputs():
    return {path: digest((ROOT / path).read_bytes()) for path in (
        'implementation/business-skills/release.json', 'implementation/business-skills/release.py',
        'implementation/business-skills/check_packages.py')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--skills', nargs='+', help='Bounded closure demonstration; default all 27')
    args = parser.parse_args()
    config = json.loads((HERE / 'release.json').read_bytes())
    source = RuntimeSource(config['core_commit'])
    archives, inventory = build(source, config, inputs(), args.skills)
    # Validation precedes any output write; a conflicting existing output blocks.
    from check_packages import validate_inventory
    validate_inventory(archives, inventory, source)
    for path in (args.output.absolute(), *args.output.absolute().parents):
        require(not path.is_symlink(), 'Output directory/ancestor symlink: ' + str(path))
    args.output.mkdir(parents=True, exist_ok=True)
    outputs = {**archives, 'inventory.json': encoded(inventory)}
    outputs.update({p + '.sha256': (digest(data) + '  ' + p + '\n').encode() for p, data in archives.items()})
    for path, data in outputs.items():
        destination = args.output / path
        require(not destination.is_symlink() and (not destination.exists() or destination.read_bytes() == data),
                'Conflicting prior artifact; inspect before retry: ' + str(destination))
    for path, data in outputs.items():
        (args.output / path).write_bytes(data)
    print(json.dumps(dict(output=str(args.output), skills=inventory['skills'], modes=inventory['modes'],
        business_resources=inventory['business_resources'], inventory_sha256=digest(outputs['inventory.json']),
        native_import='NOT_RUN'), sort_keys=True))


if __name__ == '__main__':
    main()
