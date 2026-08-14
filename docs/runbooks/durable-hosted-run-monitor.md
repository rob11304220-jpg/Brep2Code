# Durable Hosted-Run Monitor

Use M70's monitor only after a hosted process has separately passed preflight and received explicit authorization. It reads the existing report once per invocation and writes a separate local state file. It never launches, signals, retries or resumes a process; it does not construct a provider, read credentials or change a corpus report.

For a monitorable single-request run, the request producer must first use its
explicit `--phase prepare` operation. That operation atomically writes its own
content-free `running` report with `request_state: prepared`; only then may a
monitor attach. After setup, invoke the same command with `--phase execute`.
The producer changes the report to `issued` immediately before the request and
writes the terminal result. Never create that report by hand or ask M70 to do
so.

## Setup

Choose a new monitor-state path distinct from the report path:

```powershell
uv run brep2code monitor setup --report data/corpus-runs/new-authorized-run.json --state data/monitor-runs/new-authorized-run.monitor.json --stale-after 300
```

`setup` records the report path, heartbeat, lifecycle phase and stale window. A missing, malformed or stale `running` report writes an `operator_action_required` handoff and stops monitoring. It does not infer process health or try another request.

## Observe and hand off

Invoke observation from the durable task mechanism while the process remains authorized:

```powershell
uv run brep2code monitor observe --state data/monitor-runs/new-authorized-run.monitor.json
```

For a still-`running` report, the monitor increments its heartbeat and labels an unchanged report `no_progress`. `completed` and `interrupted` reports become terminal monitor state with an operator handoff. A terminal or operator-action state is immutable under further observation: inspect the report and obtain new hosted authorization before any new run. Historical budgets and remaining-request counts are never reused.

## Teardown

End only the monitor lifecycle with:

```powershell
uv run brep2code monitor teardown --state data/monitor-runs/new-authorized-run.monitor.json
```

This records `operator_teardown` in monitor-owned state and leaves the report unchanged. It cannot terminate or resume the hosted process.
