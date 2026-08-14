# Frozen Hosted Campaign Launcher

Use this runbook to prepare one versioned campaign locally.  It is an offline
procedure: it does not authorize provider construction, credential access or
egress.

## Prepare

1. Create a reviewed `campaign.json` conforming to the [launcher contract](../architecture/v1/contracts/frozen-hosted-campaign-launcher.md).  The case must be registered and development-split; record the exact input and split-authority SHA-256 values.
2. Include only allowlisted Q01 facts in `q01.transcript`; never include raw
   STEP, a local path, a reference script, a provider response or held-out data.
3. Use `reference.mode: "none"` or an explicit registered card ID with index,
   card hashes and one declared role.  M139 accepts only `repair_policy: none`
   and `max_repair_rounds: 0`.
4. Choose fresh, distinct report and monitor paths, then run:

```powershell
uv run python -m brep2code.cli campaign-prepare `
  --spec path\to\campaign.json `
  --report data\campaign-preflight\campaign-report.json `
  --monitor-state data\campaign-preflight\campaign-monitor.json
```

5. Retain the `prepared_offline` report only as local preflight evidence.  Do
   not reuse the paths as a later campaign or infer any remaining request
   capacity.

## Later execution boundary

This runbook deliberately has no execute command.  A future selected G3
workpack must revalidate the unchanged prepared checkpoint, complete all
hosted preflight gates and obtain itemized authorization for destination,
model, outbound content, case scope, repair/retry bound, deadline, budget,
executor and fresh report/monitor paths.
