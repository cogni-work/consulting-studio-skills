# S release decisions and publication handoff

**Release 0.1.0 is prepared locally and unpublished at this preparation checkpoint.**
Owner approval, generated artifacts, independent review, publication, installation
and acceptance are separate facts. No public operation is established by this file.

## Approved identity, grant and exact scope

The owner approved the S Apache-2.0 grant, public identity, publication scope and
regular PR218 merge on 2026-10-27 at 13:50 UTC. At 13:52 UTC the owner selected
publication at **2026-10-27 17:00 Europe/Berlin (16:00 UTC)**. The subsequent
scope correction required fresh approval; the earlier 29-source approval alone
does not cover the expanded source set.

On 2026-10-27 at **14:59:59 UTC**, the owner explicitly approved the corrected
**31 S own source components plus two separately open App Resume adapter
instruction sources**. The reviewed source baseline is
`dba54c6644d58cd0ff31177f59e4691bd4343631`, tree
`a91be25ea522564a506ea0914ca013bf50e3527e`. The approved scope SHA-256 is
`6248cbe9957b91b65e10413abb934b3ac33111f1e542fdd6419732ac6693f4b0`;
the approved source-delta SHA-256 is
`19b525f388c8fd3f14d4fbb245cadc549cc7ae022c9729c0e49cb49cf25be2b4`.
These dated owner decisions are the approval source; private conversation links
and message identifiers are excluded from the public package.

The public repository is `cogni-work/consulting-studio-skills`, plugin name
`consulting-studio-skills`, first release version `0.1.0`, planned tag `v0.1.0`.
Publication covers only the reviewed history-free extracted `repo/` contents and
exact plugin/repository release archives with checksums. It excludes canonical
private Git history and the separate historical `exporter-artifacts/` directory.
No marketplace publication, installation, credentials or permission change is
included. The approved private security contact is stephan@cogni-work.ai, with
no personal acknowledgement, response or correction deadline.

`legal/scope.json` maps the applied release scope. Exact approved evidence is
retained as `legal/history/approved-scope.json` and
`legal/history/approved-source-delta.json`; these metadata copies are evidence,
not additional licensed works. Identical evidence copies at
`implementation/s-distribution/approved-scope.json` and
`implementation/s-distribution/approved-source-delta.json` support offline rebuild.
The approval object is embedded in `legal/scope.json` and release metadata; no
separate approval document is implied. `repository.json` enumerates current
generated outputs and their hashes. The 93 canonical S inputs comprise 76 inherited
Apache method/supporting files, 15 other first-party nonlegal inputs and two
canonical legal evidence files. The 31 own source components comprise those
15 nonlegal inputs, six rebuild tools/metadata inputs and ten repository code,
documentation and notice inputs. The two App Resume adapter instruction sources
are separately approved open components, outside the S runtime payload; their
approval includes no GUI/MCP software release.

The release applies the complete Apache text, SHA-256
`c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`,
at public repository root, plugin root and each business-method root. It carries
the approved S NOTICE text; its exact approved proposal is retained historically
as `legal/history/NOTICE-S.proposed.txt`, SHA-256
`4235c333ef37e7c6d8a352cda1ab9cd0880d4b5d21ba13892b32a81ee0ac94df`.
Canonical root LICENSE/NOTICE and the canonical rebuild snapshot remain exact
historical evidence. Existing recipient grants, actual third-party terms,
attribution and prominent modification notices remain preserved. The grant
creates no trademark permission, title certification or individual service promise.

## Publication and readback from a Mac

This is an execution plan for the authorized publication time, not an operation
receipt. Before that time, complete local preparation and exact final-source
independent review. If a required check or identity is unresolved, keep publication
blocked and report the specific gap; the clock does not waive release checks.

1. On the Mac, identify the reviewed output directory and inspect its
   `repository.json`, `legal/scope.json`, approval evidence and `SHA256SUMS`.
   Check the plugin/repository archives against those exact hashes. Retain the
   reviewed source commit, exported tree and independent review receipt privately.
2. Prepare a fresh local Git directory containing only the extracted `repo/`
   contents, including required hidden files. Keep its Git history independent of
   the canonical private repository; do not copy `.git`, parent directories or
   `exporter-artifacts/`. Inspect the complete tracked file set before pushing.
3. At or after 17:00 Europe/Berlin on 2026-10-27, inspect whether
   `cogni-work/consulting-studio-skills` already exists. Reconcile any existing or
   uncertain result before retrying. Using the authorized existing GitHub account,
   create or fill only that approved public repository with the reviewed tree.
   Stop if new credentials, permission changes or an unexpected owner are needed.
4. Confirm the public default-branch commit and full tree match the prepared
   tracked contents. Tag that exact public commit `v0.1.0`. Create the GitHub
   Release with the 0.1.0 notes in CHANGELOG.md and attach only
   `consulting-studio-skills-0.1.0-plugin.zip`,
   `consulting-studio-skills-0.1.0-repository.zip`, `repository.json` and
   `SHA256SUMS`. GitHub's automatically generated source archives are distinct
   from the deterministic repository archive.
5. Read back the repository through its public URL, inspect the root README,
   LICENSE, NOTICE, legal evidence and public plugin identity, and resolve
   `v0.1.0` to the exact full commit. Download every attached asset into a fresh
   directory and verify its bytes against the prepared checksums. Record observed
   URL, commit/tag, asset hashes, time and any incomplete result in the designated
   private record. Report publication successful only after that readback.

No operative marketplace descriptor is emitted. A future marketplace route needs
its own authorization and format/host qualification. The public GitHub repository
and Release do not establish an importable marketplace or installed methods.

## Remaining installation decision

A bounded fresh installation/update/recovery still requires the actual workspace,
independent installer outside all contributors, admin, intended users, private
record home/updater, exact V1/V2 artifacts and allowed host effects. Follow
[the test plan](INSTALL-TEST-PLAN.md). The existing private SkillsOnly 1.0.3 test
remains separate. Local source/rebuild checks and publication supply no host or
acceptance pass. S requires no M runtime or M compliance decision.
