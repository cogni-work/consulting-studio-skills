# Graphic specification contract 0.1.4

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
Preserve the narrative question, its actual answer and established direction;
compatible isolated standalone work requires no universal upstream chain.

Inputs carry the ordinary question/request, audience, purpose, requested medium,
exact readable permitted source/result bytes and versions/passages, coverage,
ownership/use restrictions, metric or coding definitions, current target and
supplied effective design reference (or its explicit absence). An upstream skill
need not run when supplied material meets these meanings. Read the
[common binding contract](../../../workspace-bindings/contract.md) and
[entity/correction contract](../../../runtime/entity-lineage.md).

For actual discovery/read compose research-sources, knowledge-wiki, entity-home and
method-settings; prepared outputs use entity-home/artifact-home. Personal and the
particular Shared home, acting identity, purpose/audience, technical access and
reuse/retention authority remain separate. Keep live bindings and private libraries
in their authorized homes. Resolve any requested save separately through a supported
authorized operation, verify readback and reconcile uncertain effects before retry.
Otherwise return prepared output without claiming retention.

Outputs retain both aggregate and relevant segmented views, exact underlying values
and source passage inventory, filters/exclusions/transformations, denominator weights,
baseline, metric/coding definitions, population/period/unit, missingness and uncertainty.
The supported headline/provisional story, contrary evidence and permitted human notes
remain inspectable. The encoding proposal declares its scale, mappings, rationale and
owner choices. The readable handoff binds content/evidence/design identities,
audience/purpose, intended relationship, values/derivation, qualifications and medium.

For count-ratio comparisons retain all relevant observed segments, identify the
baseline/comparison periods and keep explicitly based non-observed cells separate.
Quantitative counts must identify definition/population/period basis/unit and
exact source passages. Compatible ratios may differ; incompatible comparisons have no
delta; missing/zero-denominator cells are unknown and prevent incomplete totals.
Row IDs and all generated/stated claim IDs must be unique. Reject repeated identities
explicitly, including collisions between a supplied row ID and a derived claim ID;
different coordinates do not permit reuse and no silent renaming occurs.
All observed cells stay visible. Broader measures, subset views, multi-period analyses
and inferential intervals need their own exact definitions, coverage, justified
derivation and limitations. Use an actually available authorized calculation route.

Qualitative notes retain attributed wording. Without coding there are no counts or
scores; a supplied one-primary-theme-per-note sample method needs exact note coverage,
denominator, assumptions and limits. The resulting counts describe supplied notes,
not population prevalence. No method adoption occurs.
The neutral attributed-note headline reflects whether coding is supplied and makes
no agreement/disagreement inference. The claim ledger includes the exact retained
summary, all supporting note passages and the supplied coding basis or explicit
absence of coding. Full claim enumeration includes substantive summaries.

Corrections pin exact prior output bytes and current dependencies, preserve prior
specifications/issued work/notes, prepare changed drafts and identify affected checks.
Inspect the supplied prior specification and issued caption/note bytes; label any
synthetic specimens explicitly. Include the exact supplied issued identity in affected
uses when dependencies change. State which rendered artifacts and other homes were
actually inspected. A proposed correction implies no persisted flags, global propagation,
notification, release or acceptance.

Separate reference correspondence, arithmetic recomputation and author semantic
self-review from independent review, causal explanation, rendered inspection,
actual intended-reader wiki navigation, collaboration/continuity, owner usefulness
and real-client readiness. Use publishing-render for requested production through
available authorized capabilities and publishing-inspect for the exact artifact.
Claim each result only for its observed scope and exact versions.

## Delivery and structured handoff

Resolve selected source, note and graphic identities/versions before inventory use.
General inventory permission does not select unrequested material; its identities,
passages, paraphrases and instruction warnings do not enter the output or ledgers.
Equal snapshot denominators do not prove identical records or stable-cohort tracking.

Resolve delivery before dependent work. An applicable adopted configuration and its
standing retention apply without another save question. Explicit chat-only overrides
them for this turn. An audience, home or provider outside the configuration needs one
focused question; prepare the draft beside it and write to neither home. Without a
save/readback route the draft stays prepared and delivery incomplete; without a list
or readback route an uncertain earlier write stays unreconciled and is not retried.

