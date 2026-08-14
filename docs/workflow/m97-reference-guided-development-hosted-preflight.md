# M97 Reference-Guided Development Hosted Preflight

- **Date**: 2026-08-10
- **Workpack**: `WP-M97-001-reference-guided-parameter-variation-development-hosted-calibration`
- **Mode**: read-only local preflight complete; hosted execution is not authorized.

## Fixed proposed scope

- **Destination/model**: `https://api.deepseek.com`, DeepSeek `deepseek-v4-pro`.
- **Rows**: only the three preregistered M95 development rows:
  `param_reference_guided_through_hole_development_low`,
  `param_reference_guided_through_hole_development_nominal`, and
  `param_reference_guided_through_hole_development_high`. Held-out rows are
  excluded from execution and review.
- **Conditions and egress**: for each row, the card condition sends a bounded,
  path-free observation transcript (387, 388, or 388 UTF-8 bytes locally) for
  a fixed `single boolean-cut tool` card request, then the same transcript plus
  the compact derived card for script generation. The baseline sends only the
  bounded, path-free observation transcript for script generation. No raw
  STEP, local path, reference script, source hash, provider payload,
  credential, request header, or previous report is sent.
- **Policy/gates**: frozen M96 policy
  `reference-guided-through-hole-variation-v1-m96`; its immutable historical
  index fixture is
  `docs/corpus/sequence-paired/fixtures/m96-m97-guidance-index-v1.json`,
  with index SHA-256
  `dfa731d597581b3b4d306782c1078c7de5b79672462229baaf5d7248fa230517`;
  card SHA-256
  `55341683e3e7df3e058a845193e34fba20b0650c0db28a31489ad5d343b60d30`.
  The unchanged OCP API, provenance, output, bbox, volume, and topology gates
  run under no-input `wsl-bwrap`.
- **Bound**: exactly nine sequential requests (two card + one baseline for
  each row), zero repair, zero retry, and a 120-second deadline per request.
- **Fresh paths**: proposed report
  `data/corpus-runs/m97-reference-guided-through-hole-development-calibration.json`
  and monitor state
  `data/monitor-runs/m97-reference-guided-through-hole-development-calibration.monitor.json`.

## Read-only evidence

- The M96 policy contains exactly the frozen three development rows and a
  separate three-row held-out order; the M97 CLI rejects any other request
  budget and uses no held-out path.
- Input SHA-256 values are `c6803644c67b03de2968440198717a0ec9eee4b3161f3ef40f2c8238c8a362ec`
  (low), `3c6378d3c90579a8ea723cc568c79ba63a5916ca7c987a06f54a11cfd8efa77b`
  (nominal), and `8eed1dcc0673e38f5a570196d2729c62cb66005f6ac67658ce4a70f673f6ae3f`
  (high).
- The M96 transcript audit passed for all three rows; the M97 offline fixture
  passed all three reference scripts with no input mount under `wsl-bwrap`.
- The local configuration selects the stated DeepSeek endpoint/model and has
  a key present; no credential or environment snapshot was displayed.
  `wsl.exe` is available.
- Both proposed report paths are absent. The new M97 lifecycle creates a
  content-free `running` checkpoint at `0/9`; each request is marked issued
  immediately before provider work, and execute terminalizes `completed` or
  `interrupted`. M70 remains report-read-only and cannot retry or resume.

## Authorization

Liaol explicitly approved every fixed-scope item above on 2026-08-10:
destination/model, the limited derived egress, the three named development
rows and paired conditions, nine-request cap, 120-second per-request deadline,
zero retry/repair, and no-input `wsl-bwrap` execution. This approval covers
one new `prepare` → M70 monitor → `execute` lifecycle only; it does not
authorize report reuse, a further request after terminal failure, held-out
evaluation, or policy/card/prompt changes.

The provider deadline and nine sequential requests can outlast an interactive
command window, so the authorized run must use `prepare`, attach the durable
M70 monitor, then `execute`. A timeout or terminal failure consumes issued
capacity only and does not authorize another request.
