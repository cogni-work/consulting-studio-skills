#!/usr/bin/env python3
"""Verify the finite public tree and reproduce its deterministic source ZIP."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    if output == root or root in output.parents:
        parser.error('Write the archive outside the verified source tree')
    files = {}
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if '.git' in rel.parts:
            continue
        if path.is_symlink():
            raise ValueError('Unexpected symbolic link: ' + rel.as_posix())
        if path.is_file():
            files[rel.as_posix()] = path.read_bytes()
    manifest = json.loads(files['repository.json'])
    actual = {p: dict(bytes=len(d), sha256=hashlib.sha256(d).hexdigest())
              for p, d in files.items() if p != 'repository.json'}
    if actual != manifest['files']:
        raise ValueError('Public source inventory mismatch')
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path, data in sorted(files.items()):
            item = zipfile.ZipInfo(path, (2026, 10, 29, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.create_system = 3
            item.external_attr = 0o100644 << 16
            z.writestr(item, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('xb') as f:
        f.write(buffer.getvalue())
    print(hashlib.sha256(buffer.getvalue()).hexdigest() + '  ' + str(output))


if __name__ == '__main__':
    main()
