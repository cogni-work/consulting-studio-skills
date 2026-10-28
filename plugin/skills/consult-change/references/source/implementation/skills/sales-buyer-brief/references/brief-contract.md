
<!-- Consulting Studio packaging modification, 2026-10-28: local resource locators and explicit governing reads; canonical source and emitted hashes in distribution.json. Owner-approved S1.1.0 Apache/NOTICE overlay; existing recipient grants retained. -->
# Buyer brief contract 0.1.0

Apply [Deliverable mode and home](../../../runtime/storage-lifecycle.md#deliverable-mode-and-home)
early and carry its selected mode/home, exact version and actual state into the
handoff. This does not expand read-only/preparation scope or business authority;
a retained copy needs its own applicable instruction and save/readback/final link.

Prepare a readable draft and exact-revision handoff. Ordinary work may use sections
of one brief. When a structured handoff is useful, preserve the fields below with
matching readable content. A draft creates no authoritative business record;
retention requires a separately authorized supported save and readback.

## Readable content and lineage

Lead with the buyer situation at its evidenced strength and the next human question
or decision. Preserve the problem in the buyer's words, why now, cost of inaction
or unknown, confirmation, alternatives and criteria. Show who said what, whose view
was reported, stakeholder positions and authority, promises, assumptions, dissent,
unresolved conflicts and next moves. Every next move/question has owner/date or
explicit `unknown`; proposed owners/dates must be labelled proposed rather than
silently assigned. Important unanswered questions take priority over generic intake.

Keep exact source revisions/passages and read coverage beside substantive evidence.
Use browsable source-record/version/passage links in an authorized wiki where
available. A local Markdown link establishes correspondence only; inspect the
original source and separately test intended-reader navigation before claiming
those checks passed. An original locator and source ID alone prove neither. Do not copy
restricted sources or broaden access to repair navigation.

## Structured handoff fields

The output has `skill`, `version`, `case_id`, `brief`, `input_sha256`, `target`,
`sources_read`, `statements`, `stakeholders`, `criteria`, `alternatives`, `promises`,
`assumptions`, `human_originals`, `conflicts`, `measurements`, `buyer_events`,
`corrections`, `questions`, `handoff`, `limitations`, `dispositions` and
`actions_performed`. Lists may be empty only when their inputs are absent; explain
material gaps in the brief. Do not put evaluator criteria into the buyer's mouth.

- `brief`: stable `id`, new exact `revision`, `status: draft`, `relationship_owner`,
  `audience`, `purpose`, `need`, `why_now`, `cost_of_inaction`, `confirmation` and
  `relationship_owner_decision`. Unsupplied confirmation/decision remains unknown
  or pending; human-supplied decisions are attributable, not assistant choices.
- `input_sha256`: exact hashes of files actually supplied for this case. Source,
  target/requirement identity and operation receipts remain separate evidence.
- `sources_read`: `source_id`, `revision`, `coverage`, `omissions`; match the supplied
  coverage. Retained passage inspection is not full inspection of an original report.
- `statements`: one record per selected substantive buyer/firm statement, with
  `source_id`, `revision`, `passage`, exact `quote`, `speaker`, `reporter`, `subject`,
  `basis`, `confirmation`, `causal_status` and `href`. `basis` distinguishes stated,
  reported, documentary, assumed and inferred; quotations never prove their cause.
- `stakeholders`: supplied `id`, `role`, `position`, `statement_refs`, `authority`
  (status, evidence or unknown), and `next_move` (action, owner, date, basis).
  Keep a supplied role distinct from contracting/decision authority.
- `criteria`: exact `id`, `wording`, `source_id`, `revision`, `passage`, `status`,
  `score`, `conditions`, `confirmation` and `href`. Status is preference, mandatory,
  scored or unconfirmed. Retain absent scores as null; quoted selection criteria
  are not success proof. This list and the brief ID/revision form the offering-proof interface.
- `alternatives`, `promises`, `assumptions`: preserve supplied objects with their
  status and exact source references. Separate a promised draft meeting question
  from a delivery commitment. Missing cost, authority or comparability may become
  explicit assumptions/questions; no invented fee, savings, credential or commitment.
- `human_originals`: exact `id`, `revision`, `passage`, `author`, `text`, `href` for
  each permitted supplied note/dissent. Keep history alongside the latest note.
- `conflicts`: identify competing exact references, what is unresolved and a
  settling question. Do not erase a local position or use majority voice as authority.
- `measurements`: preserve each supplied metric's `id`, `value`, `unit`, `population`,
  `period`, `entity`, `source_id`, `revision`, `passage` and `limitations` exactly.
  Unknown maps/conversions stay missing; produce no fabricated group total/average.
- `buyer_events`: supplied exact event references/quotes plus `kind`,
  `decision_authority`, `proposal_acceptance`, `order_status`, `reason_basis` and
  `interpretation`. Recommendation/rejection/silence remain distinct. An attributable
  rejection may be preserved as reported without verifying contracting authority;
  do not change an opportunity or infer an order. Unknown facts stay unknown.
  For this structured profile, `kind` uses recommendation/reported_rejection/silence,
  `order_status` uses not_established/unknown and `reason_basis` uses stated/absent.
  These enums describe provenance/state distinctions; the assistant writes its own
  source-specific interpretation and limitations.
- `corrections`: exact old/new source references, `affected_brief_revision`,
  `affected_criteria`, `effect` and `history_preserved`. Keep original source/brief
  references; new text flags dependencies stale without overwriting them.
- `questions`: `id`, `question`, `settles`, `owner`, `date`, `basis`. Unknown owners
  and dates are explicit; supplied next-move ownership is not a guess at the decider.
- `handoff`: exact `brief_id`, `brief_revision`, `criteria_ids`, unresolved criterion
  IDs and `authority: draft only; no transfer or business decision`. A supplied
  criterion set can enter offering-proof directly without invoking this skill.
- `limitations`: include read/permission gaps and blocked tailoring by affected lane,
  with the exact missing reference and settling step. Do not claim to apply an
  unread required method or invent a substitute.
- `dispositions`: `retained`, `submitted`, `buyer_decision_recorded`,
  `order_created`, `work_authorized` are false for this draft-only profile;
  `wiki_navigation`, `original_source_inspection`, `native_access_enforcement`,
  `installed_agent`, `collaboration_continuity`, `independent_review`,
  `human_usefulness`, `real_client_readiness` are `not_run`. `actions_performed` is
  empty. Record only performed checks in their own receipts; a self-check is never
  an independent verdict. Keep unperformed checks `not_run`.

## Governing requirements and limits

Apply [journey stages 1–3](../../../runtime/requirements.md#business-lifecycle),
[commercial objects](../../../runtime/requirements.md#business-records),
[decisions](../../../runtime/requirements.md#human-decisions) and
[knowledge and evidence](../../../runtime/requirements.md#evidence-and-knowledge).
Preserve buyer attribution, criteria, correction history, permissions, current
requirements and human authority. Illustrative geography/sector/service choices
establish no law or firm mandate. Prior scoping, research or retained knowledge
establishes no buyer outcome, proof reuse right or current operating capability.
