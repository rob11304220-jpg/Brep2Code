# M10-010 ABC Third Deterministic External Increment Review

## Completed evidence

Under ADR-0011, the existing local `abc_0000_step_v00.7z` archive was completely extracted only into ignored `data/datasets/abc/v00/step/`.  Its ignored completion catalog records archive SHA-256 `52e6dd1b6fa38e3cd99af59b662370829129540030975919c3e256dce6ad1dbe`, 10,000 STEP members, and `13,703,699,417` listed and cached bytes.  This reconstructable cache does not enable a full corpus, default fixture discovery, tracked full manifest, provider input, or redistribution.

The deterministic archive-order admission then continued after M10-007 cutoff `00000031`.  It accepted readable single-solid `00000032` and `00000033` for development, rejected `00000034` because the existing input probe reported three solids, and accepted readable single-solid `00000035` for held-out.  The tracked selection record preserves each source identity, SHA-256, probe baseline, split, and local-research/no-redistribution boundary.

Both ignored `wsl-bwrap` controls reached `run_status: completed`.  Across the 2/1 split, all three scripts exited successfully and every input/output STEP summary was readable.  The fixed box scaffold failed bbox, volume, and topology comparisons in all three cases, which is expected control evidence rather than an admission failure.

## Decision

M10-010 changes no Harness behavior, default command, provider policy, CLI, report schema, manifest contract, probe, or gate.  It authorizes no hosted request.  The next active work is M10-011: verify the cumulative attribution ledger and select one evidence-gated successor route before any repair experiment or further sampling.
