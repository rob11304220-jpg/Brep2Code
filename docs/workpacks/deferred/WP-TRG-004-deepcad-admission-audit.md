# WP-TRG-004: DeepCAD Offline Admission Audit

- Status: deferred
- Owner: unassigned

## Goal

Assess DeepCAD as a second sequence-supervised source only if documented
Fusion evidence identifies a representation or coverage blocker.

## Trigger condition

A review records the specific unsupported Fusion operation or representation
and why the existing cache cannot answer the next paired-data question.

## Scope

- Review official source, release identity, license and redistribution terms.
- Map the construction-sequence representation to a deterministic local replay
  hypothesis and define the smallest offline feasibility checks.
- Record whether paired B-Rep/history evidence can be reproduced locally.

## Compatibility constraints

This is documentation and offline feasibility review only: no dataset download,
sample selection, manifest, provider request, hosted execution, or Harness
behavior change is permitted.

## Acceptance

- The review states a bounded recommendation: reject, defer, or open a
  separate local acquisition/replay workpack.
- It records the precise Fusion blocker, source/license boundary, representation
  compatibility, and planned validation before any acquisition decision.

## Out of scope

Dataset acquisition, general CAD SDK design, IR promotion, and benchmark use.
