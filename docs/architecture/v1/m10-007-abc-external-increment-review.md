# M10-007 ABC Second Deterministic External Corpus Increment Review

## Completed evidence

This local-only increment continued ABC `v00` archive-member order after the M10-003 cutoff. It scanned `00000027` through `00000031`, accepted readable single-solid members `00000027`, `00000030`, and `00000031`, and rejected `00000028` (three solids) and `00000029` (two solids). The accepted files preserve a 2-case development and 1-case held-out split.

All three selected local files matched the tracked SHA-256 values and supplied existing-probe bbox, topology, and volume baselines. The ignored development and held-out `wsl-bwrap` reports both reached `run_status: completed`: all three input summaries, script exits, and output summaries passed. The fixed box scaffold failed bbox, volume, and topology comparisons for each case, as expected control evidence.

## Decision

The increment remains an explicit local corpus input and makes no change to default commands, scripts, probes, gates, or external-data redistribution. It does not authorize a hosted request; any first-pass evaluation requires a new workpack, a fresh preflight, and separate explicit authorization for each split.
