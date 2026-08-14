# M127 Shared Hosted-Stability Re-entry Preflight

- **Workpack**: `WP-M127-001-shared-hosted-stability-reentry`
- **Status**: passed offline owner-side preflight; awaiting independent G3 review and any later itemized hosted authorization
- **Provider construction / request**: none

## Proposed hosted boundary

| Item | Frozen value |
|---|---|
| Destination / model | `https://api.deepseek.com` / `deepseek-v4-pro` |
| Case / split | One self-authored P1 development row: `three_hole_plate`; held-out forbidden |
| Egress | Path-free bounded observation transcript and fixed instructions; second request additionally includes only the frozen `vertical-cylinder-construction` card |
| Excluded egress | Raw STEP, paths, filenames, reference scripts, reports, responses, headers, traces and credentials |
| Lifecycle | Two sequential requests, one fresh atomic report with 2/2 accounting, zero repair and retry |
| Cap / deadline | 4096 output tokens and 300 seconds per request |
| Execution | `wsl-bwrap` without an input mount |
| Fresh paths | `data/corpus-runs/m127-three-hole-plate-stability-reentry.json` and `data/monitor-runs/m127-three-hole-plate-stability-reentry.monitor.json` |

This boundary intentionally preserves M118's bounded stability shape while
moving to a fresh M127 policy namespace, fresh report/monitor paths, and fresh
authorization scope. It is a shared hosted-stability re-entry candidate only:
it does not activate `TRG-005`, enter M115 calibration, or authorize a family-
scoped hosted campaign.

## Offline checks

- Added the fresh M127 CLI/checkpoint identity
  `reference-assisted-three-hole-plate-stability-reentry-smoke` and frozen
  policy
  [`m127-three-hole-plate-stability-reentry-policy-v1.json`](../corpus/registry/m127-three-hole-plate-stability-reentry-policy-v1.json).
  The command preserves the fixed `three_hole_plate` case, `repeated boolean-cut tool`
  role, two-request accounting, zero repair, and required `4096` token cap
  while separating M127 accounting from M118.
- The selected input SHA-256 remains
  `34ef08fd81be048d1ba09066f21f162931d91a2001701f7ad737fb3722ae4418`.
  The fixed guidance index SHA-256 remains
  `dfa731d597581b3b4d306782c1078c7de5b79672462229baaf5d7248fa230517`;
  the selected card SHA-256 remains
  `55341683e3e7df3e058a845193e34fba20b0650c0db28a31489ad5d343b60d30`.
- Focused CLI validation passed in the repo virtualenv: the observed-build test
  session includes the new M127 command path, and Ruff passed on the touched
  CLI, test, and hosted-runbook documentation files.
- Fresh checkpoint validation passed locally with a fake-provider
  `prepare -> execute` sequence against a temporary report path:
  `policy = m127-three-hole-plate-stability-reentry-v1`,
  `max_output_tokens = 4096`, `requests_used = 2`, and
  `requests_remaining = 0` at terminal `completed`. This validates the fresh
  M127 accounting boundary without constructing a hosted provider or sending
  egress.
- A local no-input `wsl-bwrap` replay using the checked-in
  `three_hole_plate/reference_build_sequence.py` passed with
  `sandbox_backend = "wsl-bwrap"`, `sandboxed = true`,
  `provenance_coverage = true`, `input_mount_present = false`, empty input
  accesses, and pass results for script, output, bbox, volume, and topology
  gates. This confirms the secure executor boundary required by the M127
  hosted profile.
- The planned M127 report and monitor destinations are still absent in the
  workspace, so no running/interrupted/completed M127 checkpoint is currently
  in scope.

## Interpretation table

| Terminal outcome | Interpretation |
|---|---|
| `pass` | Only this frozen M127 shared stability path completed successfully. It does not satisfy another track's gate or authorize any family-scoped campaign. |
| `provider timeout` / lifecycle failure | Only this fixed request path failed to complete within the frozen lifecycle boundary. It does not identify provider-wide, model-wide, or geometry-complexity cause. |
| `script/API failure` | Only the generated result failed the frozen output or supported API contract. Downstream gates remain `not evaluated` if they were not reached. |
| `sandbox/provenance failure` | Only the secure execution or provenance boundary failed on this path. |
| `geometry/semantic/editability gate failure` | Only this frozen policy reached an applicable downstream gate and did not satisfy it. |
| `interrupted` | Partial evidence only; not a reviewed terminal campaign result and not reusable capacity. |

## Authorization gate

This preflight grants no provider authority. After Liaol independently reviews
the frozen M127 policy, code changes, and retained offline evidence, any later
authorization request must explicitly approve every row of the proposed
boundary above, including destination/model, derived outbound content, the
fixed `three_hole_plate` development row, the two-request budget, zero
retry/repair, 4096-token cap, 300-second deadline, no-input `wsl-bwrap`, and
the two fresh M127 report/monitor paths.

## Independent G3 review checklist

Liaol's independent review should confirm at minimum:

- the M127 command/policy namespace is fresh and does not reuse M118
  accounting, report paths, monitor paths, or prior authorization;
- the fixed development scope, role/card hashes, request bound, token cap, and
  deadline match the frozen M127 policy;
- the fake-provider `prepare -> execute` evidence shows the fresh M127 policy
  reaches terminal `2/2` accounting without a hosted request;
- the separate no-input `wsl-bwrap` replay passes sandbox, provenance, and the
  existing geometry gates; and
- the allowed conclusion and explicit non-inference remain bounded to shared
  hosted-stability re-entry only.

## Itemized authorization payload draft

If the independent G3 review passes, the later authorization request should ask
for approval only for the following exact boundary:

- destination `https://api.deepseek.com`;
- model `deepseek-v4-pro`;
- outbound content limited to one path-free observation transcript plus fixed
  instructions, then that same transcript plus only the frozen
  `vertical-cylinder-construction` card;
- one fixed development row: `three_hole_plate` from the checked-in P1
  manifest;
- exactly two sequential requests;
- zero retry and zero repair;
- `4096` maximum output tokens per request;
- `300` seconds provider deadline per request;
- `wsl-bwrap` without an input mount; and
- fresh paths
  `data/corpus-runs/m127-three-hole-plate-stability-reentry.json` and
  `data/monitor-runs/m127-three-hole-plate-stability-reentry.monitor.json`.
