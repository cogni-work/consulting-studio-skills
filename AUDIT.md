# Current S release 1.1.0, 2026-10-28

Setup0.1.7 adds Installation prüfen; the27 business methods and Librarian0.2.1
retain their canonical sources. The owner approved the three changed Setup inputs
and two new packaging inputs under Apache-2.0 on2026-10-28 at11:30UTC.
The exact current scope and generated legal overlay are recorded in legal/scope.json.
Public0.1.0 and its tag/assets remain immutable historical evidence.

Rebuild the current plugin without Git, network, private history or an App:

    python3 -B rebuild/implementation/aligned-release/prepare.py --rebuild-from rebuild --public-release --output ../s-1.1.0-rebuilt

Compare the four S artifacts with SKILLS-SHA256SUMS at this repository's root.
The repository ZIP separately preserves current public documentation and unchanged
historical public source/history; two builds from the pinned public base reproduce
its bytes. The old implementation/s-distribution generator below describes0.1.0.
No installation, native qualification, update/recovery or customer acceptance is
established by source/package checks or publication. Issue228 remains open.

---

# Technical notes and release history

## Testing status and limitations

The testing phase has started. The exact 0.1.0 package has not yet been tested
through a fresh ChatGPT installation and ordinary use. Compatibility with Codex,
Desktop and mobile is also unverified. Local documentation, archive and rebuild
checks do not establish installation or native behavior.

## Package and rebuild

`plugin/` contains the 27 methods and the separate Setup, Workspace Librarian and
Resume entries, including their required local resources. `rebuild/` contains
101 finite inputs: 93 canonical files, six build-tool/metadata files, rebuild.json
and REBUILD.md. The source package includes the assembly code under
`implementation/s-distribution/`. Python 3's standard library is sufficient;
no private Git history, constructor, M software or network is needed to rebuild
from the supplied inputs.

From an extracted repository, write to a new local output directory:

```sh
python3 -B implementation/s-distribution/prepare.py --rebuild-from rebuild --output /tmp/consulting-studio-S-rebuilt
python3 -B implementation/s-distribution/prepare.py --rebuild-from rebuild --check /tmp/consulting-studio-S-rebuilt
```

The output contains the plugin ZIP, repository ZIP, extracted `repo/`, current
`repository.json` and checksum files. Historical exporter artifacts are separate
rebuild evidence, outside the plugin and public release asset selection. From the
canonical authoring checkout, omit `--rebuild-from rebuild`. Generated snapshots
are outputs; make source changes in the canonical authoring repository.

The `v0.1.0` tag and its two released ZIPs are immutable. For an exact 0.1.0 rebuild,
use that tag or its repository ZIP and its original checksums. A later main-branch
documentation correction is not a replacement 0.1.0 archive. Its `repository.json`
file inventory must describe the edited tree; historical approval evidence,
source snapshots, plugin bytes and released archive identities stay unchanged.
Such a correction does not make main byte-identical to the original release or
make the original generator reproduce later documentation edits. Rebuild the
release from its tag; use the current canonical generator for future packages.

## Preserved 0.1.0 preparation record, 2026-10-27

The following record describes the original preparation checkpoint. Its pending
publication statements are historical. Current user instructions are in
[README.md](README.md).

Release-specific preparation follows reviewed source
`dba54c6644d58cd0ff31177f59e4691bd4343631`, tree
`a91be25ea522564a506ea0914ca013bf50e3527e`. Technical inventory/export revision
0.2.0 and public release version 0.1.0 identify different things. The owner approved
the corrected scope on 2026-10-27 at 14:59:59 UTC; exact approved scope SHA-256 is
`6248cbe9957b91b65e10413abb934b3ac33111f1e542fdd6419732ac6693f4b0`
and source-delta SHA-256 is
`19b525f388c8fd3f14d4fbb245cadc549cc7ae022c9729c0e49cb49cf25be2b4`.
Read [OWNER-DECISIONS.md](OWNER-DECISIONS.md) for authority and the timed publication
plan. This document describes the audit boundary; it is neither a new executed
check receipt nor independent review, legal certification or host acceptance.

| Finite set | Release boundary |
| --- | --- |
| 93 canonical S inputs | Previous 91 plus two provider neutral Resume files; 76 inherited Apache method/supporting files, 15 other first-party nonlegal inputs and two retained legal evidence files |
| 101 standalone rebuild inputs | 93 canonical files, six tools/metadata inputs, rebuild.json and REBUILD.md; no M runtime, private Git history, constructor or network required |
| Three auxiliary entries | Setup, canonical Workspace Librarian and provider neutral read-only Resume; unchanged 27 business procedures/35 modes, each with its complete 86-resource closure |
| Separate App Resume adapter | Two owner-approved open instruction sources; explicit M packaging boundary, outside the S runtime payload; no GUI/MCP software release |
| Approved own source scope | 31 S components: 15 nonlegal canonical inputs, six rebuild inputs and ten repository code/docs/notice inputs; the two adapter instructions bring the separately approved aggregate to 33 |
| Applied release mapping | legal/scope.json and repository.json identify current outputs/hashes; legal/history/approved-scope.json and approved-source-delta.json retain exact approved evidence |
| Public identity | consulting-studio-skills 0.1.0 with Apache-2.0; historical exporter metadata remains separate provenance/rebuild evidence; no operative marketplace descriptor |

The exporter rejects unknown inputs, missing reads, stale pins, unclassified outputs
and changed packaging dependencies. The repository generator uses that same finite
selection. Generated snapshots are outputs, never another editable knowledge source.
The existing checks cover resource links, source hashes, three discoverable entries,
unchanged business-method identity, notice roundtrips, rights boundaries and offline
reproducibility. Their executed final-version receipts are recorded separately.

Public repository root, plugin root and each business-method root use the complete
approved Apache text: 11,357 bytes, SHA-256
`c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`.
The approved S NOTICE preserves applicable attribution and nonredistribution limits.
Its exact approved proposal is retained at legal/history/NOTICE-S.proposed.txt,
SHA-256 `4235c333ef37e7c6d8a352cda1ab9cd0880d4b5d21ba13892b32a81ee0ac94df`.
Canonical root LICENSE/NOTICE, canonical rebuild legal inputs, historical artifacts and original npm observation bytes stay
unchanged. Approval evidence copies add no licensed source components.

Public creation/upload/release/readback remains pending at this preparation
checkpoint. No provider operation, workspace installation, fresh-session application,
update/recovery or autoload is established here. Saving, readback, human adoption,
discovery and actual later-session use remain separate observations. Source and
archive checks do not close issue212 or establish general self-install readiness.

Contributor self-checks and the later independent exact-final-source review are
reported separately. The complete contributor roster remains outside the review;
the reviewer inspects final source only after contributors stop editing.
