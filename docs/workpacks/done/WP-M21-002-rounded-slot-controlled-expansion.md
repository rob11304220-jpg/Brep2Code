# WP-M21-002: Rounded-Slot Controlled Production and Validation

- Status: done
- Milestone: M21
- Owner: Codex

## Goal

Test the preregistered `rounded-slot-v1` grammar on exactly six self-authored
sequence-paired rows without changing its frozen design or promoting it.

## Result

- Produced only the three preregistered `offset_rounded_slot` held-out assets;
  all remain `experimental` and outside the registry and manifests.
- Repeated generation produced hash-stable normalized STEP files.
- All six rows passed existing geometry replay, exact sequence/dependency
  agreement, rounded-slot anti-degeneration checks, and three mutations.
- Focused tests reject rectangular-profile degeneration and split leakage.
- Full local validation: 88 pytest passed; Ruff and `git diff --check` passed.

## Evidence reuse / guidance-card disposition

No reusable experience card.  The evidence remains development-side and
deterministic-oracle scoped.

## Out of scope

Governance promotion, active-library registration, manifests, provider use,
training, runtime integration, native-history claims, generic B-Rep inference,
or a general IR.
