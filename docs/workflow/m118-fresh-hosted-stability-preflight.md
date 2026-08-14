# M118 Fresh Hosted-Stability Preflight

- **Workpack**: `WP-M118-001-fresh-hosted-stability-preflight`
- **Status**: passed offline; awaiting independent G3 review and itemized user authorization
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
| Fresh paths | `data/corpus-runs/m118-three-hole-plate-stability.json` and `data/monitor-runs/m118-three-hole-plate-stability.monitor.json` |

The maximum provider wait is 600 seconds, excluding local Harness work. An
authorized execution must use the durable `prepare` → monitor → `execute`
lifecycle rather than an interactive command window.

## Offline checks

- The selected input SHA-256 is
  `34ef08fd81be048d1ba09066f21f162931d91a2001701f7ad737fb3722ae4418`.
  The P1 manifest contains exactly one `three_hole_plate` row.
- Guidance index SHA-256 is
  `dfa731d597581b3b4d306782c1078c7de5b79672462229baaf5d7248fa230517`;
  the selected card SHA-256 is
  `55341683e3e7df3e058a845193e34fba20b0650c0db28a31489ad5d343b60d30`.
- A non-secret local configuration check found the configuration file, exactly
  one nonempty key entry, the selected model and the selected endpoint. It did
  not display a credential, environment snapshot or provider object.
- Both proposed report and monitor paths are absent. No existing running or
  interrupted checkpoint is in scope.
- Fake-provider checkpoint validation passed with exactly two requests, the
  M118 policy identity and 4096-token cap. The CLI rejects a one-request bound
  and an alternate token cap before any hosted provider path.
- The no-input `wsl-bwrap` reference replay passed static API validation,
  sandbox/provenance coverage, no-input-access control, output readability,
  bbox, volume and topology gates. WSL emitted a local `.wslconfig` warning,
  but the executor returned `sandboxed: true`, exit code zero and all stated
  gates passed; it is retained as an environment warning, not a sandbox
  failure.

## Authorization gate

This preflight grants no provider authority. After Liaol independently reviews
the frozen policy, code and checks, the user must explicitly approve every row
of the proposed boundary above, including destination and egress, model/case,
two-request budget, zero retry/repair, 4096-token cap, 300-second deadline,
no-input executor and both fresh paths.
