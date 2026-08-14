---
type: contract
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - contract
  - case-corpus
---

# Contract: Case Corpus

The M4 case corpus is a small manifest-driven review workflow. It exists to collect concrete Harness evidence before adding larger datasets or modeling abstractions. Hosted-provider evaluation was implemented in completed `WP-M6-001` and remains opt-in.

## Manifest

The manifest is structured data with one entry per case.

Required fields:

| Field | Meaning |
|-------|---------|
| `case_id` | Stable id used in record ids and reports |
| `tier` | `P0`, `P1`, `P2`, or `P3` |
| `input_step` | Repository-relative STEP input path |

Optional fields:

| Field | Meaning |
|-------|---------|
| `expected_bbox` | Expected bbox sanity data |
| `expected_counts` | Expected topology counts |
| `expected_volume` | Expected volume |
| `difficulty_tags` | Short tags such as `box`, `hole`, `boolean` |
| `first_pass_script` | Repository-relative deterministic script fixture used only by local fake `--first-pass` generation |
| `reference_script` | Repository-relative replacement script for fake-provider replay |
| `notes` | Short implementation-side note |

Current committed manifests:

| Manifest | Tier | Cases |
|----------|------|-------|
| `case-library/manifests/self-authored/p0.json` | P0 | `box`, `cylinder`, `block_with_hole` |
| `case-library/manifests/self-authored/p1.json` | P1 | `filleted_block`, `chamfered_block`, `three_hole_plate`, `box_cylinder_union` |
| `case-library/manifests/self-authored/p2.json` | P2 | Nine self-authored multi-operation feature-interaction cases; see `docs/corpus/m7-003-coverage.md`. |
| `case-library/manifests/self-authored/p3.json` | P3 | Five self-authored scale, orientation, proportion, and topology-pair cases; see `docs/corpus/m7-003-coverage.md`. |

## Runner

For each case, the runner should:

1. Resolve repository-relative paths.
2. Execute `ManualHarness` with the case STEP input.
3. Collect revision id, status, gates, probe summaries, and failure classification.
4. If `reference_script` is present and the first run fails, optionally replay through the local fake-provider repair loop.
5. In explicit hosted mode only, send failed primary cases to the selected provider through the bounded repair loop; provider-generated revisions require `wsl-bwrap`.
6. Atomically checkpoint the compact corpus-level report before the first case and after every completed case.
7. Write a terminal `completed` report, or on a handled interruption/runner exception write `interrupted` with the current case id and a non-sensitive interruption classification.

Default runs must not require network access, credentials, hosted LLM SDKs, or external dataset downloads.

An external-data manifest is an explicit local-development input, never a default fixture. Its raw inputs must remain under ignored `data/datasets/<dataset>/<release>/`; the tracked selection record must retain upstream release, source identity, SHA-256, local-only licensing boundary and any normalization decision. It must not contain a `reference_script` or `first_pass_script` unless a later separately approved workpack establishes a lawful, reproducible source for that artifact.

Development-side source and asset relationships are indexed in [`docs/corpus/library/`](../../../corpus/library/README.md). That index is not an executable manifest and cannot activate a source, relocate a fixture, or change this contract's explicit-path requirement.

`corpus --first-pass` is an explicit generation mode. Before executing a generated script, it supplies the provider only a bounded `probe_summary` context and requires a complete replacement `build_sequence.py`. In local fake mode every selected case must provide `first_pass_script`; a missing fixture is a preflight error and no case runs. `--first-pass --repair` keeps repair explicit: the first-pass result is recorded separately and a failing case may use `reference_script` only as a local fake-provider replay. Existing corpus runs and local `--repair` runs do not enable first-pass generation.

The first-pass input summary uses the same bounded input-probe path as Harness. If it is unavailable, no provider request is constructed or issued; the schema-v3 case records `input_probe_failure`, `provider_requests: 0`, and the structured input summary. This is distinct from a provider failure and does not consume the request budget.

Hosted mode requires all of the following before any request: an explicit caller authorization flag, a positive case bound, a positive per-case round bound, a positive request budget within the applicable maximum, a positive provider-request timeout, valid local provider configuration, and an available secure executor. The maximum is `max_cases × max_rounds` for ordinary hosted repair and `max_cases × (1 + max_rounds)` for hosted `--first-pass`, which includes one initial generation request plus up to `max_rounds` repair requests per case. If the initial secure execution reports an unavailable or unsandboxed backend, the case is classified as `sandbox` and no provider request is made. Local fake-provider replay (`--repair`) and hosted mode are mutually exclusive.

## Reliability and recovery review

Provider lifecycle behavior must be established with offline or loopback tests before a new hosted batch. The review covers provider-request deadlines, worker termination, request issuance accounting, atomic checkpoints, and the distinction between a handled interruption and an externally killed process. It must not infer provider/model quality from a timeout.

The locally retained provider-lifecycle diagnostics are additive and deliberately
minimal: `last_phase`, an ordered `events` list of phase names with monotonic
elapsed milliseconds, and a sanitized `error_class`. They distinguish an
unobserved worker startup, an HTTP attempt still in flight at the outer
deadline, and an error returned by the worker. They must not contain request
content, credentials, URLs, local paths, raw provider output, environment
values, or timeout configuration.

