#!/usr/bin/env python3
"""Verify canonical fidelity, deterministic bytes and offline governing closure.

The current-source check is distinct from imported/installed skill execution.
"""
import argparse
import io
import json
import posixpath
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

import release

require = release.require


def unpack(data, name):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), 'Duplicate archive member')
        files = {}
        for info in archive.infolist():
            path = PurePosixPath(info.filename)
            require(not path.is_absolute() and '..' not in path.parts and path.parts[0] == name
                    and len(path.parts) > 1 and str(path) == info.filename, 'Unsafe archive path')
            require(info.date_time == (1980, 1, 1, 0, 0, 0), 'Nondeterministic archive time')
            require(stat.S_IFMT(info.external_attr >> 16) == stat.S_IFREG
                    and (info.external_attr >> 16) & 0o777 == 0o644, 'Nonregular/executable archive member')
            files[str(path.relative_to(name))] = archive.read(info)
    require([p for p in files if PurePosixPath(p).name.casefold() == 'skill.md'] == ['SKILL.md'],
            'Expected exactly one root SKILL.md')
    return files


def anchors(data):
    values = set()
    counts = {}
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', data.decode(), re.M):
        slug = re.sub(r'[^\w\- ]', '', heading.lower().replace('`', '')).replace(' ', '-')
        suffix = counts.get(slug, 0)
        counts[slug] = suffix + 1
        values.add(slug + ('-' + str(suffix) if suffix else ''))
    values.update(re.findall(r'<a\s+(?:id|name)=[\"\']([^\"\']+)', data.decode()))
    return values


def destination(files, origin, locator):
    parts = urlsplit(locator.strip('<>'))
    if parts.scheme or parts.netloc:
        return
    path = posixpath.normpath(posixpath.join(posixpath.dirname(origin), unquote(parts.path))) if parts.path else origin
    require(path in files and not path.startswith('../'), 'Missing offline dependency: ' + origin + ' -> ' + locator)
    if parts.fragment and path.endswith('.md'):
        require(unquote(parts.fragment) in anchors(files[path]), 'Missing offline anchor: ' + origin + ' -> ' + locator)


def check_links(files):
    for path, data in files.items():
        if path.endswith('.md'):
            for match in release.LINK.finditer(data.decode()):
                destination(files, path, match.group(2))
            for pattern in (release.REFERENCE_LINK, release.HTML_LINK):
                for match in pattern.finditer(data.decode()):
                    destination(files, path, match.group(2))
        elif path.endswith('.json') and path != 'manifest.json':
            def walk(value, pointer=''):
                if isinstance(value, dict):
                    for key, member in value.items():
                        address = pointer + '/' + key
                        if release.json_locator(pointer, key) and isinstance(member, str):
                            destination(files, path, member)
                        else:
                            walk(member, address)
                elif isinstance(value, list):
                    for i, member in enumerate(value):
                        walk(member, pointer + '/' + str(i))
                elif isinstance(value, str):
                    for match in release.LINK.finditer(value):
                        destination(files, path, match.group(2))
                    for pattern in (release.REFERENCE_LINK, release.HTML_LINK):
                        for match in pattern.finditer(value):
                            destination(files, path, match.group(2))
            walk(json.loads(data))


def validate_package(data, row, source, generator_inputs):
    files = unpack(data, row['name'])
    require(release.digest(data) == row['archive_sha256'], 'Archive digest mismatch')
    manifest = json.loads(files['manifest.json'])
    require(release.digest(files['manifest.json']) == row['manifest_sha256'], 'Manifest digest mismatch')
    require(manifest['source_commit'] == source.commit and manifest['source_tree'] == source.tree,
            'Canonical source identity drift')
    require(manifest['generator_inputs'] == generator_inputs, 'Generator identity drift')
    require(set(manifest['files']) == set(files) - {'manifest.json'}, 'Emitted inventory drift')
    for path, checksum in manifest['files'].items():
        require(release.digest(files[path]) == checksum, 'Emitted resource digest mismatch: ' + path)
    require(manifest['name'] == row['name'] and manifest['modes'] == (source.items[row['name']]['modes'] or [None]),
            'Skill/mode identity drift')
    require(all(value == 'NOT_RUN' for value in manifest['gates'].values()), 'Invented installed/review acceptance')
    # Regenerate independently from the selected canonical inputs; hashes alone can
    # be forged along with an edited payload, so compare the complete bytes.
    config = json.loads((release.HERE / 'release.json').read_bytes())
    expected = release.assemble(source, row['name'], config, generator_inputs)
    require(files == expected, 'Canonical procedure/resource/adaptation fidelity drift')
    check_links(files)
    for resource in manifest['resources']:
        for adaptation in resource['adaptations']:
            if adaptation['classification'] == 'bundled governing/resource read':
                destination(files, resource['emitted_path'], adaptation['result'])
    return manifest


def validate_inventory(archives, inventory, source):
    require(inventory['source_commit'] == source.commit and inventory['source_tree'] == source.tree,
            'Inventory source identity mismatch')
    items = inventory['items']
    names = [i['name'] for i in items]
    canonical = [i['name'] for i in source.catalog['skills']]
    require(names == [n for n in canonical if n in names] and len(names) == len(set(names)),
            'Inventory skill identity/order mismatch')
    require(set(archives) == {i['archive'] for i in items}, 'Archive inventory mismatch')
    require(inventory['skills'] == len(items) and inventory['modes'] == sum(len(i['modes']) for i in items)
            and inventory['business_resources'] == sum(len(source.methods[n]) for n in names), 'Coverage totals mismatch')
    for row in items:
        manifest = validate_package(archives[row['archive']], row, source, inventory['generator_inputs'])
        for key in ('modes', 'method_version', 'bundle_version', 'runtime_dependencies', 'gates', 'core_adaptation_compatibility'):
            require(row[key] == manifest[key], 'Inventory/manifest drift: ' + key)
        require(row.get('issue') == manifest.get('issue'), 'Inventory/manifest drift: issue')
        require(row['procedure_source_sha256'] == release.digest(source.read('implementation/skills/' + row['name'] + '/SKILL.md')),
                'Procedure source digest mismatch')
        require(row['procedure_emitted_sha256'] == manifest['files']['SKILL.md'], 'Procedure emitted digest mismatch')
        require(row['resource_count'] == len(manifest['resources']) and row['own_business_resources'] == len(source.methods[row['name']]),
                'Resource coverage drift')
    return dict(skills=len(items), modes=inventory['modes'], business_resources=inventory['business_resources'],
                source_commit=source.commit, source_tree=source.tree, native_import='NOT_RUN')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, help='Validate generated artifacts; default regenerate current source in memory')
    args = parser.parse_args()
    config = json.loads((release.HERE / 'release.json').read_bytes())
    source = release.RuntimeSource(config['core_commit'])
    if args.directory:
        inventory = json.loads((args.directory / 'inventory.json').read_bytes())
        require(inventory['generator_inputs'] == release.inputs(), 'Artifacts built by different generator bytes')
        archives = {row['archive']: (args.directory / row['archive']).read_bytes() for row in inventory['items']}
    else:
        archives, inventory = release.build(source, config, release.inputs())
        again, second = release.build(source, config, release.inputs())
        require(archives == again and inventory == second, 'Nondeterministic generation')
    evidence = validate_inventory(archives, inventory, source)
    require((evidence['skills'], evidence['modes'], evidence['business_resources']) == (27, 35, 73), 'Incomplete full release')
    print(json.dumps(evidence, sort_keys=True))


if __name__ == '__main__':
    main()
