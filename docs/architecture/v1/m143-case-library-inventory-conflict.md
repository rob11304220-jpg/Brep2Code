# M143 Case-Library Inventory Conflict

## Result

M143's metadata-only inventory cannot validate `admission-profile-v1` while
the active registry disagrees with authoritative per-case metadata.

## Reproducible evidence

`tools/audit_admission_profile.py` reads only the active self-authored registry
and each listed `case.json`; it does not open STEP fixtures or reference
scripts. The inventory reports 87 active registry rows and these conflicts:

| Case | Registry status | Authoritative `case.json` status |
|---|---|---|
| `param_offset_rounded_slot_low` | `active` | `experimental` |
| `param_offset_rounded_slot_nominal` | `active` | `experimental` |
| `param_offset_rounded_slot_high` | `active` | `experimental` |

ADR-0014 states that each `case.json` owns self-authored identity and lifecycle
metadata. Yet ADR-0023 and the registry describe these rows as promoted active
assets. M143 must not resolve this drift by silently preferring the registry,
altering the three cases, or inspecting their held-out fixtures.

## Boundary and re-entry

The profile schema and recommendation cap are present, but the profile audit
remains intentionally blocked until a separately authorized, bounded metadata
reconciliation resolves the lifecycle authority conflict and records its
validation. This report creates no case admission, manifest, runtime, provider,
or hosted authority.
