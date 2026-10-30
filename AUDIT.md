# S release 1.2.2, 2026-10-29

This release publishes the unchanged owner-tested S1.2.2 candidate as
`consulting-studio-skills.zip`, SHA-256
`b929d367b7c1a9e96a9eaffbc6fbc2815d75bd488e581416873816219ae09ded`.
Candidate source commit: `2f24ecb713f696ccbc3b2ae4aaf827b7ec9d33a0`.
The source pin is retained provenance, not a promise that private authoring history
is publicly navigable. The release contains 27 consulting methods / 35 modes and
Setup, Workspace Librarian and neutral Resume: 30 entries in total.

All 30 technical and display names match. Setup remains included. Generated
packaging commentary and nonfunctional origin breadcrumbs are removed throughout
the instructions and nested references; substantive methods, functional resource
links, human notes and required reads remain. Exact original legal notices and
metadata are retained in their package homes outside the skills tree. Existing
Apache-2.0 terms and attribution are preserved. Later S1.2.3 report-contract and
work-location changes are outside this release.

The candidate's exact installer and finite rebuild inputs are preserved. Build-time
candidate statements such as publication not authorized or acceptance not run
remain historical metadata in those bytes. The current owner decision and release
record supply the subsequent publication authority and scoped acceptance without
altering the tested artifact. Repository documentation improvements are separate
from the installer.

## Testing status and limitations

**S1.2.2 is owner-tested and accepted for the documented scope.** On 2026-10-29,
the owner successfully ran Setup and a bounded problem-framing workflow using
S1.2.2 with Astra, including fresh reads of saved settings and required references.
The owner subsequently accepted S as ready for use and approved this publication.

Additional owner-reported workflows demonstrated reuse of an existing project,
authorized saving to Pages followed by readback, and an ordinary stakeholder task
from general chat that reused existing framing rather than creating a standalone
document. The exact model and package version of those later runs were not
separately confirmed; they are supporting observations, not an expanded exact
S1.2.2/model test matrix. Private material and transcripts are excluded here.

Recorded local validation of the candidate source passed 136 commands, with an
independent source/artifact review and repeatable rebuild checks. These checks
establish their source/package scope; they are distinct from the owner's host
observations. No independent host test or certification is claimed.

The documented tests do not cover the whole method/mode catalog, every model or
client surface, colleague/team access, controlled update or recovery. Those remain
unverified rather than failures of the successful scoped tests. New users can
start with [the README example](README.md#try-it) and use
[the qualification plan](INSTALL-TEST-PLAN.md) for further coverage suited to their
work. The plugin supplies no new data permissions or connected tools.

## Rebuild the exact S1.2.2 installer

From this repository's root, write to a new output directory:

```sh
python3 -B rebuild/implementation/skill-presentation/prepare.py --rebuild-from rebuild --output ../s-1.2.2-rebuilt
```

Python standard library only; no Git, network, private history, App source or
credentials are needed for the finite rebuild. Compare the rebuilt installer,
rebuild archive, distribution and selection against the published checksums.
Recreate the deterministic public repository archive separately:

```sh
python3 -B release/repository.py --output ../consulting-studio-skills-1.2.2-repository.zip
```

The output must not already exist and must be outside the repository root. This
helper validates `repository.json` before packaging. The repository archive
contains the public source and documentation; GitHub's automatically generated
source archives are separate from this deterministic repository archive. Historical release rebuild instructions below apply only to
their named release/tag.

For the exact repository archive published with S1.2.2, use the `v1.2.2` tag.
The main branch may contain later description updates and their refreshed source
inventory. Those documentation changes do not update the published installer,
release assets or their recorded checksums.

---

# Historical S release 1.2.1, 2026-10-29

S1.2.1 incorporates reviewed project/reference maintenance, cumulative research,
accepted synthesis and read-only reentry rules. It contains27 methods/35 modes,
Setup0.1.8, Librarian0.2.2 and neutral Resume0.2.1. All93 canonical input bytes
match the reviewed selection:29 changed runtime revisions and64 unchanged inputs.
The31-input source delta also includes two changed packaging inputs. Current public
S publication was authorized on2026-10-29 at05:41:49UTC and continues the existing
Apache-2.0 S terms; legal/scope.json records exact sources and release adaptations.
Prior approvals, owner README prose, LICENSE/NOTICE, tags and assets are preserved.

Canonical selected source is recorded separately from reviewed packaging source
23ee5920912ccf15fcfd2ca3477d11c41fc97f3a and merged main
1b207ee2d34620b44728522fe83023567a3ceedb; the latter share tree
a41d142b556d2be59ba4574326a1d29610bfd9c5. The public generator is a release
adaptation of the exact retained candidate generator. All six reused tools and
selection remain exact; canonical sources are not edited in this public export.

Rebuild the current plugin and finite input ZIP without Git/network:

    python3 -B rebuild/implementation/aligned-release/prepare.py --rebuild-from rebuild --public-release --output ../s-1.2.1-rebuilt

Compare plugin ZIP, rebuild ZIP, distribution.json and selection.json against
SKILLS-SHA256SUMS. Rebuilding the repository ZIP additionally requires the exact
previous public tree atfff65b7e5debd215f52bc9228d07bdee535dd762 supplied with
--public-base. The103 finite rebuild inputs include93 canonical files, eight
emitted generator inputs, the exact candidate generator and REBUILD.md.
No App/GUI/MCP/server or private customer source is included. Source/package checks
and publication establish no native execution, fresh-chat continuity, installation,
update/recovery or customer acceptance; issue228 remains open.

---

# Historical S release 1.1.0, 2026-10-28

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

## Historical 0.1.0 test status

The following describes 0.1.0 at its preparation checkpoint. The testing phase had started. The exact 0.1.0 package has not yet been tested
through a fresh ChatGPT installation and ordinary use. Compatibility with Codex,
Desktop and mobile is also unverified. Local documentation, archive and rebuild
checks do not establish installation or native behavior.

## Historical 0.1.0 package and rebuild

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
