# WP-TRG-034: Capability-Contract Code Alignment

- Status: deferred
- Owner: unassigned
- Reviewer: independent reviewer required
- Risk tier: G2

## Entry condition

`WP-TRG-033` is complete and independently reviewed or explicitly accepted,
and the user selects one bounded hypothesis and its Q01--Q04 contract for this
package. The activation package must freeze the M146 crosswalk ID/SHA-256, M150
case-evidence mapping ID/SHA-256 and selected relationship IDs. The chosen
hypothesis must already have one complete, evidence-bounded Q01 observable,
Q02 action constraint, Q03 gate, and Q04 diagnostic/stop chain. If more than
one capability is needed, or any chain link is absent, stop and select a new
bounded offline evidence/contract package before activation.

## Goal

Align one selected bounded modeling hypothesis with the relevant Q01 observable,
Q02 action constraint, Q03 gate, Q04 diagnostic/stop contract, and focused
tests.

## Scope

- State one M146 `hypothesis_id`, its linked decision package (or why none
  applies), evidence roles, counterexample, stop rule, known
  non-generalization, verified M146/M150 provenance hashes, and relationship
  IDs used as evidence context.
- Make the smallest code, contract, documentation, and regression-test changes
  required to represent or verify that bounded capability.
- Add a versioned, source-linked implementation-contract mapping from that one
  hypothesis to its Q01 observable, Q02 action constraint, Q03 gate, Q04
  diagnostic/stop contract, and validation evidence. Do not overload the M146
  crosswalk's evidence-navigation schema with executable authority.
- Declare the mapping's implementation status as `implemented`,
  `contract_only`, or `unsupported`. `contract_only` and `unsupported` are
  valid outcomes, but cannot be represented as implemented capability or used
  to bypass a missing-evidence stop condition.
- Update derived navigation to link the implementation-contract mapping and
  validation evidence back to the hypothesis.

## Compatibility constraints

The change must be fail-closed outside the selected hypothesis boundary. It
cannot infer generic feature recognition, history recovery, helper, IR, SDK,
runtime-card, manifest, provider, or training authority from a case or unit.
The M146 crosswalk is an input snapshot, not a code-generation specification.
M150 relationships are evidence provenance, not case/manifest authority.

## Acceptance

```powershell
uv run python -m pytest tests -q
uv run python -m ruff check .
python tools\audit_development_evidence_crosswalk.py
python tools\audit_case_evidence_relationships.py
uv run python tools\check_governance.py
git diff --check
```

## Out of scope

Unbounded multi-capability refactors, case production, split/manifest changes,
runtime projection, provider use, and hosted execution.
