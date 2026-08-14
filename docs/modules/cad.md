# CAD Module

## Responsibility

`brep2code/cad/` owns execution adapters for `build_sequence.py`.

`ScriptExecutor` is the explicit `unsafe-local` subprocess runner. It:

- executes `build_sequence.py` from the revision workspace
- sets `BREP2CODE_WORKSPACE`
- captures exit code, stdout, stderr, timeout state, and duration

`WslBubblewrapExecutor` is the opt-in M5 backend for the supported Windows host. It stages `build_sequence.py` into the WSL Linux filesystem, runs it through bubblewrap with a cleared environment and network namespace, exposes the script read-only, and exposes only `output/` and `intermediates/` as writable paths. Select it with `brep2code run --executor wsl-bwrap`.

When the Harness requests provenance tracing, this executor builds the local
`provenance_trace.c` preload library in the private stage. Its startup marker
attests coverage and its `open`/`openat`-class hooks record attempted
`/input/` accesses from Python, native OCP code, and descendants. The trace
contains only local access metadata, never STEP contents. `unsafe-local` has
no such attestation and therefore cannot support an independent-reconstruction
classification.

## Boundary

The CAD module is not a project-level modeling SDK. It does not expose operations such as sketch, extrude, fillet, boolean, or a fixed IR. CAD backend calls live inside `build_sequence.py` or future bounded runtime helpers, not in Harness core.

## Public Entry

- `brep2code.cad.ScriptExecutor`
- `brep2code.cad.WslBubblewrapExecutor`
- `brep2code.cad.ExecutionResult`

## Acceptance

The executor must preserve logs for both successful and failed scripts so later repair loops can inspect traces. M2 expects scripts to write a valid STEP artifact at `output/model.step`. M46 additionally records an optional provenance trace path, observed input accesses, and coverage state in `ExecutionResult` and `execution.json`.
