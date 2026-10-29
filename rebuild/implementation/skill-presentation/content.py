"""Finish and check delivered skill content; package evidence stays outside skills."""
import hashlib
import html
import json
import posixpath
import re
import unicodedata
from pathlib import PurePosixPath


SCHEMA = 'consulting-studio/skill-presentation@1'
KNOWN_NOTICES = (
    'Consulting Studio modification, 2026-10-27: local resource locators were packaged; '
    'an explicit working-instruction read was added where applicable. '
    'Exact source identities and changes are recorded in the accompanying manifests.',
    'Consulting Studio packaging modification, 2026-10-28: local resource locators '
    'and explicit governing reads; canonical source and emitted hashes in distribution.json. '
    'Existing license rights retained; current exact release approval pending.',
    'Consulting Studio packaging modification, 2026-10-28: local resource locators '
    'and explicit governing reads; exact canonical and emitted hashes retained. '
    'Prior Apache/NOTICE copies retained; approval of the current delta remains PENDING.',
    'Consulting Studio packaging modification, 2026-10-29: local resource locators '
    'and explicit governing reads; exact canonical and emitted hashes retained in distribution.json. '
    'S1.2.1 public release continues the existing Apache-2.0 S terms; recipient grants retained.',
)
# Match package and M layouts, never the external evidence homes. The caller
# supplies delivered package payloads, not the separate canonical/rebuild inputs.
SKILL_PATH = re.compile(r'^(?P<parent>(?:[^/]+/)?)skills/(?P<skill>[^/]+)/(?P<relative>.+)$')
EXTERNAL_PARENTS = {'metadata/', 'legal/', 'canonical/', 'provenance/', 'rebuild/'}
PROHIBITED_KEYS = frozenset((
    'distributionmodificationnotice', 'generatorinputs', 'sourcerepository',
    'sourcecommit', 'sourcetree', 'canonicalpath', 'canonicalsha256', 'emittedsha256',
    'buildorigin', 'buildprovenance', 'buildhistory', 'packaginghistory',
    'packagingprovenance', 'packagingmodification', 'sourceorigin', 'generatedfrom',
    'packagedfrom', 'breadcrumbs', 'breadcrumb', 'distributionadaptations',
))
PROSE_RULES = (
    ('injected build marker', re.compile(r'\bbuild[\s-]+injected\b', re.I)),
    ('generated file marker', re.compile(
        r'\b(?:auto[\s-]*generated|generated[\s-]+file)\b|\bdo not edit[^\n]{0,80}\bgenerated\b', re.I)),
    ('packaging modification commentary', re.compile(
        r'\bconsulting\s+studio\s+(?:packaging\s+)?modification\b', re.I)),
    ('build or packaging provenance label', re.compile(
        r'\b(?:build|packaging)[\s-]+(?:origin|provenance|history|breadcrumbs?|meta[\s-]*comments?)\b', re.I)),
    ('source origin label', re.compile(
        r'\b(?:source|canonical)[\s-]+(?:origin|breadcrumb|provenance)\s*[:=]', re.I)),
    ('generated origin prose', re.compile(
        r'\b(?:generated|packaged|derived)\s+(?:by|from)\s+(?:the\s+)?'
        r'(?:build\b|packag|canonical\b|source\b|repository\b|commit\b|implementation/|cogni-work\b|https?://)', re.I)),
    ('optional source breadcrumb', re.compile(r'\boptional[\s-]+provenance\b', re.I)),
    ('repository history breadcrumb', re.compile(
        r'github\.com/cogni-work/consulting-studio/(?:issues|pull|commit|tree|blob)/', re.I)),
    ('origin path label', re.compile(
        r'(?m)^\s*(?:[-#>]\s*)*(?:source|origin|canonical source)\s*[:=]\s*'
        r'(?:`?(?:implementation|canonical)/|`?[0-9a-f]{40}\b|https?://github\.com/cogni-work/)', re.I)),
)
LABEL_LINE = re.compile(r'(?m)^(?P<prefix>\s*display_name\s*:\s*)(?P<value>[^\n]+)$')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()


def _json(data, path):
    def pairs(rows):
        result = {}
        for key, value in rows:
            require(key not in result, 'Duplicate JSON key in skill content: ' + path)
            result[key] = value
        return result
    try:
        return json.loads(data, object_pairs_hook=pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError('Invalid skill JSON: ' + path) from error


def _skill_path(path):
    match = SKILL_PATH.fullmatch(path)
    if match and match['parent'] not in EXTERNAL_PARENTS:
        return match['parent'], match['skill'], match['relative']
    return None


def _scalar(value):
    value = value.strip()
    if value.startswith('"'):
        result = json.loads(value)
    elif value.startswith("'") and value.endswith("'"):
        result = value[1:-1].replace("''", "'")
    else:
        result = value
    require(isinstance(result, str) and bool(result), 'Expected a nonempty scalar')
    return result


def _frontmatter(data, path):
    text = data.decode('utf-8')
    require(text.startswith('---\n') and '\n---\n' in text[4:], 'Missing skill frontmatter: ' + path)
    front = text.split('\n---\n', 1)[0][4:]
    names = re.findall(r'(?m)^name:\s*([^\n]+)$', front)
    require(len(names) == 1, 'Expected one technical skill name: ' + path)
    name = _scalar(names[0])
    require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) is not None,
            'Unsupported technical skill name: ' + path)
    require(re.search(r'(?m)^description:\s*\S.+$', front) is not None,
            'Missing useful skill description: ' + path)
    return name, front


