# Delivered skill presentation

[Issue 228](https://github.com/cogni-work/consulting-studio/issues/228) includes
owner-requested packaging corrections: a skill's actual `display_name` must equal
its technical frontmatter `name`, and skills must contain no generated packaging
commentary or nonfunctional build-origin breadcrumbs. The rule covers every
instruction and nested reference in each delivered S, App and M skills tree.
Functional method resource links, substantive methods, human notes, evidence
lineage requirements and useful descriptions remain unchanged.

[content.py](content.py) provides a Python standard-library finalizer and a separate
validator. Call the finalizer only on a complete generated package payload, before
computing final distribution and archive hashes:

```python
clean_files, evidence = content.finalize(files, profile='S')
coverage = content.validate(clean_files)
```

`files` maps package-relative paths to bytes. Profiles are `S`, `App` and `M`.
Both `skills/<technical-name>/...` and `m/skills/<technical-name>/...` are covered;
a package may contain several skills. Only root `SKILL.md` files register actual
entries. A supporting `procedure.md` is an instruction resource, not another
entry. Missing explicit display metadata uses the technical name; every present
entry-frontmatter or interface `display_name` must match exactly. An existing
interface description and invocation policy are preserved.

## Corrections and external records

The finalizer removes only the enumerated exact generated HTML blocks and exact
`distribution_modification_notice` JSON values. It does not delete arbitrary
comments or rewrite prose heuristically. A new or altered prohibited form fails
validation and needs a specific source correction. Exact removed text, input and
output hashes, affected paths, profile and transformations are returned as
`consulting-studio/skill-presentation@1` evidence outside the skills tree.

Generated root skill `manifest.json` records move to
`metadata/skills/<technical-name>/manifest.json`. Their original hash is retained;
resource and file paths are rebased against an explicit `payload_root` and hashes
are recalculated against the clean payload. Functional instruction resources stay
at their existing paths. Exact `LICENSE` and `NOTICE` payloads within each skill
move to `legal/skills/<technical-name>/` preserving their relative suffix and bytes.
The M equivalents remain under `m/metadata/` and `m/legal/`. Collisions and missing
referenced payloads reject the build. These are technical relocations, not a new
license grant or a conclusion about file-specific obligations.

The caller must update outer distribution mappings using `evidence['relocations']`,
recompute all final package inventories and hashes, and retain `evidence` outside
the skills tree. The finalizer does not mutate its input mapping. Historical
published packages and canonical rebuild inputs are not passed through this
operation or silently rewritten.

## Build and CI rejection boundary

The validator scans the complete UTF-8 skills closure, including Markdown, YAML,
plain text and recursively decoded JSON keys and strings. Unexpected binary
content, duplicate JSON keys, orphan skill content and malformed entries fail
rather than receiving an incomplete scan result. Legal and metadata homes outside
the skills tree remain inspectable package records.

The finite prohibited classes include:

- Consulting Studio packaging modification commentary, including altered wording.
- Build/packaging origin, provenance, history, breadcrumb and meta-comment labels.
- Source-origin labels and generated, packaged or derived-from origin prose.
- Nonfunctional canonical repository issue, pull request, commit, tree and blob
  breadcrumbs, and labelled original implementation paths.
- Structured source commit/tree/repository, generator, canonical-path/hash and
  packaging-origin metadata, including nested and alternate key formatting.

Unicode normalization, standard HTML entities, JSON escapes, common Markdown
formatting and zero-width separators are normalized before applying the defined
rules. The gate does not claim to identify every possible natural-language
paraphrase. It does not forbid ordinary business evidence provenance or functioning
relative resource navigation merely because they use the words source or version.
Meaningful unrelated comments and human dissent remain permitted.

The [regression suite](../tests/test_skill_presentation.py) injects defined
prohibited classes in entries, deeply nested references, JSON objects and decoded
strings across S, App and M layouts. It also checks exact permitted cleanup,
display names, retained descriptions/policy, legal-record relocation and refreshed
hashes, functional links, human notes, malformed inputs and full-entry coverage.
The suite is discovered by the repository's full validation tier. Actual builders
call the same validator after final composition and before emission: `prepare.py`
for S/App, and `release-candidate/current.py` for M and its exact S sibling.
The artifact regression suite builds the real S/App closure; the M boundary suite
checks lifecycle/inventory regeneration and rejection in the composed archive.
A test of source text alone does not certify generated bytes.

```sh
python3 -B -m unittest discover -s implementation/tests -p test_skill_presentation.py
```

## Current unpublished candidates

[prepare.py](prepare.py) emits S1.2.2 as `consulting-studio-skills.zip`, its finite
standalone rebuild snapshot, distribution, selection and checksums. Its optional
private App1.1.1 source input produces a complete App1.1.2 inspection candidate;
all prior App instructions are compared after only the defined presentation
corrections, and unexplained adaptations reject. App binding/settings remain exact
except the package version. This is a complete candidate, not an installed update
or an assertion that an importer supports the metadata relocation.

```sh
python3 -B implementation/skill-presentation/prepare.py --source-commit FULL_COMMIT --output ../s-candidate
python3 -B implementation/skill-presentation/prepare.py --source-commit FULL_COMMIT --app-source /absolute/private-app-source.zip --output ../app-candidate
python3 -B implementation/release-candidate/current.py --source-commit FULL_COMMIT --dependencies /absolute/existing/node_modules --output ../sm-candidate
python3 -B implementation/ci/run.py --tier full
```

Pin the complete clean committed source after review. All93 selected canonical
resources must also match that commit, and all active tooling hashes are retained.
M1.1.2 recompiles its existing GUI/MCP source twice in isolated source/dependency
copies, retains complete external third-party texts and consumes the same corrected
S archive. It does not install dependencies or access a live endpoint. Existing
M rights/source-origin qualifications outside the instruction tree retain their
separate meanings; instruction cleanup supplies no software-rights approval.

The earlier aligned and S-distribution CLI routes refuse new builds. Explicit
finite historical rebuild replays remain evidence only. Published S1.2.1 and
private App1.1.1 are not replaced; their package versions, hashes and source pins
remain historical. The new candidates carry no historical release authorization.

Content validation and reproducible local artifacts establish neither actual host
invocation nor installed readiness. In particular, Setup visibility is distinct
from chat/onboarding routing. Publication, deployment, installation, release
adoption and owner acceptance retain their separate applicable authority.
