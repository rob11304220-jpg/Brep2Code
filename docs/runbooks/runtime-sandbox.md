# Runtime Sandbox Verification

This runbook is for the development Agent validating the runtime execution plane. It is not material supplied to the runtime LLM.

## Prerequisites

- Windows host with WSL distro `Ubuntu-24.04` and `bwrap`.
- Dedicated Linux runtime at `/home/liaol/.brep2code-runtime` with `cadquery-ocp`.
- Do not select `unsafe-local` when testing the contract.

## CAD smoke

```powershell
uv run python -m brep2code.cli run --record wsl-sandbox-box --input case-library\self-authored\box\input.step --data-root data --executor wsl-bwrap
```

The result must report `sandbox_backend: "wsl-bwrap"`, `sandboxed: true`, and pass the usual output gates.

## Input mount probe

```powershell
uv run python -m brep2code.cli run --record wsl-input-probe --script tests\fixtures\sandbox\input_mount_probe.py --input case-library\self-authored\box\input.step --data-root data --executor wsl-bwrap
```

The command intentionally fails its output-model gate. Its stdout must report `input_readable=True` and a non-zero input size; the script receives the selected model only as `/input/model.step`.

## Isolation probe

```powershell
$env:BREP2CODE_TEST_SECRET = "not-a-secret"
uv run python -m brep2code.cli run --record wsl-isolation-probe --script tests\fixtures\sandbox\isolation_probe.py --data-root data --executor wsl-bwrap
Remove-Item Env:BREP2CODE_TEST_SECRET
```

The Harness command intentionally fails its output-model gate because the probe does not generate STEP. Inspect the revision `traces/stdout.txt`; it must contain all three true values: `repository_hidden`, `ambient_secret_hidden`, and `network_blocked`.

## Timeout probe

```powershell
uv run python -m brep2code.cli run --record wsl-timeout-probe --script tests\fixtures\sandbox\timeout_probe.py --data-root data --timeout 1 --executor wsl-bwrap
```

The command must return a normal Harness JSON result with `exit_code: 124` and `timed_out: true`; it must not raise an unhandled executor exception.

## Reconstruction-provenance verification

```powershell
uv run python -m brep2code.cli run --record wsl-provenance-round-trip --script tests\fixtures\sandbox\provenance_ocp_roundtrip.py --input case-library\self-authored\box\input.step --data-root data --executor wsl-bwrap
uv run python -m brep2code.cli run --record wsl-provenance-child-read --script tests\fixtures\sandbox\provenance_child_reads_input.py --input case-library\self-authored\box\input.step --data-root data --executor wsl-bwrap
```

Both commands record a `coverage=active` attestation in the local provenance
trace and must classify the result as `round_trip`; the child-process case
also proves that the tracer follows descendants. Inspect the revision
`signal_bundle.json` rather than treating the normal geometry gates as a
reconstruction claim. A result can be `independent_reconstruction` only if
the normal run has an attested no-read trace and the Harness's second run of
the same staged script, without `/input/model.step`, succeeds with an
attested no-read trace. Missing trace coverage is always
`provenance_unknown`.

## Write-boundary and descendant probes

```powershell
uv run python -m brep2code.cli run --record wsl-write-probe --script tests\fixtures\sandbox\write_boundary_probe.py --data-root data --executor wsl-bwrap
uv run python -m brep2code.cli run --record wsl-descendant-probe --script tests\fixtures\sandbox\descendant_probe.py --data-root data --executor wsl-bwrap
```

Both commands intentionally fail the output-model gate. The write probe stdout must list both attempted paths as blocked. For the descendant probe, wait five seconds and verify that `output/descendant.txt` was not created; `output/parent.txt` may exist.

## Explicit resource and violation probes

```powershell
uv run python -m brep2code.cli run --record wsl-resource-probe --script tests\fixtures\sandbox\resource_mount_probe.py --runtime-resources tests\fixtures\sandbox\resources --data-root data --executor wsl-bwrap
uv run python -m brep2code.cli run --record wsl-violation-probe --script tests\fixtures\sandbox\unhandled_write_probe.py --data-root data --executor wsl-bwrap
```

Both commands intentionally fail the output-model gate. The resource probe stdout must report `resource_readable=True`. The violation probe must include `sandbox_event.code: "sandbox_policy_violation"` in its execution summary.

## Q01 observation / no-input build control

```powershell
uv run python -m brep2code.cli run --record m48-no-input-build --input case-library\self-authored\box\input.step --data-root C:\tmp\brep2code-m48-verify-cli --executor wsl-bwrap --build-without-input
```

The result must pass normal health gates, report
`observation_build_capability.input_mount_present: false`, and omit
`/input/model.step` from `execution.sandbox_mounts`. A tool-facing observation
context must be assembled only from `BRepToolBridge.observe()` envelopes; it
must not contain input paths or trace paths.

## M140 offline tool-turn control

Run the focused fake-provider tests when changing tool-turn orchestration:

```powershell
uv run python -m pytest tests\test_tool_turn_loop.py -q
```

The test sequence must demonstrate a probe result becoming a path-free `tool`
message for the next turn, rejection of an unselected/wrong card, one global
tool budget across calls, and terminal structured execution feedback. It is
offline evidence only; it does not construct a provider or authorize hosting.

## Interpretation

A passing smoke alone is insufficient. If any isolation value is false, the
provenance trace lacks coverage, or the selected backend is not `wsl-bwrap`,
do not make a reconstruction claim or enable hosted-provider execution.

## Validation cadence

Use the smallest relevant offline check during implementation: tool/context
changes run the focused tool-bridge tests; Harness or executor changes add the
focused Harness tests. Run the full focused corpus suite only when a change
touches Harness orchestration, executor behavior, signal/report schema, corpus
projection, or a CLI execution path, and always before workpack closure or
independent review. The corpus suite intentionally creates local
record/revisions, runs STEP probes, and exercises report/repair compatibility,
so it normally takes one to two minutes. Run Ruff, governance audit, and
`git diff --check` at every stage boundary.
