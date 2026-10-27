# Deliverable contract 0.1.3

Apply [Deliverable mode and home](../../../runtime/storage-lifecycle.md#deliverable-mode-and-home)
early and carry its selected mode/home, exact version and actual state into the
handoff. This does not expand read-only/preparation scope or business authority;
a retained copy needs its own applicable instruction and save/readback/final link.

For substantive report/presentation workflows, explicitly apply the
[report and presentation graphics pass](../../../runtime/requirements.md#report-and-presentation-graphics)
with evidence-visualize before production. Validate/reuse suitable current figures
or record a justified text/table-only outcome. Bind selected figures to argument
placement, exact values/derivation, visible captions/sources/qualifications and
faithful static fallbacks. Integrate them in the final report/deck and inspect every
selected final figure in every requested format. A separate Page, specification,
editable-source figure or speaker notes cannot replace a missing exported figure.
Preserve the actual narrative question and answer when they occurred. A supplied
preference establishes direction, not a completed production checkpoint; keep the
checkpoint pending before production rather than inventing an exchange. Preserve
established direction;
compatible isolated standalone work requires no universal upstream chain.

The usable answer leads. Bind stable Deliverable identity/revision, author/owner/home,
request, audience/purpose, exact Result/content/evidence and Baseline references,
source/read/use coverage, effective design and requested forms. Preserve the agreed
question, scope/exclusions, criterion IDs and dates. No invented engagement is needed
for compatible supplied work.

Return supported storyline sections with explicit observation, analysis, implication
and qualification; refuted/open branches, contrary statements, human originals and
proposed recommendations/alternatives remain readable. Every substantive section,
summary, graphic and proposal binds its exact Result/passages and evidence dependencies.
Criterion coverage judges each exact agreed criterion, including any required
produced form and reader/artifact inspection. Prepared content with an unproduced
required form or unperformed required check is partial, with its content readiness
and remaining gap explicit. Exact-content support criteria do not inherit unrelated
navigation gaps. Gaps name consequence, settling action and
owner/date or unknown; an incomplete form cannot establish promise completeness.

Publishing handoff binds exact content digest, audience/purpose, design identity/rights,
requested medium and graphic relationship, metric definition, underlying values,
source versions/passages/digests, transformation, scale/filter/exclusions and limits.
Production, visual/semantic/reader/navigation checks, human review, release/submission
and client acceptance are separate exact-version dispositions. Do not call prepared
Markdown a finished requested report or call a deck outline an inspected deck.

Correction retains stable identity, prior/current byte identities, changed supports,
impacted sections/graphics/recommendations/criteria/handoff/checks, known issued uses,
human originals and accepted/reserved versions. Proposed impact is separate from
persisted effect. Uninspected dependency coverage and uncertain occurrence remain
unresolved; no blind retry or notification is implied.

A structured companion may retain `request`, `deliverable_ref`, `result_ref`, `baseline`, `storyline`,
`findings`, `recommendations`, `coverage`, `graphic`, `human_originals`, `dependencies`,
`publishing_handoff`, `decisions`, `dispositions`, `correction`, `delivery`,
`questions_asked`, `withheld`, `untrusted_content`, `effects`, `checks`,
`limitations` and `next_decision`. When present, use these shapes and values:

| Field | Shape and controlled values |
| --- | --- |
| `request` | exact current request text |
| `deliverable_ref` | `id` (stable), `revision` (short label, distinct from any uncertain earlier label), `recorded_in_home` boolean (false while prepared, true only after readback), `content_sha256` |
| `result_ref` | `id`, `revision`, `sha256` of the exact Result bytes consumed |
| `baseline` | `id`, `revision`, `criteria` as the ordered criterion-ID list, `due`, and `scope_out` as the supplied exclusion list; optional `scope_in` and other carried baseline fields preserve their supplied values |
| `storyline` | list of content-section objects, each with `source_refs` list of exact {`source_id`, `revision`, `passage`} edges; empty where no source passage is claimed |
| `findings` | one row per Result finding: `id`, `status` `supported` / `refuted` / `open` as consumed, `qualification` |
| `recommendations` | list of objects with `id`, `status` `proposed`, `alternatives`, `decider` or `unknown`, `source_refs` as for storyline |
| `coverage` | list, one row per baseline criterion: `criterion`, `state` `covered` / `partial` / `gap`, (`covered` only when the entire exact criterion is met), and for partial/gap `consequence`, `settling_action`, `owner`, `date` (or `unknown`) |
| `graphic` | `outcome` `figure-selected` / `text-table-only` / `blocked`, `rationale`, `figures` list, optional `tables` list; each figure/table has `source_refs` as for storyline; `inspected` (true only after actual final-format inspection) |
| `human_originals` | permitted notes used: `id`, `revision`, `author`, `date`, `kind`, exact `text` |
| `dependencies` | one row per cited passage: `source_id`, `revision`, `passage`, optional exact `quote`; only sources read for this request |
| `publishing_handoff` | `design_ref` {`id`, `revision`} as configured, `content_sha256`, audience, purpose, `medium` carrying the exact configured requested form (preparation/production state stays separate) |
| `delivery` | `mode` `retained` / `chat-only` / `unresolved`; `home` (configured home for retained, else null); `configuration_id`, `configuration_revision`; `configuration_use` `applied` / `overridden` / `needs-choice`; `retention_authority` `explicit` / `standing` / `none`; `state` `chat-delivered` / `prepared` / `saved-unverified` / `saved-readback`; `final_link` or null; `prior_writes` (unique attempt identities) [{`attempt_id`, earlier attempted record `revision`, `status` `unreconciled` / `reconciled-present` / `reconciled-absent`, `retried`, and `who_can_check` (or `unknown`) while unreconciled}]; `fallback_used` false; `blocker` |
| `questions_asked` | exact questions put to the user this turn |
| `withheld` | `denied_contributions` count (no identity), `material` [{`ref`, `reason`}] for unsupplied or out-of-limit material |
| `untrusted_content` | [{`source_id`, `revision`, `passage`, `handling` `not-followed`}] |
| `effects` | booleans `saved`, `message_sent`, `wiki_written`, `retained_copy`, `provider_write`, `artifact_rendered`, each true only when it actually occurred |
| `dispositions` | `production`, `artifact_inspection`, `engagement_lead_review`, `independent_review`, `release_submission`, `client_acceptance`, `wiki_navigation`, `installed_agent`: `not_run` / `not_applicable` / `blocked` unless the act is actually evidenced for this version |

Use actual authorized tools for any requested storage operation; these fields
imply none. The readable answer is useful independently. Exact output-byte receipts/checks stay outside their own
self-referential payload; identity/version labels alone do not pin content.
`deliverable_ref.content_sha256` and `publishing_handoff.content_sha256` both hash
all UTF-8 bytes of the complete readable reply as delivered, including whitespace
and line endings. Keep these digests in the companion or an outside receipt, never
inside the readable text they hash. No content markers or extracted blocks apply.
The list and reference keys above make the companion protocol explicit before
execution; they add no expected answer, source interpretation or business act.
For source/component preparation, required product production, review, native and
acceptance gates remain `not_run` or `blocked`; `not_applicable` never waives an
applicable gate merely because this component did not execute it.

When a structured figure/table uses copied scalar values, it may add `value_cells`
with `path` (keys addressing its `values`), `type` (`integer`, `number`, `string`),
`source_literal` (the exact copied literal), and `source_ref` (an own source edge).
The typed value's string representation equals that literal, which occurs exactly
in the addressed selected passage. This is a lexical bridge only: it cannot establish
that the value belongs to the stated entity, measure, population or period. Derived
rates, transformations, units and that semantic association require direct review;
do not turn them into fabricated copied-source literals.

Technical checks compare declared source edges with the selected source inventory,
original note fields, exact request/configuration/form and byte identities. They do
not infer citations or effects from prose, classify source instructions, establish
semantic support, or certify reader understanding. Declaration completeness,
untrusted-content recognition, content quality and truthful readable claims require
separate direct review of the exact output. No successful technical check transfers
to production, review, release, acceptance or installed-runtime gates.
