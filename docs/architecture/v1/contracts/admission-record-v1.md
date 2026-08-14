---
type: contract
related-project: Brep2Code
version: v1
status: active
---

# Contract: Immutable Admission Record v1

An admission record is a versioned, source-hash-bound development-side evidence
artifact. It states why one bounded case mechanism may be reviewed as a
reference modeling sequence. It is not a case lifecycle record, manifest,
runtime resource, prompt input, retrieval document, SDK/IR fragment, or
hosted payload.

## Required evidence

- identity and scope: `admission_id`, `status`, decision, family/grammar, and
  declared applicability/prohibitions;
- source binding: repository-relative source paths plus SHA-256 digests for
  the decision, preregistration, production review, observable, and repair
  policy;
- oracle and development evidence: input hashes, split roles, expected
  selector cardinality, terminal sequence disposition, replay/gate evidence,
  and editability mutations;
- held-out isolation: a reviewed, hash-pinned evidence link only. An admission
  record must not contain a held-out fixture, STEP path/hash, candidate
  sequence, parameters, or replay result newly obtained by its audit;
- negative controls, stable rejection taxonomy, alternatives,
  counterexamples, operation/parameter dependencies, and repair signature;
- an explicit non-projection disposition.

## Audit rules

`tools/audit_admission_record.py` validates the v1 selector pilot
deterministically. It checks source and development input hashes, declared
split roles, terminal sequence and fail-closed policy, control taxonomy,
required audit evidence, and the absence of prohibited held-out/raw/runtime
references. It does not replay or inspect a held-out candidate.

The auditor reports the record's SHA-256 so a review can pin the exact record
revision. Any source or record change requires a new audit and independent
review; a rejected candidate remains evidence and cannot be silently swapped.

## Authority boundary

An independently reviewed record may support a later, user-selected admission
or projection decision. It does not itself authorize a case promotion,
manifest change, reference pack, experience card, retrieval, provider request,
training use, or claim of unique native CAD history.
