# Governance Health Snapshot

Produce an offline, read-only snapshot of task-lifecycle health:

```powershell
uv run python tools/governance_health.py --format markdown
uv run python tools/governance_health.py --format json
```

The snapshot reports active, backlog, and completed workpack counts, active
handoff count, evidence-ledger dispositions, and the current governance-audit
result. It is a repository-state diagnostic, not a productivity score and not
evidence about Harness, model, or hosted-provider performance.

Run it when reviewing governance changes or selecting a future bounded package.
It reads tracked governance files only, sends no data externally, and does not
modify the repository.