`running` is an atomic checkpoint, not a successful aggregate result. `completed` means the runner reached its normal terminal report. `interrupted` means the runner handled an interruption or runner exception and retained completed case evidence. An external force-stop cannot reliably write a terminal report; the preceding checkpoint is valid partial evidence only. A request is counted when issued, including when its response later times out or fails.

Any targeted hosted validation after a reliability review still requires a new explicit authorization stating the provider/model, case bound, round bound, provider timeout, and request or cost budget. Default corpus and local fake-provider commands remain offline.

## Report

Each case result should include:

| Field | Meaning |
|-------|---------|
| `case_id` | Case id from manifest |
| `tier` | Case tier |
| `record_id` | Harness record id used for the run |
| `revision_id` | Primary Harness revision id |
| `status` | Primary Harness status, normally `pass` or `fail` |
| `gate_statuses` | Compact map from gate name to gate status |
| `provenance` | Additive M46 provenance classification and attestation, when available |
| `reconstruction_eligible` | True only when provenance is `independent_reconstruction`; separate from geometry health/status |
| `probes` | Compact input/output probe summaries from `signal_bundle.json` |
| `failure_type` | Classification such as `script_failure`, `missing_output`, `output_probe_failure`, `input_probe_failure`, `gate_failure`, or `unknown_failure` |
| `signal_bundle_path` | Path to the primary revision signal bundle |
| `repair` | Optional fake-provider replay summary from `RepairLoopRunner` |
| `repair_failure_type` | Optional hosted-repair classification: `provider_request`, `provider_response`, `repair_exhausted`, or `unknown` |

Every report includes `run_status`: `running`, `completed`, or `interrupted`. An `interrupted` report additionally contains a non-sensitive `interruption` object with a code, the current case id, and (for a runner exception) only the exception type. It preserves all prior completed case results and is atomically replaced after each checkpoint. A hosted provider request runs in a separately terminable worker; when it exceeds `provider_timeout_seconds`, the repair summary records `provider_request_timeout` and the case remains a completed checkpoint rather than blocking the corpus process.

The separate M135 fixed-epoch preflight checkpoint is local preparation, not a
corpus result. Its `epoch_contract` records only the frozen executor,
provider/model identifiers, deadline, optional token cap, zero repair/retry,
18-request cap, monitor identity and `not_authorized` state. A new checkpoint
must have distinct fresh report and monitor paths and starts at zero issued
requests. It never records a credential, raw provider content, raw STEP,
absolute input path or outbound transcript.

For `observed-development`, an interruption caused by a validated M58 worker
lifecycle error may additionally include `diagnostics`. Its schema is strictly
limited to `last_phase`, phase events with monotonic elapsed milliseconds, and
a sanitized `error_class`; malformed or surplus fields are omitted. This
additive local evidence does not alter the request count, retry policy, or the
need for a fresh authorized batch.

M65 observed-development case entries may include a `telemetry` object. Its
versioned `context_ledger` contains only section character/UTF-8-byte counts
and message count; it contains no prompt content. `request_timing` records
send/done offsets relative to case start. Its `first_byte_offset_ms` is
nullable and, when present, records only first-response-body-byte timing; no
byte content is retained. `token_usage` remains null when unavailable.
`phase_elapsed_ms` separates local input preparation, observation, provider
wait, Harness, and end-to-end elapsed milliseconds. These fields are diagnostic
evidence, not token estimates or provider-quality claims.

For an observed-development provider timeout or lifecycle error, M66 projects
the same strict telemetry whitelist beneath `interruption.telemetry`. Its
response-dependent `done_offset_ms` and `token_usage` remain null; a timeout
may retain a first-response-byte lifecycle event if it was observed before the
worker was terminated. This does not alter the terminal interruption or
request count.

M68 adds the `http_response_completed` lifecycle phase for a worker that has
received and parsed a complete provider response. Sanitized response metadata
may expose only `http_status_class` and `provider_request_id_present`; neither
headers nor a request-id value are retained. M89-002 adds a first-response-body
byte lifecycle event and nullable timing offset without retaining response
bytes or changing the non-streaming request mode.

Local reports retain schema version 1 and include `run_id`, `manifest`, `summary`, and `cases`. Hosted repair reports use schema version 2 and additionally include a sanitized `evaluation` object: provider/model identifier, repair policy identifier, executor, authorization marker, case/round/request bounds, `provider_timeout_seconds`, and requests used. First-pass reports use schema version 3 and add a versioned `generation_policy`. Each v3 case contains nullable `primary_generation`, `repair`, and `fake_provider_replay` fields. `primary_generation` records the generated-script Harness outcome, bounded probe summary, request count, duration, and trace references; `repair` is reserved for hosted repair; `fake_provider_replay` is reserved for explicit local replay. Neither report variant may contain credentials, environment snapshots, or full provider responses.

The report is evidence for review, not a benchmark score.
