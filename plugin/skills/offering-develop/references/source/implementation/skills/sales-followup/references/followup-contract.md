
<!-- Consulting Studio packaging modification, 2026-10-29: local resource locators and explicit governing reads; exact canonical and emitted hashes retained in distribution.json. S1.2.1 public release continues the existing Apache-2.0 S terms; recipient grants retained. -->
# Follow-up contract 0.1.0

Apply [Deliverable mode and home](../../../runtime/storage-lifecycle.md#deliverable-mode-and-home)
early and carry its selected mode/home, exact version and actual state into the
handoff. This does not expand read-only/preparation scope or business authority;
a retained copy needs its own applicable instruction and save/readback/final link.

Prepare a short readable document or action table from permitted records. Use the
structured fields below when an exact handoff is useful, with matching readable
content. A draft does not update an authoritative relationship store.

Lead with the next useful human action or unresolved choice. Keep relationship,
need, source/version/passage, accountable owner, action owner, next action and
known/unknown date visible. Explicit proposed choices remain separate from supplied
facts. Preserve original need, delivery lineage, human wording/dissent and supplied
prior follow-up history. No opportunity or commitment arises from a draft.

## Structured handoff shape

Top-level fields: `skill`, `version`, `case_id`, `summary`, `as_of`, `target`,
`input_sha256`, `freeze_sha256`, `source_coverage`, `followups`, `human_originals`,
`limitations`, `effects`, `gates`. Interpret the actual evidence and ask questions
that settle the specific missing action, owner, date or disposition.

- `source_coverage`: exactly the case's requested source revisions, status and
  coverage/omissions; denied/unsupplied sources have no content and are not read.
- `followups`: one per supplied `id`, with new `draft_revision`, exact `prior`
  supplied record, `relationship_id`, `need` (exact supplied object), `origin`,
  `relationship_owner`, `action_owner`, `next_action`, `date`, `renewal_dates`,
  `status`, `date_status`, `last_meaningful_update`, `evidence`, `act_assessments`,
  `proposed_next_action`, `settling_question`, `limitations` and `opportunity_ref`.
  `origin` and `opportunity_ref` preserve supplied links/null, not invented entities.
  Each owner/action/date has `value` and `basis` (`supplied`, `unknown`, `proposed`);
  unknown is the literal string `unknown`. Supplied facts name exact evidence in
  `evidence`. Suggestions belong in `proposed_next_action`; no human act is implied.
- `evidence`: `source_id`, `revision`, `passage`, exact `quote` and local `href`.
  Substantive supplied facts and dispositions cite the permitted supporting passages.
  Local links test correspondence only. Check actual intended-reader navigation
  and original-message inspection separately before claiming they passed.
- `status`: `open`, `completed`, `dismissed`, `linked` or `unresolved`. It describes
  a draft's reading of supplied evidence. `prior` remains unchanged. A supplied
  terminal state stays terminal; distinct needs use distinct supplied identities.
  Completion/dismissal cannot be guessed. Assess each supplied candidate act with
  exact `id`, `supports_update` boolean and source-specific `reason`; a positive
  assessment needs matching follow-up/action revision and an occurred act no later
  than `as_of`. Completion cites the action owner's actual fulfilled action, or
  the relationship owner's attributable report of its occurrence. Dismissal cites
  the relationship owner's disposition with a reason. Unknown/conflicting attribution
  remains unresolved; no universal legal/commercial authority model is introduced.
- `date_status`: `overdue`, `upcoming`, `undated` or `inactive`, derived only from
  the evidenced next-action date, observation date and current state. Renewal end
  and notice dates stay in exact `renewal_dates`; never use them as action dates.
- `last_meaningful_update`: date and exact evidence for the latest evidenced
  business event within supplied coverage; not generation time. State/date changes
  identify their supporting act. Prior dates and act times remain independently
  inspectable. This limited view establishes no full relationship freshness.
- `human_originals`: exact permitted case objects (author, revision, text, source
  and audience). Private notes outside the output's audience are omitted, with no
  quoted content or leaked inventory; originals remain in their owning home.
- `limitations`: concrete missing facts/affected lane and settling step; distinguish
  known coverage from full history. Unavailable material prevents unsupported
  attribution/updates, not unrelated supplied drafting.
- `effects`: `sent`, `scheduled`, `crm_written`, `record_written`, `opportunity_created`,
  `work_authorized`, `scope_changed`, `retained_live`, `settings_changed`, `deployed`
  are false for this draft-only profile. Recording a previously reported sent act
  does not mean this task sent a message. `gates`: `native_navigation`, `native_access_enforcement`,
  `native_retention`, `installed_agent`, `collaboration_continuity`,
  `human_usefulness`, `real_client_readiness`, `independent_review` are `not_run`.
  Record actual checks and independent review separately against exact source and
  output revisions; a self-check never becomes an independent verdict.

## Governing sources and interface

Apply [journey stages 1, 3 and 7](../../../runtime/requirements.md#business-lifecycle),
[relationship objects and record discipline](../../../runtime/requirements.md#business-records),
[authority/lifecycle](../../../runtime/requirements.md#human-decisions) and
[knowledge boundaries](../../../runtime/requirements.md#evidence-and-knowledge).
Follow-up/Need identities, owners, original source lineage, action/date, status and
business-update time form the [sales-monday-review](../../sales-monday-review/procedure.md)
read-time handoff. No pursuit-event invocation is required. Use only current
authorized source/storage operations. An illustrative sector or service context
establishes no law, adopted governance or client-material reuse permission.
