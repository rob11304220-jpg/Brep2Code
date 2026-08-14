# M67 Hosted Telemetry Preflight — Awaiting Authorization

- **Date**: 2026-08-09
- **Mode**: read-only; no provider request issued

## Fixed proposed collection

- Destination/model: `https://api.deepseek.com`, DeepSeek `deepseek-v4-pro`.
- Egress: only each case's existing M48 path-free bounded observation
  transcript; no raw STEP, path, filename, reference script, docs, trace,
  credential or environment value.
- Cases: `param_additive_boss_low` (8 faces/30 edges),
  `param_rounded_slot_low` (11/54), and `param_fillet_low` (7/30), all
  development/P2 and each selected through `--case-id`.
- Bound: each case is an independent first pass, exactly one request, no repair,
  `wsl-bwrap`, 300-second provider deadline; total maximum 3 requests.
- Reports: `data/corpus-runs/m67-param-additive-boss-low.json`,
  `data/corpus-runs/m67-param-rounded-slot-low.json`, and
  `data/corpus-runs/m67-param-fillet-low.json`.

## Checks

- Manifest SHA-256:
  `DC4C6E8F3302367A3B1082FAD602FE36FF2A59901E59079695DA75724892A593`.
- Non-secret configuration parses as `deepseek-v4-pro` at
  `https://api.deepseek.com`; bubblewrap is `0.9.0`.
- All three proposed report paths are absent and have no checkpoint.
- M65/M66 telemetry is covered by 21 focused offline tests. M67's selector
  retains manifest membership and request bounds.

## Authorization gate

This preflight does not authorize egress. A new authorization must approve the
destination/model, outbound transcript boundary, all three named development
cases, three total independent one-request/no-repair runs, 300-second deadline,
`wsl-bwrap`, and the three reports. M54/M63/M64 budgets, reports and
authorizations are not reusable.
