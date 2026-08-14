# Handoff: Fusion 360 Line3D loop-ordering offline repair

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Evaluate a bounded endpoint-ordering treatment for the fixed M17 held-out
Line3D loop-order mismatch.

## Done

- M17 identified direct local evidence: an accepted Line3D profile list was not
  continuous and produced a degenerate output.
- M17 stopped without replacement sample, syntax expansion, corpus run or
  provider request.
- Endpoint ordering did not repair the held-out mismatch; strict replay was
  restored after M14/M17 controls retained their outcomes.

## Next

- Do not advance M18. Any coordinate-frame/extrude-direction diagnostic needs
  a separate workpack and must retain the held-out failure baseline.

## Decisions

- Ambiguous/non-closing loops must reject; no generic sketch healing.
- The endpoint-ordering treatment is rejected and not retained in the tool.

## Blockers

- None.
