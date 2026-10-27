# Provider operations

Use only tools exposed in the current session. Inspect their current schemas and
actual resource access before applying the relevant procedure below. If an operation
is absent or its contract differs, stop that operation and return the precise gap;
continue useful permitted independent work.

## Library files

Use the existing Library skill and its current authorized tools and helpers; this
guide implements no upload or Library integration. Apply the shared
[Library saving and document handoff](../../../runtime/storage-lifecycle.md#library-saving-and-document-handoff)
contract. Preserve exact returned identities and actual versions; create a new item
only when no identity exists or a separate copy is explicitly requested and authorized.
An unresolved earlier create must first be reconciled. For the agreed reopen test,
read the exact returned Library identity separately and compare meaningful remote
content. Search can lag and is not that verification gate. Keep actual user opening
of the offered supported reference separate from tool readback. Library saving needs
no complete Studio Setup, Pages tree or project adoption. Settings-dependent work
still uses the existing bounded Librarian discovery procedure.

## Pages and Spaces

Bootstrap from an exact Page ID or user-designated private index. A Space ID and
its root Page ID are different: use get_space for the root, then read_page.
Before creating a child, read its actual parent/root and applicable instructions;
search only that selected home for a Page serving the same entity/revision purpose.

For new homes, create_space has no exposed creation idempotency key. Retain its
result immediately and reconcile an uncertain outcome before another creation.
Creating an owner-only project home supplies no collaborator grant. Inspect effective
sharing, including completeness and inherited sources, before relying on its audience.

read_page with editing view returns canonical blocks, IDs and hashes. Retain the
structured result. Carry metadata.stream_kind into edits and later reads; use content
for normal wiki work. Copy content.through_sequence as base_sequence only when
returned; metadata.current_sequence is not an edit guard.

Use create_page under the selected space_id or parent_page_id for versioned candidates.
The returned page_id and URL address that Page, not a guaranteed immutable revision.
Persist business revision metadata and exact source block IDs/hashes. Source/version
navigation and recoverability still need observation. Never invent a historical URL.

For edits, use edit_page or patch_page with observed block IDs and expected_hash.
Non-patch batches are atomic; patches may partially commit. Check every operation,
commit_status and ignored_reason. A block_deleted no-op is not a successful content
change. For a hash conflict, reread and rebuild only rejected edits; for an unknown
commit, inspect state before retrying. Never replay already-applied operations.

A same-actor test can retain a baseline hash, apply a guarded update, then attempt a
synthetic stale update on a designated test block. Confirm rejection and preservation.
Label that narrowly; it is not evidence of two collaborators editing concurrently.

Create accepted synthesis as a new revision only after the curator's exact decision.
Preserve the original candidate and earlier revision. Store the current-revision
reference in the authorized registry/catalog through a guarded settings edit.
That pointer change must not rewrite the old knowledge records.

## SharePoint

Use the owner's exact folder/library/item URL. Search within the supplied relevant
scope where supported; broad inventory discovery is not bootstrap. Inspect current
item permissions and versions through exposed tools and respect incomplete visibility.

Separate search, read, create and update capability. A profile call alone proves no
specific folder access, write route or retention authority. Inspect the selected
source's information-use basis before copying it into a Page.

The exposed update_file_exact replaces an entire file. Its current schema provides
no conditional revision/ETag write guard. Do not use it to overwrite a collaborative
wiki and claim conflict protection. Prefer an authorized new versioned contribution
or controlled owner incorporation when a safe update route is unavailable.

For creation/upload, use the actual file reference format supported on this host and
the exact target returned by the connector. Retain receipts and inspect readback.
A local file path or successful upload receipt alone is not cross-host proof.

## Sites

A deployed Site URL is not itself an entity store. Establish the actual record
service, identity/audience and demonstrated write tool before selecting it as a home.
Site/database inspection does not establish create/update support. Select Sites only when its actual record service and authorized operations satisfy
the requested task. A view URL does not establish a usable knowledge home.
