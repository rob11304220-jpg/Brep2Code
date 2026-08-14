# M8-001 ABC External STEP Admission Review

## Completed evidence

The selected source is ABC Dataset `v00`, using the official STEP index and one local archive (`abc_0000_step_v00.7z`). ABC identifies the CAD-model copyright as belonging to original creators; accordingly raw assets, archive contents and reports remain only under ignored `data/`. The tracked selection record contains only source IDs, paths, SHA-256 values and non-sensitive probe baselines.

The deterministic scan examined the first 24 STEP members in archive order. Eleven multi-solid members were rejected. The first twelve readable single-solid members form an 8-case development split and a 4-case held-out split. No unit, coordinate or format conversion was applied; input units remain `unknown` as reported by the existing probe.

All twelve selected local files matched their recorded SHA-256 values and loaded through the explicit manifest. The completed report at ignored `data/corpus-runs/abc-v00-m8-001-baseline.json` executed every case through `wsl-bwrap`: all 12 scripts exited 0, two fixed-box controls passed and ten cases failed only geometry gates. These failures are expected controls from the deterministic box scaffold, not admission failures.

## Decision

The evidence confirms that the current input probe, manifest loader, sandbox executor and existing geometry gates can process this bounded external STEP slice. It does not identify a repeated attributable OCP/API, parameter, sequencing, probe or gate defect. Do not introduce a helper, IR, SDK, CAD workplace, new probe or new gate.

Future hosted evaluation of these samples remains a separate, explicitly authorized workpack. It must retain the local-only asset boundary and must not treat this 12-case slice as a model benchmark.
