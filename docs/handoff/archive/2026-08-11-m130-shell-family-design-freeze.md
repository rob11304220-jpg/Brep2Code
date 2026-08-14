# Handoff: Shell Family Design Freeze

- **Date**: 2026-08-11
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M130-001-shell-family-design-freeze`

## Goal

Freeze the offline `shell-v1` family design under the M24 intake contract.

## Next

- Create `shell-v1-preregistration.json` with one top-opening uniform-thickness grammar, a 3/3 family-isolated split, invariants and controls.
- Write the corresponding design ADR and run the generic intake audit.
- Completed: `shell-v1-preregistration.json` and ADR-0066 are frozen; the
  intake audit, Ruff, governance audit and diff check passed. No candidate
  assets or hosted scope were created.
- Next: obtain Liaol's independent G2 review before closure.

## Boundaries

No candidate production, manifest/provider/runtime/card change, hosted work, or rib scope.
