
<!-- Consulting Studio modification, 2026-10-27: local resource locators were packaged; an explicit working-instruction read was added where applicable. Exact source identities and changes are recorded in the accompanying manifests. -->
# Operational requirements for delivery status

| Requirement | Apply it in the view |
| --- | --- |
| [Planning contract](../../consult-planning/references/output-contract.md) | Use exact compatible baseline/plan and distinguish proposed work, assigned work, receipt, analysis completion and observed completion. |
| [Delivery journey](../../../runtime/requirements.md#business-lifecycle) | Derive completed/next work, milestone consequences, missing inputs, stakeholders, blockers, risks, named decisions and change status from known records. |
| [Delivery objects](../../../runtime/requirements.md#business-records) | Preserve exact Baseline, Work Item, Milestone, Reservation and Scope Change identities; keep human originals and contradictory evidence. |
| [Decisions](../../../runtime/requirements.md#human-decisions) | Separate raised/assessed/scope-approved/cost-committed/activated change facts. A view changes no commitment or meaningful business-update timestamp. |
| [Deliverable contract](../../consult-deliverable/references/output-contract.md) | Preserve exact-version review/release/submission/acceptance and reservations; current drafts inherit no historical acceptance. Keep uncovered criteria and form gaps explicit. |
| [Knowledge](../../../runtime/requirements.md#evidence-and-knowledge) | Retain business-event time, freshness, read coverage, source support, contrary facts and use restrictions. An absent update proves no completion. |
| [Correction](../../../runtime/entity-lineage.md) | Preserve previous views/notes and show stale support, uncertain effects and incomplete dependency coverage without persisting changes on read. |

Show missing-input owner/action/date or unknown and the consequence for named work
or a milestone. Preserve the committed date; forecasts remain separate. Differing
planning and deliverable baselines require reconciliation, not silent adoption.
Denied reads leave coverage unknown unless other permitted observations establish
a consequence; missing access alone proves no milestone threat.

Read only the references needed for the selected task. Apply their current adopted
requirements within the actual audience, purpose and available authorized operations.
A method dependency names compatible information; it does not require a prior skill
invocation. Retain exact source versions and content identities when consuming outputs.
