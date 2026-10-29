# Proof selection contract 0.1.0

Apply [Deliverable mode and home](../../../runtime/storage-lifecycle.md#deliverable-mode-and-home)
early and carry its selected mode/home, exact version and actual state into the
handoff. This does not expand read-only/preparation scope or business authority;
a retained copy needs its own applicable instruction and save/readback/final link.

Prepare a readable proof-selection draft. Use the structured fields below when an
exact handoff is useful; keep matching readable content. Record the actual scope
of inspection and do not infer a storage operation from the handoff format.

Lead with the proposed fit and decisive limitations, and the human next decision.
Each substantive claim has an authorized browsable wiki source record with exact
revision/passage, read coverage and original locator where permitted. Local links
test passage correspondence only. Test rendered intended-reader navigation through
the currently authorized route; leave it `not_run` until observed. Do not copy
restricted source content to repair a link.

## Structured handoff fields

- `skill`, `version`, `case_id`, `synthetic`, `input_sha256`, `target`: identify
  the exact method, case and supplied files. Synthetic examples select no actual
  instance target. Input hashes and source/operation receipts remain separate.
- `context`: exact actor, draft audience, outgoing audience, purpose, observation date,
  relationship owner and offering owner from the case. `selection_status: draft`.
- `criteria_binding`: exact case `criteria_binding` object, including artifact and
  criteria digests for sales-buyer-brief or direct supplied-criteria provenance. `criteria`: entire
  exact case list, including wording/status/provenance; no changed score or invented
  requirement. Keep ordinary and tender input variants distinct.
- `upstream_context`: for sales-buyer-brief cases preserve the supplied `corrections`,
  `human_originals`, `measurements`, `historical_supplied_brief` when present and
  `limitations` from that exact artifact. Mark any current dependent uses stale;
  old references remain intact. Direct input has no fabricated brief or invocation.
- `candidates`: one record per requested candidate, with `candidate_id`,
  `disposition` (selected/excluded/unresolved), `use`, `read_status`
  (read/blocked), `support` (exact source_id/revision/passage/quote/href for each
  supplied passage actually read), `currency`, `read_coverage`, `omissions`,
  `criterion_ids`, assistant-written `relevance`, `relevance_gaps`, `limitations`,
  `owner_checks`, and `settling_step` (action, owner, date). Nonempty relevance,
  gap/limit and settling prose is source-specific, never a prescribed answer.
  Readable candidates retain supporting coverage even when outgoing use is blocked.
  A denied-read candidate has empty support, `read_coverage: not_read`, no source
  identity/locator/text in the ledger and a generic blocker. Unselected sources stay
  in their authorized homes. `owner_checks` repeats each case grant exactly and adds
  `current_state` and `use_status` (permitted/blocked/unresolved); no missing owner.
  Selection requires permitted source read and every required owner's current scoped
  grant. A permissible anonymous use does not enable a named or reference-call use.
- `sources_read`: exact source_id/revision/coverage/omissions for only read sources.
- `contrary_evidence`: exact supplied contrary references and executor interpretation
  with bounds. `correction_flags`: old/new references, affected dependent revisions,
  stale status and required human disposition; preserve all supplied correction data.
- `human_originals`: exact supplied proof-shelf notes, plus upstream originals where
  present, with authored attribution. Preserve originals separately from interpretation.
- `payload_inspection`: one entry per supplied surface ID, retaining surface kind,
  inspectability, owner IDs and `disposition` (include/omit/blocked), with a specific
  reason. Inspection covers text, names, links, metadata, comments, attachments and
  receipts. Do not emit prohibited surface values merely to explain their omission.
- `client_preview`: `status` (draft_safe_subset/blocked_for_transfer), `surfaces`
  (surface_id/kind/content, only included permitted surfaces), `omitted_surface_ids`
  and `blocked_surface_ids`. A safe subset contains no uninspectable or disallowed
  surfaces. All grant restrictions apply to content as well as shell labels. A
  blocked preview may contain inspectable draft content but is expressly blocked
  as a complete payload; it must never be called complete-safe. Permission safety
  and operational transfer authorization are separate: both preview statuses remain
  unsubmitted and transfer is false.
- `method_lanes`: when required method is unsupplied, exact reference/status and
  blocked tailored lane with settling step; permitted common lane may remain draft.
- `questions`: question, settles, owner/date (supplied or unknown), basis.
- `decisions`: relationship and offering choices remain pending human decisions.
- `dispositions`: retained/transferred/submitted/offer_adopted/reference_contacted/
  order_created/work_authorized false; wiki_navigation/original_source_inspection/
  native_access_enforcement/installed_agent/collaboration_continuity/independent_review/
  human_usefulness/real_client_readiness not_run. `actions_performed: []`.

For synthetic examples, permission observations describe fictional grants only.
Actual transfer needs current sender/receiver/operation authority and demonstrated
access. Local output files or a permission ledger do not establish enforcement.

## Governing requirements and limits

Apply [journey stages 2, 3 and 8](../../../runtime/requirements.md#business-lifecycle) for
permitted proof, CV permission and offering ownership; [objects](../../../runtime/requirements.md#business-records)
for Source, Claim, Evidence Permission and Handoff; and
[decisions](../../../runtime/requirements.md#human-decisions) for separate access,
permission, transfer and business authority. Follow [reuse, revocation and exit](../../../runtime/storage-lifecycle.md#reuse-revocation-and-exit):
check every owner, inspect complete outgoing surfaces and preserve bounded reuse.
Prior scoping, research or retained knowledge grants no success claim or permission.