def _normalized(text):
    # Decode standard alternate representations before the finite rules. This is
    # a defined regression boundary, not a natural-language completeness claim.
    text = unicodedata.normalize('NFKC', html.unescape(text))
    text = re.sub(r'[\u200b-\u200f\u2060\ufeff]', '', text)
    return re.sub(r'[`*_]', ' ', text)


def _key(value):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKC', value).casefold())


def _scan_text(text, path):
    text = _normalized(text)
    for label, rule in PROSE_RULES:
        require(rule.search(text) is None, 'Prohibited ' + label + ' in skill content: ' + path)
    for match in re.finditer(r'(?m)^\s*(?:[-#>]\s*)*([^\n:=]{1,80})\s*[:=]', text):
        require(_key(match[1]) not in PROHIBITED_KEYS,
                'Prohibited packaging/source key in skill content: ' + path + ': ' + match[1].strip())


def _scan_json(value, path):
    if isinstance(value, dict):
        for key, member in value.items():
            require(_key(key) not in PROHIBITED_KEYS,
                    'Prohibited packaging/source key in skill content: ' + path + ': ' + key)
            _scan_json(member, path)
    elif isinstance(value, list):
        for member in value:
            _scan_json(member, path)
    elif isinstance(value, str):
        _scan_text(value, path)


def _names(data, path):
    text = data.decode('utf-8')
    return [_scalar(match['value']) for match in LABEL_LINE.finditer(text)]


def validate(files):
    """Reject defined packaging-origin classes throughout every delivered skill.

    Functional relative resource links, source/version/passage business evidence,
    human notes and unrelated meaningful comments remain permitted. No legal
    compliance or host registration assertion follows from this content check.
    """
    skill_files = {path: parts for path in files if (parts := _skill_path(path))}
    require(bool(skill_files), 'No delivered skill content to validate')
    entries, covered = {}, {}
    for path, (parent, skill, relative) in skill_files.items():
        require(isinstance(files[path], bytes), 'Expected skill bytes: ' + path)
        try:
            text = files[path].decode('utf-8')
        except UnicodeDecodeError as error:
            raise ValueError('Non-UTF-8 skill content is not covered: ' + path) from error
        require('\x00' not in text, 'Binary skill content is not covered: ' + path)
        require(relative != 'manifest.json' and PurePosixPath(relative).name not in ('LICENSE', 'NOTICE'),
                'Package evidence must be outside the skills tree: ' + path)
        _scan_text(text, path)
        if path.endswith('.json'):
            _scan_json(_json(files[path], path), path)
        covered.setdefault((parent, skill), []).append(path)
        if relative == 'SKILL.md':
            name, front = _frontmatter(files[path], path)
            require(name == skill, 'Skill technical name/directory mismatch: ' + path)
            labels = _names(front.encode(), path)
            require(all(label == name for label in labels), 'Skill display_name differs from name: ' + path)
            entries[(parent, skill)] = dict(name=name, path=path, labels=[dict(path=path, value=v) for v in labels])
    require(set(covered) == set(entries), 'Skill files have no actual root SKILL.md: ' + repr(sorted(set(covered) - set(entries))))
    for key, entry in entries.items():
        parent, skill = key
        interface = parent + 'skills/' + skill + '/agents/openai.yaml'
        if interface in files:
            labels = _names(files[interface], interface)
            require(len(labels) == 1, 'Expected one actual interface display_name: ' + interface)
            require(labels[0] == skill, 'Skill display_name differs from name: ' + interface)
            entry['labels'].append(dict(path=interface, value=labels[0]))
        metadata = parent + 'metadata/skills/' + skill + '/manifest.json'
        if metadata in files:
            manifest = _json(files[metadata], metadata)
            require(manifest.get('name') == skill, 'External skill manifest name mismatch: ' + metadata)
            if 'display_name' in manifest:
                require(manifest['display_name'] == skill, 'Skill display_name differs from name: ' + metadata)
                entry['labels'].append(dict(path=metadata, value=manifest['display_name']))
    rows = [dict(technical_name=entry['name'], entry_path=entry['path'],
                 effective_display_name=entry['name'], explicit_display_names=entry['labels'],
                 files_scanned=len(covered[key])) for key, entry in sorted(entries.items())]
    return dict(schema=SCHEMA, status='PASS', skill_count=len(rows), files_scanned=len(skill_files),
                bytes_scanned=sum(len(files[path]) for path in skill_files), entries=rows,
                limit='Defined prohibited packaging-origin classes; no claim to detect every possible natural-language paraphrase')


