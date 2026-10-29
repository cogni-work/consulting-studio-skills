# Evidence-check contract 0.1.1

Apply [Deliverable mode and home](../../../runtime/storage-lifecycle.md#deliverable-mode-and-home)
early and carry its selected mode/home, exact version and actual state into the
handoff. This does not expand read-only/preparation scope or business authority;
a retained copy needs its own applicable instruction and save/readback/final link.

The skill consumes an exact draft, permitted versioned passages, their coverage/use
basis, human originals and criteria. Its report is a read-only review preparation.
It never mutates the checked draft or decisions. Supplied inputs need no upstream
skill execution or live binding discovery.

Return a readable report. When a structured report is requested, use the following
meanings without assuming a provider API or persistence schema.

- `skill`, `version`, `case_id`, `draft`, `context`, `input_sha256` and `freeze_sha256`
  bind exact skill identity, copied draft/context and input bytes. Include case and
  freeze identities only when supplied; do not invent them.
- `summary` gives decision-changing findings. `inventory` contains one row per
  supplied draft unit, including original `unit_id`, `text`, `kind` and `citations`.
  Inventory the complete declared draft scope; compound parts must all be
  assessed in `reason` and may not be silently dropped.
- Each row has `status` (supported/misworded/partial/unsupported/contradicted/unresolved),
  `basis`, `reason`, `proposed_correction` (null when none), `settling_input` (null
  when none), `decision_owner` (supplied owner or null), and `arithmetic` (list of
  `{expression, operands, result, unit, scope, limitation}` or empty).
- `citation_checks` contains one entry per original citation, in original order:
  copied `citation`, `format_target` (resolved_local/unresolved), `semantic`
  (supports/partial/does_not_support/not_checked) and `reason`.
- `evidence` and `contrary_evidence` are lists of exact `{source_id, revision,
  passage, quote, href}`. Use only currently permitted sources. `href` identifies
  the actual readable source record and exact revision/passage. Additional useful passages do not repair
  the original citation's semantic verdict. Old and corrected source versions stay
  distinct. No source quote is invented for an inaccessible target.
- `human_originals` copies permitted original objects verbatim. `source_coverage`
  lists only permitted source objects with exact `source_id`, `revision`, `coverage`
  and `omissions`. `exclusions` identifies the preserved human-note annex as outside
  the evidence-claim inventory. `gaps` describes unsettled work without exposing
  denied inventories; `untrusted_content` records a non-disclosing instruction concern.
- `navigation` records `format_scope`, `actual_wiki_navigation`,
  `native_access_enforcement` and `reason` at their actually observed scope.
  Unobserved navigation, access enforcement and original-report inspection stay
  `not_run`. A supplied permission declaration is not observed provider enforcement.
- `effects` sets draft_modified/research_invoked/retained_live/transferred/sent/
  approved/released to false. `review` sets `author_self_check: performed`,
  `independent_review: not_run`, `human_acceptance: not_run` at execution time.

Readable reports must expose every original unit and original citation, judgment,
reason, basis, proposed correction/settling input, arithmetic, evidence/contrary
quotes and local links, read coverage/omissions, notes, exclusions, gaps and all
navigation/review/effect limits. Preserve decision-changing qualifications in the
main findings; do not hide them behind structured receipts. Mechanical correspondence
and boundary checks cannot certify semantic truth or actual navigation.

Verify authorized wiki navigation as the intended reader in the actual rendered
output. Keep source/craft review and human acceptance separate, bound to the exact
draft/report versions and evidence inspected.
