# WP-M25-001: Face-Selected-Dependent-Cut Design and Preregistration

- Status: done
- Milestone: M25
- Owner: Codex

## Goal

Freeze a bounded self-authored family that makes a unique boss-top face
selection observable before a dependent blind cut.

## Scope

- Preregister exactly six family-isolated rows and a seven-operation oracle.
- Freeze observable selector predicates, semantic invariants, directional
  mutations, negative controls, rejection taxonomy, and hash-stability checks.
- Create M25-002 as the sole possible controlled-production route.

## Compatibility constraints

Offline-only. No assets, producer, registry, manifest, provider, training,
runtime, parser/helper/SDK, IR, or generic face-naming behavior changes.

## Acceptance

- The M24 intake audit passes the frozen record.
- The selector is bounded to one unique planar +Z maximum-Z boss face and
  rejects wrong/vertical/ambiguous selection claims.
- `git diff --check` passes.

## Evidence reuse / guidance-card disposition

No runtime experience card: this is a planning record, not runtime evidence.

## Result

Completed offline on 2026-08-05. ADR-0028 and the preregistration freeze the
six rows and selector contract before candidate production. M25-002 is only a
separately selectable proposal; no asset or runtime path changed.

## Out of scope

Candidate production, generic face/edge references, selector implementation,
promotion, external data, hosted evaluation, and runtime changes.