def _strip_json_notices(value, path, pointer, actions):
    if isinstance(value, dict):
        result = {}
        for key, member in value.items():
            at = pointer + '/' + key.replace('~', '~0').replace('/', '~1')
            if key == 'distribution_modification_notice':
                require(member in KNOWN_NOTICES, 'Unknown packaging notice requires source correction: ' + path + at)
                actions.append(dict(action='remove_exact_generated_json_notice', path=path, pointer=at, notice=member))
            else:
                result[key] = _strip_json_notices(member, path, at, actions)
        return result
    if isinstance(value, list):
        return [_strip_json_notices(member, path, pointer + '/' + str(i), actions) for i, member in enumerate(value)]
    return value


def _inventory(files):
    return {path: dict(sha256=digest(data), bytes=len(data)) for path, data in sorted(files.items())}


def finalize(files, *, profile):
    """Apply only enumerated presentation corrections, then reject other defects.

    The returned evidence belongs outside the skills tree. It records the exact
    removed generated notes, original hashes, relocations, clean hashes and scope.
    Caller rebuilds the outer distribution/archive inventories from returned bytes.
    """
    require(profile in ('S', 'App', 'M'), 'Expected an explicit S, App or M profile')
    result, actions, relocations, manifests = dict(files), [], {}, {}
    for path, data in sorted(files.items()):
        parts = _skill_path(path)
        if not parts:
            continue
        parent, skill, relative = parts
        target = None
        if relative == 'manifest.json':
            target = parent + 'metadata/skills/' + skill + '/manifest.json'
            manifests[path] = _json(data, path)
        elif PurePosixPath(relative).name in ('LICENSE', 'NOTICE'):
            target = parent + 'legal/skills/' + skill + '/' + relative
        if target:
            require(target not in result, 'External evidence relocation collision: ' + target)
            relocations[path] = target
            result[target] = result.pop(path)
            actions.append(dict(action='relocate_exact_package_record', path=path, output_path=target,
                                sha256=digest(data), bytes=len(data)))
            continue
        changed = data
        for notice in KNOWN_NOTICES:
            block = ('\n<!-- ' + notice + ' -->\n').encode()
            count = changed.count(block)
            if count:
                changed = changed.replace(block, b'')
                actions.append(dict(action='remove_exact_generated_comment', path=path, occurrences=count, notice=notice))
        if path.endswith('.json'):
            before_count = len(actions)
            value = _strip_json_notices(_json(changed, path), path, '', actions)
            if len(actions) != before_count:
                changed = encoded(value)
        if relative == 'SKILL.md' or relative == 'agents/openai.yaml':
            entry = parent + 'skills/' + skill + '/SKILL.md'
            name, _ = _frontmatter(files[entry], entry)
            text = changed.decode('utf-8')
            if relative == 'SKILL.md':
                boundary = text.index('\n---\n', 4)
                label_area, rest = text[:boundary], text[boundary:]
            else:
                label_area, rest = text, ''
            old = _names(label_area.encode(), path)
            if any(label != name for label in old):
                label_area = LABEL_LINE.sub(lambda match: match['prefix'] + json.dumps(name), label_area)
                changed = (label_area + rest).encode()
                actions.append(dict(action='normalize_actual_display_name', path=path, before=old, after=name))
        result[path] = changed
    for path, manifest in manifests.items():
        parent, skill, _ = _skill_path(path)
        prefix = parent + 'skills/' + skill + '/'
        if 'display_name' in manifest and manifest['display_name'] != skill:
            actions.append(dict(action='normalize_manifest_display_name', path=path,
                                before=manifest['display_name'], after=skill))
            manifest['display_name'] = skill
        manifest['payload_root'] = prefix.rstrip('/')
        manifest['original_manifest_sha256'] = digest(files[path])
        def refreshed(relative):
            full = posixpath.normpath(prefix + relative)
            target = relocations.get(full, full)
            require(target in result, 'Moved manifest points to absent payload: ' + path + ': ' + relative)
            return posixpath.relpath(target, prefix.rstrip('/')), digest(result[target])
        if isinstance(manifest.get('files'), dict):
            manifest['files'] = {refreshed(relative)[0]: refreshed(relative)[1] for relative in manifest['files']}
        for resource in manifest.get('resources', []):
            if 'emitted_path' in resource:
                resource['emitted_path'], resource['emitted_sha256'] = refreshed(resource['emitted_path'])
        if isinstance(manifest.get('canonical_to_emitted'), dict):
            manifest['canonical_to_emitted'] = {canonical: refreshed(relative)[0]
                                                for canonical, relative in manifest['canonical_to_emitted'].items()}
        result[relocations[path]] = encoded(manifest)
    coverage = validate(result)
    changed_rows = [dict(path=path, before_sha256=digest(files[path]), output_path=relocations.get(path, path),
                         emitted_sha256=digest(result[relocations.get(path, path)]))
                    for path in sorted(files) if path in relocations or result[path] != files[path]]
    evidence = dict(schema=SCHEMA, profile=profile, actions=actions, relocations=relocations,
                    changed_files=changed_rows, original_files=_inventory(files), emitted_files=_inventory(result),
                    coverage=coverage, legal_records='License and NOTICE payloads are relocated byte-exact; applicable rights and file-specific obligations are assessed separately. This content scanner makes no license decision or new grant.')
    return result, evidence
