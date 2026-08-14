# M10-003 ABC Deterministic External Corpus Increment Review

## Completed evidence

This local-only increment continues the already acquired ABC `v00` archive in archive-member order immediately after the M8 cutoff. It scanned members `00000023` through `00000026`, accepted the first three readable single-solid files (`00000023`, `00000024`, and `00000026`), and rejected `00000025` because the existing input probe reported three solids. The accepted files preserve a 2-case development and 1-case held-out split.

The tracked selection record contains source identities, paths, SHA-256 values, license boundary, normalization decision, and bounded-probe baselines only; raw assets and reports remain ignored under `data/`. The existing probe reports unknown units, upstream coordinates, and no conversion or transform for all accepted inputs. On 2026-08-02 all three selected local files matched their recorded SHA-256 values. The ignored development and held-out reports `abc-v00-m10-003-development-preflight.json` and `abc-v00-m10-003-held-out-preflight.json` both reached `run_status: completed` through `wsl-bwrap`; all three input summaries, script exits, and output summaries passed. The fixed box scaffold then failed only bbox, volume, and topology comparisons for all three cases, as expected control evidence.

## Decision

The increment remains an explicit local corpus input. It adds no reference or first-pass scripts, does not modify default manifests or commands, and does not authorize a hosted evaluation. Existing input probes, manifests, sandbox execution, and geometry gates remain unchanged; fixed-scaffold geometry-gate failures are control evidence rather than admission failure.
