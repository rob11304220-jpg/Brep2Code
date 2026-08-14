---
type: roadmap
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - M7
  - evaluation
  - hosted-provider
---

# M7 Roadmap — Reproducible Generation Evaluation

## Purpose

M6 established bounded hosted repair as an engineering capability, not a model-quality benchmark. M7 moves the project toward comparable first-pass generation evidence and reproducible evaluation while retaining the offline, credential-free default path.

## Delivery sequence

1. **Provider reliability and recovery** — establish offline and loopback evidence for provider deadlines, cancellation, worker cleanup, request accounting, and report recovery before another hosted batch.
2. **First-pass generation evaluation** — distinguish a provider's initial B-Rep-to-script attempt from the current default scaffold and from subsequent repair.
3. **Layered self-authored corpus expansion** — expand the committed, reproducible corpus to approximately 20–50 cases before considering external-corpus ingestion.
4. **Evidence review** — review only completed reports to decide whether new helpers, probes, gates, an IR, or an SDK are warranted.

The corresponding workpacks are M7-001 through M7-003. All three are complete and their acceptance evidence has been reviewed.

## Evaluation discipline

- Default commands remain offline, deterministic, and credential-free. A hosted request requires a new explicit authorization for the provider/model, maximum cases, maximum rounds, timeout, and request or cost budget.
- Each evaluation must retain versioned case-manifest, prompt/policy, provider/model, executor, bounds, latency, request-accounting, and sanitized failure evidence. Hosted results are bounded engineering evidence, never a benchmark or a general CAD-reconstruction claim.
- A completed report is required for aggregate conclusions. A `running` checkpoint or `interrupted` report preserves useful case evidence but is not a completed corpus result.
- Provider-generated scripts continue to execute only through `wsl-bwrap`; reports and traces must not contain credentials, environment snapshots, or full provider responses.

## Architecture escalation gates

Do not introduce a project-level modeling IR, complete CAD SDK, or CAD workplace during M7.

A narrow runtime operation helper may be proposed only when completed evaluations repeatedly show the same attributable OCP/API boilerplate, parameter, or dependency-sequencing problem across multiple cases. The proposal must show that the helper removes that repeated failure without hiding gate evidence.

An IR or SDK requires a separate ADR and completed evaluation evidence demonstrating that narrow helpers cannot represent stable, cross-case operation sequences or their auditable intermediate state. A provider timeout, an isolated failed geometry gate, or a small number of successful repairs is insufficient evidence.

## Scope boundary

M7-003 uses self-authored, committed STEP fixtures with manifests, geometry expectations, and local reference scripts. Public datasets may be assessed in a later, separate workpack covering licensing, selection, normalization, and reproducibility; M7 does not download or run them.

## Evidence inputs

- [M6 hosted evaluation report](m6-hosted-evaluation-report.md)
- [Case corpus contract](contracts/case-corpus.md)
- [LLM provider configuration runbook](../../runbooks/llm-provider-config.md)
