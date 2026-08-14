# WP-M30-001: Blind/Through Observability Design and Probe-Boundary Audit

- Status: done
- Milestone: M30
- Owner: Codex

## Goal

Freeze the smallest Q01 design that can test blind versus through cylindrical
cut extent from measured B-Rep facts, without using deterministic reference
sequence labels as recognition inputs.

## Scope

- Reuse only the existing `prismatic-hole-v1` through development and blind
  held-out records as fixed oracle labels for post-measurement scoring.
- Define required terminal-face, adjacency, containment, axis and tolerance
  facts, plus an explicit unsupported result.
- Audit the public M1 probe contract against those required facts.
- Propose a separately selectable offline-only reporter/audit workpack.

## Decision-package impact

- `decision_id`: `q01-blind-through-observability-v1`.
- Q01/Q02 effect: a cut-extent hypothesis is allowed only after recorded
  terminal or connectivity facts discriminate it; otherwise it stops as
  `unsupported`.
- Q03/Q04 effect: no repair is proposed for missing observability.
- Evidence role: fixed oracle labels, a future discriminating audit, and
  negative controls for counterbore/unknown connectivity/label leakage.
- Knowledge disposition: design only; no Q01 observable unit is reviewed.

## Probe-boundary result

`probe_entity` currently supplies surface type, bbox, parameter range and
sampling; `probe_topology` supplies entity lists and counts. Neither supplies
face-edge-face adjacency, terminal-face role, loop containment nor
through-connectivity. Therefore existing public probe responses cannot yet
prove this distinction, and M30-001 makes no recognition claim.

## Compatibility constraints

Offline-only. No candidate assets, case registration, executable manifest,
provider use, training input, runtime resource, CLI/probe contract, helper,
IR, SDK, gate or parser change.

## Acceptance

- The preregistration identifies measured facts, labels excluded from inputs,
  negative controls, split boundary and stop rule.
- The stated M1 probe boundary is traceable to the current probe contract and
  implementation.
- JSON parsing and `git diff --check` pass.

## Completion

- Added the design-only observable contract at
  `docs/corpus/knowledge/observables/blind-through-cylindrical-extent-v1.design.json`.
- Recorded that current public probes cannot supply the required relation facts.
- M30-002 remains a separately selectable offline reporter/audit proposal; it
  cannot use reference-script labels during measurement or change runtime
  behavior.

## Out of scope

Candidate production, feature classification, generic cylinder recognition,
history recovery, public probe expansion, runtime adoption, hosted evaluation,
or any production repair.
