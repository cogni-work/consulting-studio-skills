
<!-- Consulting Studio modification, 2026-10-27: local resource locators were packaged; an explicit working-instruction read was added where applicable. Exact source identities and changes are recorded in the accompanying manifests. -->
# Pursuit event contract 0.1.4

Apply [Deliverable mode and home](../../../runtime/storage-lifecycle.md#deliverable-mode-and-home)
early and carry its selected mode/home, exact version and actual state into the
handoff. This does not expand read-only/preparation scope or business authority;
a retained copy needs its own applicable instruction and save/readback/final link.

Prepare a concise record from the permitted evidence; ordinary input may be one
email. A partner records decisions while the actual buyer, contracting, internal
or firm authority decides. Use the structured fields below when exact correspondence
is needed, preserving matching readable content. Verify actual operations separately.

## Useful record and lineage

Lead with what happened, what remains unresolved and the next useful question.
Separate exact-version proposal acceptance, buyer recommendation/result, agreement/
paperwork and permission for the requested work. Keep pending orders visible after
a win; unknowns do not disappear. Quotes keep speaker/date, exact source/revision/
passage, coverage and a browsable source-record link. Local links prove correspondence
only; keep actual intended-reader navigation `not_run` until observed.

Use these top-level fields: `skill`, `version`, `case_id`, `synthetic`, `target`,
`input_sha256`, `bindings`, `upstream_context`, `record`, `lead`, `events`,
`human_originals`, `correction_flags`, `rights_review`, `method_lanes`, `questions`,
`limitations`, `dispositions`, `actions_performed`.

- Identity: sales-pursuit-event 0.1.4 structured contract, exact case/target and every input file hash
  in `input_sha256`. `bindings` equals supplied binding; `upstream_context` preserves
  the exact upstream proposal, criteria, human originals, correction flags, proof
  assessments and limitations where a real sales-proposal artifact is supplied. It stays
  draft until separate attributable submission evidence; synthetic examples remain
  explicitly fictional. No artifact is invented for absent proposals.
  Resolve the exact pinned dependency revision and verify artifact, readable content
  and contract bytes at that revision. A hexadecimal label alone proves no lineage. Exact dated submission record identifies proposal
  ID/revision/content, sender, commercial approver, independently cited `commercial_approval_evidence`, audience and attributable evidence
  inside the current read set. No prescribed signature ceremony: evidenced email or
  call-off can establish the parties' meaning.
- `record`: new `id`, `revision`, `status: prepared_unretained`, `entry_mode` matching
  input, exact supplied `opportunity` (nullable), `current_home` matching the input
  and `recorder` matching the actor. Never create a second current fact home.
- `events`: one per supplied observation, in its chronology; `id`, entire
  `observation` unchanged, `support`, `proposal_acceptance`, `buyer_result`, `order`,
  `work_authority`, `next_action`, `interpretation`. Each derived assessment has
  source-specific `detail`. `support` cites one or more actually permitted sources
  with exact `source_id`, `revision`, `passage`, `quote`, `href`.
The commercial approval record identifies its attributable approver, role `firm commercial approver`, exact proposal reference, approval timestamp before submission and actual/synthetic standing. Sender and approver may be distinct; the source passage must independently attribute approval.

- `proposal_acceptance`: `status` unresolved/accepted/rejected/superseded/withdrawn/
  no_proposal (if and only if there is no observed proposal reference), `proposal_ref` exact observed reference or null, `authority_basis`
  (source IDs or empty), `detail`. Acceptance requires identifiable exact submitted
  version and attributable actual-role evidence in the fictional case. Its basis
  includes a contextual direct acceptance passage for that exact revision and an
  attributable role record scoped to that proposal. A later order may cite that
  prior exact acceptance; order or role alone supplies no proposal acceptance.
  The current observation's explicit disclaimer/refusal cannot be overridden by
  another positive-looking passage. A changed
  version stays unresolved/superseded; never project the acceptance onto the newer one.
  Rejected, withdrawn and superseded require an explicit exact-subject source
  disposition, its actual role and communication/authority references; a revised
  proposal's mere existence does not declare the observed version superseded.
- `buyer_result`: `status` unresolved/recommended/won/lost/no_decision/withdrawn/
  internal, `decider` supplied actor or null, `authority_basis`, `buyer_stated_reasons`
  (exact supplied reason statements; empty if absent), `detail`. Seller withdrawal
  is attributed to the seller; silence is no buyer act. `interpretation` is a
  separately labelled `basis: firm_interpretation`, `text`, `support`; it must
  never replace a buyer's stated reasons or invent a causal/business outcome.
  Decided outcomes name the exact attributable source actor, never a nonempty
  invented name. Attributed role evidence must match that actor and its scoped role.
- `order`: `status` unknown/pending/concluded/not_applicable, `reference` exact
  concluded authorization document or null, `authority_basis`, `paperwork_next`
  with owner/date or unknown, `detail`. Pending/unknown means `pending_order: true`
  for an evidenced won buyer result; otherwise `pending_order: false`.
  A concluded order cites a contextually direct work-order or email-order act with contracting authority
  and exact parties/scope/`concluded_at`/effective date; frameworks alone cannot satisfy it.
  Order conclusion verifies contracting authority separately from current work
  limits or usage: an expired cap does not erase the historical concluded agreement. Conclusion must be dated no later than this observation and its work-effective date.
  `paperwork_next` repeats the exact supplied paperwork-record owner/date, or null
  unknowns when no evidence supplies them. A generic procurement mention names no
  individual owner or deadline. Markdown includes for each event the exact line
  `Paperwork owner: <owner or unknown>; date: <date or unknown>`.
- `work_authority`: `requested_work` unchanged or null, `status` no_request/blocked/
  covered_fictional, `primary` exact concluded work-order/internal-decision record
  or null, `risk` exact separately supplied own-risk record or null,
  `checked_at` exact observation time, `detail`. `covered_fictional` assesses only
  the scenario; it never means actual work was authorized/performed. Scope, actual
  approver/role, time/money/currency, current usage, effective period and revocation
  must cover the whole requested work. Own risk may supplement the original order
  or cover a pending-order start; risk and primary cannot be conflated. Later
  primary authorization cites `supersedes` and actual effective time, never backdates.
  Every primary/risk authority reference must be inside the current permitted source
  set and match its exact documentary authorization record. Event support includes the
  exact original grant and current consumption references with source quotes/links. Own-risk/internal records
  include `grant_evidence`, identifying the original direct authorization passage
  and self-referenced original grant record. That passage attributes its approver
  and role, names its exact ID/work/purpose/parties, numeric caps/currency, effective
  date and expiry; own-risk names its risk bearer, internal names success criteria.
  The bounded supplied wording is “<actor> authorizes <id>: … maximum/at most
  <hours> hours and <currency> <money> through <expiry>; effective from <date>”.
  Scope wording is “only an <work> at <firm> own risk” or “<work> for method
  exploration only”. A copied record cannot enlarge or alter these documentary
  bounds. A usage-only followup keeps every original grant field and the same
  `grant_evidence`; only `authority_evidence`, usage and revocation can change.
  It is an attributable current “Responsible-person report: … <hours> hours and
  <currency> <money> used as of/at <timestamp>” naming the same grant ID, not a new
  grant or extension. A responsible reporter may differ from the original approver;
  report quantities/time must match its record and follow the original effective
  date. A revoked grant cannot be reinstated by a consumption report. The original
  grant and current passage each undergo full documentary context inspection;
  denied/draft/quoted/hypothetical/conditional authorization supplies no authority,
  even with equal copied metadata or a positive older grant.
  An internal decision is primary only in internal-work; client modes require a
  work order/email order or separately bounded firm own risk. Usage is current at
  the assessment instant; older reports need an attributable no-intervening-use
  record naming the authority and coverage from report time through assessment.
- `next_action`: useful `action`, `owner`, `date` (null if unknown), `basis` evidence
  or explicitly proposed; action stays proposed. `questions`: question, settles,
  owner, date, basis; ask only decision-changing unresolved matters. No fabricated
  next date, personnel commitment, approval, order or client contact. `basis` is
  `proposed` with null date and owner null or a proposed role from relationship owner,
  commercial approver, contracting authority, internal sponsor, engagement lead,
  procurement role; it never assigns a named person. Otherwise `basis` is a nonempty
  list of exact permitted source references whose attributable `action_record`
  supplies precisely the action, owner and date, with a contextual direct “<actor> assigns <owner> to <action> by <date>” act. Draft/quoted/conditional/negated assignments create no named ownership. Questions use the same ownership
  and date rule, with their question as the action. A mentioned date alone assigns
  no deadline. These remain proposed next steps even when their ownership is sourced.
- `human_originals`: union of all exact permitted case and upstream original objects
  without projection, rewriting or loss; either order valid. `correction_flags`:
  each supplied correction unchanged plus nonempty `affected_uses`, `status: stale`;
  old versions remain fixed. This is staleness, not a changed buyer decision.
- `rights_review`: exact input read basis; exact supplied payload inventory for
  text/names/links/metadata/comments/attachments/receipts, with `assessment` and
  `status: draft_only`; one exact permission/grant per rights item plus
  `disposition` lineage_only/blocked/unresolved. Proof-use grants for a previous
  proposal permit no new audience/use. Excluded sensitive input and attachment
  text never appear in output, quotes, metadata or receipts. No unsupported claim
  may cite an unread attachment. Complete export inspection remains incomplete
  when a supplied surface is unreadable.
- `method_lanes`: exact supplied required method refs plus blocked status and
  settling step when unavailable. `limitations`: source-specific unknowns,
  sensitivity, mismatch, permission/method and actual unperformed checks.
- `dispositions`: retained/transferred/shared/submitted/record_saved/order_created/
  actual_work_authorized/work_started/upstream_invoked are false. wiki_navigation/
  original_source_inspection/native_access_enforcement/installed_agent/
  collaboration_continuity/independent_review/human_usefulness/real_client_readiness
  are not_run. `actions_performed` is empty. Business facts evidenced within a
  fictional scenario are separate from actual effects.

Markdown must carry the same lead, all event dispositions/details, exact proposal
references, source quotes/links, buyer reasons separate from interpretation, pending
order, work limits/effective dates and the exact original grant/current consumption references, next actions/questions, corrections, limitations
and internal exact human originals. Use one `## Event: <id>` section per event in exact chronology, with the observation
  timestamp and labelled `proposal_acceptance:`, `buyer_result:`, `order:` and
  `work_authority:` status/detail lines. Each event section itself carries its exact
  quotes/links, `Buyer-stated reasons:`, `Decider:` (unknown explicit),
  `Firm interpretation:`, exact proposal reference including content hash, `Pending order:
  true/false`, paperwork, authority limits, `Requested work:` (none or exact work/hours/money/currency),
  `Next action: <action>`, `Next-action owner: <owner or unknown>; date: <date or unknown>`
  and `Ownership basis: proposed` or its source link. Unknowns remain explicit.
  Later global sections carry originals, questions, corrections, rights, methods and
  limitations. Fenced/indented code, comments and a structured/JSON/correspondence annex
  cannot satisfy readable coverage. Missing, duplicate, swapped or misassociated event
  sections fail local correspondence;
an assessment hidden only in JSON is incomplete. Do not include excluded sensitive
surfaces or claim client acceptance/native readiness from these local checks.

Every derived object has exactly its declared fields; unchecked additions fail,
including contradictory effect/authority fields. `pending_order` and actual effects
are strict JSON booleans. Source objects copied exactly retain their source schema.
Nested field sets are defined above: record; event; each four-part assessment;
paperwork; action; interpretation; support (source_id/revision/passage/quote/href);
question; rights review (input_read_basis/payload_inventory/items), payload entries
(exact supplied fields plus assessment/status), rights items (permission/disposition);
corrections (exact supplied fields plus affected_uses/status); method lane
(reference/status/settling_step). No free extension container supplies a second fact.

Selected buyer outcomes must correspond to an explicit attributable source act.
The entire documentary passage governs: a matching prefix is no act when the
passage identifies it as draft/sample/illustrative language, quoted or reported
wording, hypothetical/conditional, or expressly negates/disclaims that act. This
applies to exact proposal acceptance, selection/rejection/abandonment,
recommendation, seller withdrawal, terminal proposal dispositions and concluded
orders, own-risk/internal grants and named assignments. Structured metadata and a scoped role cannot override contradictory
prose. Mere refusal of the wording supplies no initiative abandonment or loss.
Submission/commercial-approval metadata likewise cannot override an explicit
sample/draft/negation disclaimer in its source. A supported synthetic scenario
statement establishes only its fictional act; labels such as fictional scenario
only/no actual client effect are reality limits, not denials of that fictional act.

Inspect the whole passage conservatively; a recognized wording pattern alone
cannot establish an event. Unsupported paraphrases need source clarification or
human review. Check meaning independently of structural correspondence.
A concluded contracting work order records a won result even when a current work
cap expires; a role alone supplies no selection/loss/abandonment. Check exact attributable acts and authority documents independently of any
structured record; a format check cannot substitute for semantic/craft review.

## Governing requirements and limits

Apply [journey stages 3–4](../../../runtime/requirements.md#business-lifecycle),
[Opportunity, Proposal, Agreement Reference and Decision meanings](../../../runtime/requirements.md#business-records),
[decisions](../../../runtime/requirements.md#human-decisions) and
[knowledge boundaries](../../../runtime/requirements.md#evidence-and-knowledge).
Preserve exact-version submission and authority evidence, distinct buyer/order/work
facts, current consumption proof, correction history, all-owner permissions and
human originals. A geography/sector/service example establishes no law or actual
firm profile. Fictional authorization remains fictional; actual work requires the
current attributable authority and supported authorized operation.
