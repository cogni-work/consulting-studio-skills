# Monday read-time contract 0.1.1

Apply [Deliverable mode and home](../../../runtime/storage-lifecycle.md#deliverable-mode-and-home)
early and carry its selected mode/home, exact version and actual state into the
handoff. This does not expand read-only/preparation scope or business authority;
a retained copy needs its own applicable instruction and save/readback/final link.

Ordinary output is a brief action table and dated evidence/coverage note. JSON and
matching Markdown can support an exact handoff. Check actual read operations
separately; preparing a view performs no portfolio synchronization. Information access and outgoing
use must cover the particular reader/purpose. Human owners choose the next action.

## Compatible supplied inputs

Accept dated extracts satisfying the meanings of the
[Follow-up/Need contract](../../sales-followup/references/followup-contract.md) and
[Opportunity/Decision/Agreement Reference contract](../../sales-pursuit-event/references/event-contract.md). Require stable identity,
exact revision, owner/author/current home, audience/use basis, exact supporting
passages, coverage and original need/history. Keep relationship and action owners
separate. Exact proposal ID/revision and submission evidence differ from acceptance,
buyer result and order. Engagement/Work Item context may be supplied directly;
closure is not required.

For a structured handoff, identify `case` and `sources`. Each record carries
its immutable `snapshot`, `source_keys`, supported `business_events` and optional
`allocation` with a named person, inclusive calendar start/end dates and
`commitment` confirmed/possible/proposed/unknown. Snapshot has kind, title, need,
owners, action, deadline (`YYYY-MM-DD`, timezone-aware timestamp or unknown), state,
proposal/acceptance/buyer/order/work-authority fields when relevant, and separate
renewal dates. `allocation_conflicts` prevents reliance on disputed staffing; an order dispute alone
does not erase supported possible windows. `conflicts` are supplied unresolved upstream assessments with exact
contrary passages, not silently settled here. Typed payloads must already faithfully
represent inspected text; metadata alone is no proof. Reject incompatible supplied
records rather than inventing an upstream decision. Free-form ordinary source
interpretation requires inspection of the actual source passages.

Sources carry id/revision/passage, recorded_at, author, owner, home, audience,
coverage and exact text. Permitted sources may be partly read with named limits.
Denied/unavailable/expired/revoked entries have no content, private identity or
record inventory. Unknown times remain unknown, not output time. Future snapshots
are reported as not current and excluded from current recency/collisions. Business
acts later than source capture, missing required event chronology or ambiguous
timezone block the affected derived classification.

## Useful output and fidelity

The view has its own case/revision, target, observation time/timezone, input/freeze
hash, exact source coverage, ordered rows, current business recency, overlaps,
unassessed allocations, human originals, preserved history, prior-view reference,
uncertain effects, limitations, effects and gates. Each row retains its exact
snapshot and business events, evidence/quotes/links, separately derived date_status,
visibility and proposed settling step. Never turn proposed action into a commitment.

A date-only deadline is due today until that business day's end; a precise deadline
can be overdue earlier that day. Completed/dismissed/linked follow-ups and closed/lost/withdrawn/no-decision pursuits are inactive.
Unknown deadline/owner remains visible. Last business update is the latest supported
occurred event at or before observation time, distinct from captured/read time.
No arbitrary age threshold or complete coverage/freshness claim is supplied.

Pending-order visibility includes won pursuits whose order is pending/unknown;
submitted offers and unresolved/recommended outcomes remain separate review lanes.
No order, accepted proposal, framework or staffing reservation is inferred from
another lane. Unknown work authority stays unknown; explicit no-authority stays so.

An overlap is confirmed only when both supported allocations are confirmed;
otherwise contingent. Inclusive intervals that touch overlap for that day. Unknown,
reversed or contradictory intervals are unassessed; do not infer capacity or zero
load. No conversion from associate suggestion to named commitment.

Markdown must expose each row's owners, action/date, proposal/buyer/order/authority,
original need/renewal dates, business events, unresolved facts, source dates and
coverage, overlaps and unassessed limits, history, notes and proposed next steps.
Exact quotes retain context. Source locators resolve relative to the actual output
directory; validate the resolved file and anchor separately from generated strings.
Local anchors establish local correspondence only.

For a read-only view, all live effect flags are false. Keep target adoption,
independent review, actual access and navigation, continuity and owner acceptance
separate from author checks. Unperformed checks remain NOT_RUN; do not infer a
permission, business change or complete coverage from a generated view.

## Preserve date precision and proposed actions

Business-event dates keep the precision actually supported in the passage. The
structured handoff uses `at: YYYY-MM-DD` with `precision: date` and exact `date_quote`,
or `at: unknown` with `precision: unknown`. Event hours stay unknown; `recorded_at`
is source capture metadata, never the event time. Known business dates coexist
with undated reports, whose recency remains unresolved. No midnight is asserted.

Each snapshot has `field_basis` for relationship owner, action owner, next action
and deadline: `supplied`, `proposed` or `unknown`. “Should” recommendations retain
proposed owner/action/date; “will” can evidence a recorded commitment. Suggested
dates remain proposed even when passed (`proposed_date_passed`), never overdue
commitments. Renewal action dates stay unknown independently of end/notice dates.
On resumption preserve prior extraction objects under explicit `history_qualifications`
when their accuracy is unresolved; do not certify them as current timestamps or
commitments. Preserve original business records.
