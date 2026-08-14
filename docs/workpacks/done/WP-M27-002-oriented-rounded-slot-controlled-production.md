# WP-M27-002: Oriented Rounded-Slot Controlled Production

- Status: done
- Milestone: M27
- Owner: Codex

## Goal

Produce and audit exactly the six preregistered M27 oriented rounded-slot
candidates under the frozen +X/+Y contract.

## Scope

- Add one deterministic offline producer and family-specific audit.
- Build each row twice in clean directories and retain hash-stability evidence.
- Check geometry replay, exact sequence/frame agreement, four mutations,
  through-cut semantics, one-solid invariant, and split isolation.

## Compatibility constraints

Offline-only. Candidates remain experimental. No registry, manifest, provider,
training, runtime, parser/helper/SDK, IR, spline, arbitrary-angle, or generic
frame-inference change.

## Acceptance

- Exactly six frozen rows are produced and remain experimental.
- All six pass hash, geometry, sequence, orientation, editability, semantic,
  and split audits.
- Focused tests, Ruff, and `git diff --check` pass.

## Next

A later independent evidence-review workpack may evaluate the completed
candidates; this workpack cannot promote them.

## Result

Completed offline on 2026-08-05. All six frozen candidates were hash-stable
across two clean directories and passed geometry replay, exact frame sequence,
four directional mutations, through-cut/single-solid semantics, and split
isolation. They remain experimental.
