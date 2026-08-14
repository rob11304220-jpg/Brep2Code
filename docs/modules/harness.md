# Harness / Agent Module

## Responsibility

`brep2code/agent/` coordinates one manual Harness revision and now owns the minimal M3 provider/tool boundary:

1. create or open a record
2. create a fresh revision workspace
3. write or copy `build_sequence.py`
4. execute the script
5. save stdout, stderr, execution summary, and `signal_bundle.json`
6. run output readability and basic geometry gates when STEP probes are available
7. define LLM provider request/response data structures and sanitized trace writers
8. expose B-Rep probe APIs through bounded internal tool calls and `tool_calls.jsonl`
9. run a bounded fake-provider repair loop across immutable revisions
10. classify terminal repair feedback fail-closed before any M141 source edit
11. classify execution provenance separately from geometry health: `round_trip`, `independent_reconstruction`, or fail-closed `provenance_unknown`
12. record an optional sanitized Q01 observation transcript and a build-input-mount capability attestation
13. run one offline fake-provider observation-to-build loop without mounting the original STEP
14. expose an opt-in revision-scoped guidance-card bridge with no-card default

## Boundary

M3 required loop has no hosted LLM SDK call and no CAD operation API. It provides a fake local provider, revision trace helpers, bounded B-Rep tool bridge, and fake-provider repair runner so the repair loop can be verified without network credentials. Harness core remains independent from a fixed modeling IR or project-level CAD SDK.

## Public Entry

- `brep2code.agent.ManualHarness`
- `brep2code.agent.HarnessRunResult`
- `brep2code.agent.ProviderRequest`
- `brep2code.agent.ProviderResponse`
- `brep2code.agent.ScriptUpdate`
- `brep2code.agent.FakeLLMProvider`
- `brep2code.agent.BRepToolBridge`
- `brep2code.agent.GuidanceCardBridge`
- `brep2code.agent.RepairLoopRunner`
- `brep2code.agent.repair_policy.ClassifiedRepairRunner` (M141 offline policy)

## Acceptance

Run:

```powershell
uv run python -m brep2code.cli run --record box-smoke --input case-library\self-authored\box\input.step
```

The command should return status `pass` with `output/model.step` present, readable, and compared against the input by bbox, volume, and topology counts.

For M3 provider/trace/tool checks:

```powershell
uv run python -m pytest tests\test_agent_m3_provider_trace.py
uv run python -m pytest tests\test_agent_m3_tool_bridge.py
uv run python -m pytest tests\test_agent_m3_repair_loop.py
```

The tests should pass without network access or LLM credentials and should write sanitized LLM/tool traces under revision `traces/` directories.

For M46 provenance checks, run:

```powershell
uv run python -m pytest tests\test_harness_m2.py tests\test_corpus_m4.py -q
```

The Harness records a versioned `provenance` object in `signal_bundle.json`.
Schema-v3 corpus reports project that object additively for first-pass cases;
the pre-existing geometry gate status remains unchanged.

M48's opt-in `build_without_input=True` keeps the record input available for
Harness probes but omits it from script execution. Any supplied observation
envelopes are written to `traces/observation_context.json` only after the
path-free context guard accepts them; the signal bundle records its session
identifier, digest, and entry count.

`ObservedBuildLoopRunner` is the M50 offline integration path. It stages the
input for Q01 only, requests bounded observations, sends the path-free
transcript to `FakeLLMProvider`, and runs the returned replacement script with
`build_without_input=True`. It records request/response and observation-query
traces beside the executed revision. It does not construct a hosted provider.

M55 extends this explicit path to multiple manifest cases. Its optional
bounded repair request filters input summaries and local paths, and every
repair execution also uses `build_without_input=True`; the legacy corpus
first-pass command remains separate.

M58 keeps DeepSeek requests in a terminable worker while recording only local,
sanitized lifecycle evidence: worker/HTTP phase names, monotonic elapsed
milliseconds, and an error class. The inner HTTP timeout leaves outer-deadline
grace for a returned error path; an outer timeout still terminates the worker.
These diagnostics are offline review evidence, not a hosted connectivity or
model-quality result.

M60 atomically projects a valid M58 diagnostic into the
`observed-development` interruption checkpoint. The projection is whitelist
validated and never changes issued-request accounting, no-retry semantics, or
the default offline path.

M82 validates the generated script before invoking an executor. It rejects
known unavailable `cadquery` and `OCC` import families, records a local
`build_script_contract` disposition, and does not run a sandbox or provenance
control for a rejected script. This is an API compatibility guard, not a CAD
helper or a geometry gate.

M86 extends the already opt-in two-stage guidance path only offline: the first
provider response selects one preregistered role, and the Harness resolves the
role to the frozen, hash-bound card before accepting a replacement script.
Selection is fail-closed and trace metadata retains the role and card ID, not
raw input, reference scripts, or provider content.  It does not add a hosted
batch, a ranking system, or any new card.
