# ADR-0008: Give Input B-Rep Summary a Separate Bounded Deadline

- **Status**: Accepted
- **Date**: 2026-08-02

## Context

Two local ABC v00 inputs with 253 faces required roughly 25--30 seconds for STEP loading and complete summary. The former shared 15-second probe deadline terminated them and then allowed a Harness pass because comparison gates were skipped. Hosted first-pass generation also computed its initial input summary without a process deadline.

## Decision

- Run all summary probes in a process-isolated shared helper.
- Allow input-model summaries up to 45 seconds; retain the 15-second limit for generated output artifacts.
- Treat an unavailable supplied input summary as an explicit failing `input_model_step_readable` gate.
- Require first-pass generation to obtain the bounded input summary before constructing or issuing a provider request; on failure, record zero provider requests and a structured `input_probe_failure`.

## Consequences

- Complex but valid inputs receive a bounded opportunity to load without weakening output-artifact containment or provider deadlines.
- Input probe failure can no longer create a false passing revision, and corpus reports distinguish it from provider and geometry failures.
- Default execution remains offline; no probe timeout decision authorizes a hosted request, changes geometry tolerances, or introduces a CAD abstraction.
