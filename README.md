# Consulting Studio skills 0.1.0

**Prepared locally, 2026-10-27; publication/readback pending.** The approved public
identity is `consulting-studio-skills` version `0.1.0`, repository
`cogni-work/consulting-studio-skills`, planned tag `v0.1.0`. Publication is authorized
for 2026-10-27 at 17:00 Europe/Berlin (16:00 UTC) and has not been executed at this
preparation checkpoint. The release-specific Apache-2.0 grant and corrected scope
are owner-approved; see [the decisions and publication plan](OWNER-DECISIONS.md).

This repository contains all 27 consulting methods, 35 declared modes, their
complete governing resources and three auxiliary entries: Setup, Workspace
Librarian and Resume. It requires no M purchase, Studio GUI, MCP service, Worker
app or workspace agent. The separate private SkillsOnly test is unchanged.
Exact current identities are in `repository.json` and external `SHA256SUMS`;
historical exporter metadata is retained separately as provenance/rebuild evidence.

## Contents and rebuild

`plugin/` contains the complete S plugin, including individually inspectable method
folders. The three auxiliary entries are separately discoverable at
`skills/setup/SKILL.md`, `skills/workspace-bindings/SKILL.md` and
`skills/studio-resume/SKILL.md`. Workspace Librarian is generated from its existing
canonical instructions, with no second editable procedure. Resume has a provider
neutral read-only contract; it reads exactly identified accessible work through
actual host tools, reports present/open/one next step and never resumes writes
automatically. Each business method has its own root SKILL.md and all 86 required resources;
required reads close locally. `rebuild/` contains the exporter's exact 101 finite
inputs: 93 canonical files, six build-tool/metadata files, rebuild.json and REBUILD.md.
`implementation/s-distribution/` contains this repository's additional reproducible
assembly code and documents. The output carries no private Git history,
constructor, M code, dependency installation or live configuration.

Use Python 3 standard library from an empty local output location. From the
canonical checkout, run:

```sh
python3 -B implementation/s-distribution/prepare.py --output /tmp/consulting-studio-S-repo
python3 -B implementation/s-distribution/prepare.py --check /tmp/consulting-studio-S-repo
```

From an extracted repository, independently rebuild without Git/network:

```sh
python3 -B implementation/s-distribution/prepare.py --rebuild-from rebuild --output /tmp/consulting-studio-S-rebuilt
```

Compare both ZIPs and `repository.json` against the originating `SHA256SUMS`.
The output includes `consulting-studio-skills-0.1.0-plugin.zip`,
`consulting-studio-skills-0.1.0-repository.zip`, the extracted `repo/` and six
unchanged historical exporter artifacts under `exporter-artifacts/`. Those
historical artifacts retain their original hashes and remain outside the
publishable repository/plugin payload and release asset selection.

Generated snapshots are outputs: author changes in the canonical repository,
revise/review its explicit inventory and approved release scope, then regenerate.
The original canonical mapping is retained in plugin provenance; current manifests
record adaptations and resulting bytes. Public root/plugin/per-method LICENSE
uses the complete approved Apache-2.0 text, and NOTICE carries the approved S text.
Canonical rebuild legal inputs remain exact. `legal/scope.json` records the applied
release scope; `legal/history/` retains exact approved scope/source-delta evidence
and the original approved notice proposal. Approval metadata is evidence, not an
additional licensed work. Canonical private Git history is excluded.

## S-only installation after separate authorization

1. An owner/admin and independent installer select a fresh eligible workspace,
   intended users, actual host/surface, private test record and exact authorized
   effects. Read [the test plan](INSTALL-TEST-PLAN.md). No candidate command installs
   anything. Local checks establish no native import or usable installed methods.
2. Inspect the pinned repository/archive checksums, inventory, license standing,
   [known limits](KNOWN-LIMITS.md) and each selected method's required-resource map.
   Source access, marketplace import, installation, enablement, resource reading,
   tool authorization and owner acceptance are separate observations.
3. No operative marketplace descriptor is emitted by this release. Public GitHub
   publication establishes source and archive access; a future marketplace route
   requires separate authorization, exact descriptor/ref review and actual host
   qualification before installation. Do not infer marketplace importability from
   the repository or the plugin ZIP.
4. After that separate route is authorized and qualified, on a host that actually
   offers it, an administrator uses **Admin > Plugins >
   Import marketplace**, selects the authorized repository and fixed commit, and
   reviews the exact plugin and workspace policy before import. Use only controls
   actually exposed to that administrator. Missing eligibility or unsupported
   import is a bounded blocked route. Do not add credentials, permissions or apps
   to work around it. A local Desktop marketplace is a different route and
   supplies no whole-workspace evidence.
5. Observe all 27 methods' availability and intended-user enablement. In ordinary
   fresh conversations read the actual root instructions and applicable child
   sections through the reader available on that surface, without truncated
   output. Apply selected methods to permitted supplied or labelled fictional
   content. Verify useful output and intended-reader access. Account for all 35
   standard modes before claiming full coverage; partial tests remain partial.
6. Setup is optional. Ordinary useful work can start with supplied inputs and no
   saved firm settings. Research, storage, artifact rendering or inspection require
   their own actually available authorized tools. This package supplies none.
   Do not create homes or save settings merely to demonstrate installation.

## Controlled updates and recovery

Preserve the exact prior approved archive/commit and observed loaded identities,
customer settings/adaptations, human notes/dissent and issued work before adoption.
Compare old/new manifests and deliberately changed procedure/resource bytes, inspect
affected checks and compatibility, and obtain explicit adoption of the exact target.
Refresh the repository marketplace only through its supported sync/ref controls;
sync alone is neither loaded-runtime proof nor customer acceptance. Read the changed
bytes in fresh sessions and recheck affected ordinary work. Unknown effects stop
the affected retry until inspected; avoid duplicate imports.

For recovery, use the supported ref/version restoration control to the exact prior
approved package, then observe its actual content, enablement and settings again.
If that surface cannot select or restore the prior identity, keep recovery blocked
and retain the prior backup; do not delete/recreate marketplaces as an improvised
rollback. Preserve adaptations and notes. Package recovery does not reverse issued
outputs, messages, saves or other external effects. This candidate has no runtime
database/schema migration. Actual update and recovery remain NOT_RUN.

## Support and evidence

S is free open source under Apache-2.0 for self-installation, with no personal
acknowledgement, response or correction deadline. No qualified host or supported
release line is claimed.
See [support](SUPPORT.md), [security](SECURITY.md), [changelog](CHANGELOG.md) and
[known limits](KNOWN-LIMITS.md). License/publication/host decisions remain distinct.

Primary platform guidance inspected 2026-10-27:
[packaging](https://developers.openai.com/plugins/build/plugins),
[workspace plugin management](https://learn.chatgpt.com/docs/enterprise/plugin-management).
These describe routes; they establish no observation in the proposed test workspace.
