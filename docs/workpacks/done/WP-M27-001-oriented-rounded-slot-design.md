# WP-M27-001: Oriented Rounded-Slot Design and Preregistration

- Status: done
- Milestone: M27
- Owner: Codex

## Goal

Freeze one bounded self-authored rounded-slot family that makes its XY local
axis observable before any candidate production.

## Scope

- Preregister exactly six family-isolated rows and a four-operation oracle.
- Freeze +X/+Y frames, strict containment, through-cut semantics, directional
  mutations, negative controls, rejection taxonomy, and hash-stability checks.
- Define a candidate-only successor production boundary.

## Compatibility constraints

Offline-only. No assets, producer output, registry, manifest, provider,
training, runtime, parser/helper/SDK, IR, splines, arbitrary angles, or
generic sketch-frame inference.

## Acceptance

- The M24 intake audit passes the frozen record.
- The record declares exact local-axis and orientation controls, with wrong
  axis/frame, nonthrough-cut, profile-degeneration, and split-leak rejection.
- `git diff --check` passes.

## Evidence reuse / guidance-card disposition

No runtime experience card: this is planning evidence only.

## Next

Only a separately selected production workpack may create the six frozen
candidates and family-specific geometry audit.

## Result

Completed offline on 2026-08-05. ADR-0032 and the frozen six-row record passed
the M24 intake audit; no row or boundary changed during design.
