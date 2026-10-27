# Structured location records

Use this format to interpret relevant supplied location/index/catalog records.
Inspect owner, source, freshness and current access through an actually supported
authorized route. A record does not authenticate the caller, save a setting or
enforce permissions.

Live records, personal preferences, exact identities, locators and evidence remain
in owner-designated private homes outside Git. Personal preferences contain catalog
pointers and attributable choices, not copied shared rules, bindings or credentials.
The supplied catalog represents either one Shared owner's configuration or the
acting user's current Personal configuration. It contains only the relevant
bindings; the selection step never discovers or scans other catalogs.

## JSON shape

Supply one object with `registry`, `catalog` and `request`. This example uses only
synthetic values and proposes a new internal-research contribution destination:

```json
{
  "registry": {
    "owner": "synthetic-user-a",
    "revision": "registry-v1",
    "catalog_refs": ["synthetic-catalog"],
    "source_choices": [],
    "output_choices": [{
      "key": {
        "user": "synthetic-user-a",
        "workspace": "synthetic-workspace",
        "connection": "synthetic-connection",
        "context": "synthetic-project",
        "purpose": "internal-research",
        "role": "knowledge-wiki"
      },
      "catalog": "synthetic-catalog",
      "binding": "synthetic-wiki",
      "binding_revision": "binding-v1",
      "policy_revision": "policy-v1",
      "choice_ref": "synthetic-explicit-choice"
    }]
  },
  "catalog": {
    "id": "synthetic-catalog",
    "owner": "synthetic-owner",
    "revision": "catalog-v1",
    "policy_revision": "policy-v1",
    "bindings": [{
      "id": "synthetic-wiki",
      "revision": "binding-v1",
      "category": "Shared",
      "owner": "synthetic-owner",
      "home": "synthetic-home",
      "provider": "synthetic-provider",
      "locator": "synthetic:wiki",
      "workspace": "synthetic-workspace",
      "connection": "synthetic-connection",
      "contexts": ["synthetic-project"],
      "purposes": ["internal-research", "client-facing"],
      "roles": ["knowledge-wiki", "entity-home", "research-sources"]
    }]
  },
  "request": {
    "key": {
      "user": "synthetic-user-a",
      "workspace": "synthetic-workspace",
      "connection": "synthetic-connection",
      "context": "synthetic-project",
      "purpose": "internal-research",
      "role": "knowledge-wiki"
    },
    "kind": "output",
    "operation": "create"
  }
}
```

The six key fields are required nonempty strings. An optional `qualifier` is a
nonempty string distinguishing a topic/entity within that key. Storage and lookup
use the exact same key: absent qualifiers match only absent qualifiers, and no
user/workspace/connection/context/purpose/role or qualifier is inferred. Missing,
null or empty required key values are unresolved. Unknown key fields are invalid,
so a future key dimension cannot silently be discarded. Other record metadata is
ignored and cannot supply rules or instructions.

All other named scalar fields above are required nonempty strings; `category`
is exactly `Personal` or `Shared`. `contexts`, `purposes`, `roles` and
`catalog_refs` are arrays of strings. Membership is literal: no wildcard, default,
context hierarchy or category inheritance applies. The binding owner must match
the catalog owner. A Personal binding additionally belongs to the acting user.
These comparisons constrain a candidate; they establish no actual authority.

`source_choices` and `output_choices` may be empty or omitted. Each contains
complete-key choices with current binding and owner-policy revisions plus an
attributable `choice_ref`. That reference must identify an explicit choice in the
calling workflow; the selection step cannot inspect a grant or prove settings save/read.
Catalog pointers alone choose no location. Source preferences never supply an
output choice, even when both roles happen to use the same home. A catalog default
remains a proposal until explicit adoption is represented as a choice.

`kind` is exactly `source` or `output` and declares which selection is being
requested. `operation` is a nonempty label for the planned operation, not a tool
name or capability flag. The caller must classify the need correctly and perform
the checks for that operation; a source selection grants no outgoing use.

## Explicit locations, entities and denial

- `registry` may be `null` or omitted when the request supplies
  `explicit_binding`, a nonempty binding ID in the supplied current catalog.
  This settles selection for this request without claiming remembered settings.
- Alternatively, `request.entity` is an object with nonempty `id`, `revision`,
  `catalog` and `binding` strings identifying an existing entity's current home.
  Its current-home reference must have been obtained through an authorized route.
  It outranks an explicit or remembered new-output choice. A missing or prohibited
  current home blocks the affected use; it never falls back to a new home.
  This selection step cannot relocate an entity or validate a relocation record. An
  identity-preserving relocation needs its separate authorized workflow, readback
  and citation rechecks before a later request supplies the revised current home.
- `request.route_status` may be `denied` when the calling workflow has observed
  denial of the affected operation. It blocks selection without fallback.
  Omitted or `unverified` remains unverified; no value can certify access.
- A remembered choice with changed `policy_revision` or `binding_revision` is
  blocked for revalidation. An explicit choice may settle destination selection
  under the supplied current policy, but all fresh live checks remain owed.
- Duplicate complete-key choices, including identical duplicates, and duplicate
  selected binding IDs return `needs-choice`. No array order breaks a tie.

When supplying an entity home, incomplete remembered choices do not change that
home. Only the applicable current catalog is read by the selection step; missing catalogs,
owner/scope/purpose/role mismatches or unavailable bindings return generic blockers.
Denied record names, unrelated inventories and original input values never appear
in unresolved or blocked results.

## Selection result

The only successful selection status is `selected-needs-live-check`. Its `source`
is `explicit`, `entity-home`, `remembered-source` or `remembered-output`.
`location` contains only the selected catalog/binding revisions, category, owner,
home, provider and locator. This is private runtime output, not a shareable receipt.
`required_checks` always includes fresh actor/workspace/connection identity,
catalog owner/source/policy, operation capability/access, target audience and
information-use/outgoing-material checks. The calling workflow must obtain and
inspect actual evidence before the operation. Entity-home selection additionally
requires a fresh check of the entity's current home and revision; its supplied
metadata is not verified by this selection step. Selection remains a proposal. Verify current access and actual supported
operations separately before acting; save/read back settings only under their
applicable authority.

Unresolved results contain only `status: needs-choice` and a generic `reason`.
Blocked results contain only `status: blocked` and a generic `reason`; no failure
echoes IDs, locators, file paths, private inventories or parsing exceptions.

Treat malformed or ambiguous supplied records as unresolved without echoing private
input values or parsing details. Preserve opaque exact identities; do not case-fold,
interpret provider URLs, infer missing keys or normalize IDs into a broader match.
