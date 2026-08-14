# WP-M143-001: Case-Library Stratification and Admission Profiles

- Status: done
- Milestone: M143
- Trigger consumed: `WP-TRG-029`
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

M142's immutable selector-ambiguity admission record was independently
reviewed. The user selected this bounded, development-side investigation before
any runtime projection work.

## Goal

Create `admission-profile-v1`: an auditable crosswalk over existing case
metadata and reviewed evidence that states mechanism-specific minimum evidence
and fail-closed conditions. A profile does not admit a case or create runtime
knowledge.

## Scope

- Build a deterministic inventory from tracked case metadata, registry,
  coverage matrix, decision packages, preregistrations, and reviewed audits.
- Classify assets by modeling mechanism, entity-reference stability,
  sequence-dependency structure, parameter/split role, evidence maturity, and
  admission risk. Difficulty must be derived from these observable fields.
- Define `admit`, `needs_evidence`, `fail_closed`, and `counterexample_only`
  dispositions and their minimum evidence.
- Map the reviewed M142 record to the profile and recommend at most three next
  decision gaps. Recommendations cannot select, create, inspect, or execute a
  successor case.

## Compatibility constraints

Remain offline and credential-free. Do not add or modify a case, fixture,
manifest, reference script, Harness behavior, provider configuration, runtime
resource, card, pack, SDK, IR, retrieval index, or training asset. Held-out
material may be represented only by declared metadata and existing reviewed,
hash-pinned audit links; it must not be inspected, replayed, or executed.

## Decision-package impact

No Q01--Q04 decision package changes. This is a read-only crosswalk over
existing evidence; it creates no reusable runtime knowledge and changes no
existing gate, repair disposition, or split boundary.

## Acceptance

```powershell
uv run python -m pytest tests\test_admission_profile.py tests\test_m144_rounded_slot_metadata.py -q
uv run python tools\audit_admission_profile.py
uv run python -m ruff check tools\audit_admission_profile.py tests\test_admission_profile.py tests\test_m144_rounded_slot_metadata.py
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the source-linked inventory, profile schema and deterministic audit,
map M142, state bounded recommendations and prohibitions, run offline checks,
and obtain Liaol's independent G2 review.

## Implementation evidence

- `docs/corpus/knowledge/admissions/admission-profile-schema-v1.json` defines
  the six profile axes and four dispositions. The companion draft profile uses
  source hashes for registry, coverage matrix, and M142 record.
- `tools/audit_admission_profile.py` inventories only active registry rows and
  their `case.json` metadata. It reports 87 active rows, profile counts of 30
  baseline/unpaired, 51 family-scoped sequence, and 6 unique planar-selector
  records; it reports `fixture_access=not_performed` and held-out access as
  metadata/documentary only.
- M144 reconciled the only detected lifecycle drift. The profile now audits
  with zero inventory conflicts and recommends at most three bounded decision
  gaps without selecting any.
- ADR-0073 records the classification authority boundary.

## Closure

Liaol completed the independent G2 review and approved closure on 2026-08-12.
The reviewed profile remains metadata-only and evidence-only: it changes no
case lifecycle beyond M144's separately reviewed reconciliation, and creates
no manifest, runtime, provider, or hosted authority.

## Implementation evidence and current stop

- Added `admission-profile-v1` schema and draft profile under
  `docs/corpus/knowledge/admissions/`, plus metadata-only inventory/audit in
  `tools/audit_admission_profile.py` and focused tests.
- The inventory reads registry and `case.json` metadata only and reports
  `fixture_access=not_performed`; it found an authoritative lifecycle conflict
  for the three active-registry `param_offset_rounded_slot_*` rows whose
  `case.json` remains `experimental`.
- See `docs/architecture/v1/m143-case-library-inventory-conflict.md`. The
  profile cannot be accepted until a separately authorized reconciliation
  resolves this frozen metadata drift; M143 must not change those cases.

## Permitted stop conditions

Independent review; reproducible conflict in authoritative inventory or split
records; an out-of-scope need for new production, held-out access, manifest or
runtime change, hosted authority, or reproducible local validation blocker.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and active handoff.
On closure, archive it and leave `WP-TRG-028` deferred until user-selected.

## Blocked state

M144 reconciled the documented lifecycle metadata conflict and received
independent review. M143 resumes in `active/` under the same M143 identifier;
the profile audit remains metadata-only and does not create a new authority.

## Out of scope

Open-ended corpus expansion, generic difficulty ranking, case admission or
promotion, runtime projection, provider calls, training, hosted execution, and
all held-out candidate inspection or execution.
