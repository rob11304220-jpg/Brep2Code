# M85 Reference-Assisted P0 Hosted Preflight — Authorized

- **Date**: 2026-08-10
- **Workpack**: `WP-M85-001-reference-assisted-p0-hosted-smoke`
- **Mode**: read-only local preflight completed; hosted execution authorized

## Fixed authorization

- Destination/model: `https://api.deepseek.com`, `deepseek-v4-pro`.
- Case: P0 `cylinder`; input SHA-256 `B1CDEB7A6E3DA089EF401BDF101048476033C4F9BF44E635266F4DCC45B46EDA`.
- Reference: top-k one, role `final primitive`, index SHA-256 `DFA731D597581B3B4D306782C1078C7DE5B79672462229BAAF5D7248FA230517`, card SHA-256 `55341683E3E7DF3E058A845193E34FBA20B0650C0DB28A31489AD5D343B60D30`.
- Egress: first a bounded path-free observation transcript; second the same transcript plus the compact derived card. No raw STEP, host path, reference script, unrestricted file data, credentials, headers, or prior reports.
- Budget: exactly two sequential requests, zero repair, zero retry, 120 seconds per request.
- Executor/paths: `wsl-bwrap`; new report `data/corpus-runs/m85-cylinder-reference-assisted.json`; new monitor `data/monitor-runs/m85-cylinder-reference-assisted.monitor.json`.

## Preflight evidence

- `cylinder` is a P0 manifest member and both report paths were absent.
- Provider configuration selected the authorized endpoint/model; only key presence was checked.
- Local no-input `wsl-bwrap` cylinder reference execution passed contract, sandbox, output, bbox, volume, topology and no-input-access checks.
- The M85 durable lifecycle records `0/2`, then `1/2` and `2/2` before the two provider boundaries. A failure terminalizes the report and never resumes capacity.

## Authorization

Liaol explicitly authorized the fixed scope above on 2026-08-10.