The readable output states the delivery mode and state, prior write IDs, figure IDs
and exact captions, assertion statuses, claim and source IDs, every question asked
and exact notes. Every presented cell, rate and change matches the `values` ledger.
It claims no save, render, export, publication or message that was not observed. The structured handoff uses these fields and values:

| Field | Content and controlled values |
| --- | --- |
| `entry_mode`, `handoff` | `direct` with `null`, or `handoff` with the supplied workflow report ID/version and narrative answer |
| `sources` | Permitted sources used: `source_id`, `revision`, the source's stated `coverage` unchanged, `passages_read`, `use_restriction`, `judgement`. Denied material is omitted and unnamed |
| `measure` | The source's exact `definition_ids` (IDs only; put annotations in qualifications), `numerator`, `denominator`, `unit`, `population`, `periods`, `baseline`, `missingness`, `uncertainty`, unchanged except for named qualifications |
| `values` | Every plotted or tabled cell: `row_id`, `source_id`, `version`, `passage`, `kind` (`observed`, `missing`, `estimated`, `assumed`, `modeled`), exact `numerator`/`denominator`; missing stays `null` |
| `claims` | `id`, `wording`, `basis` (`observed`, `calculation`, `documentary`, `stated`, `inference`, `assumption`, `recommendation`), `citations` of exact `source_id`/`version`/`passage`, and a `qualification` on every claim (say `no material qualification` when none applies). An interested source's figure is `stated`; a calculation states no change across incompatible definitions (within-definition levels may share a claim) |
| `assertions_checked` | Each requested, narrative, existing-figure, source or note assertion checked: `origin` (`request`, `narrative`, `existing-graphic`, `source`, `human-note`), `status` (`supported`, `qualified`, `not-supported`, `not-comparable`, `unknown`), `reason`, `claim_ids` |
| `existing_graphics` | `source_id`, `version`, `disposition` (`reused`, `revised`, `not-reused`), `reason` |
| `figures` | `id`, `version`, `relationship`, `encoding`, exact `caption`, `placement`, `value_refs` (row IDs listed in `values`), `source_refs` (valid selected passages covering every source ID/version resolved by this figure's `value_refs`; row refs retain their exact source-cell addresses and additional definition/text citations are allowed), `qualifications`, `static_fallback`, `render_state` (`specified`; `rendered`/`inspected` only when observed) |
| `visualization` | `outcome` (`figures`, `text-table-only`, `not-applicable`) and `rationale` |
| `narrative` | `question`, the carried or pending `answer`, `conflicts` surfaced without reshaping |
| `delivery` | `mode` (`retained`, `chat-only`, `unresolved`), `home`, `configuration_id`, `configuration_revision`, `report_form`, `requested_formats`, `design_refs` of `id`/`version`/`conformance` (`verified` only for a readable reference, else `unverified` or `not-applicable`), `operation_authority` (`applied`, `overridden`, `needs-choice`), `state` (`prepared`, `saved-unverified`, `saved-readback`, `chat-delivered`), `final_link` (`null` until readback), `prior_writes` of `attempt_id`/`status` (`unreconciled`, `reconciled-present`, `reconciled-absent`)/`retried`, `fallback_used` |
| `questions_asked` | Exact questions put to the user in this turn |
| `untrusted_content` | `source_id`, `version`, `passage`, `handling` `not-followed` |
| `effects` | Booleans `saved`, `read_back`, `rendered`, `exported`, `published`, `message_sent`, `retained_copy`; true only when observed |
| `dissent` | Exact notes with `id`, `version`, `author`, `date`, `passage`, `text` |
| `checks` | Author self-checks of name to `status` (`passed`, `failed`, `not-run`) and `note`; never independent review |
| `dispositions` | `retained` boolean; `independent_review`, `rendering`, `visual_inspection`, `installed_agent`, `wiki_navigation` as `not_run` or `not_applicable` unless actually observed |
| `limitations`, `next_decision` | Material limits and the next useful decision with its owner or explicit unknown |
