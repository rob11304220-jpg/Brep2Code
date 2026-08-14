# WP-TRG-003: IR Shadow Experiment

- Status: deferred
- Owner: unassigned

## Goal

Evaluate whether a minimal, auditable operation representation improves repair of repeated dependency and entity-reference failures without replacing the production script path.

## Trigger condition

This workpack may be selected only after two validated narrow helpers show a shared operation-dependency or entity-reference model and completed-case evidence shows that script-level repair cannot preserve a correct prefix.

## Scope

- Preregister a small pilot corpus and a minimal operation set limited to the evidenced families.
- Run IR-derived output in parallel with the existing script path through the current Harness and gates.
- Compare existing gate outcomes, repair burden, and trace auditability without changing historical reports or production generation.

## Inputs

- The two completed helper reviews and ADRs.
- [Post-M9 roadmap](../../architecture/v1/post-m9-evidence-gated-roadmap.md)
- [Runtime boundaries](../../architecture/v1/runtime-boundaries.md)

## Code paths

Determined only after the trigger evidence identifies the minimal operation family.

## Docs to update

Create an ADR for the experimental representation, update contracts and module docs if it creates any new artifact, and update status and handoff.

## Trace/schema changes

Any IR artifact is experimental, versioned, traceable to the source script/case, and isolated from existing production report readers.

## Compatibility constraints

The current Python script path and gates remain authoritative. Default commands stay offline; no full CAD SDK, provider expansion, FEA, VLM judge, or multi-agent execution is introduced.

## Acceptance

- The preregistered pilot has no loss of existing gate outcomes relative to the script baseline.
- The pilot demonstrates lower repair burden and more auditable traces for the evidenced failure family.
- The review explicitly recommends either ending the experiment or opening a separate SDK decision; it does not promote the IR implicitly.

## Status transition

When done, update the required ADR, contracts, status, and handoff before moving this workpack to `done/`. A project CAD SDK remains a separate future ADR and workpack.

## Out of scope

Replacing production scripts, generic modeling language design, CAD SDK implementation, hosted benchmark claims, FEA, VLM judging, and multi-agent orchestration.
