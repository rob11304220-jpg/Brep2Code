# ADR-0084: Use an Asymmetric Hosted Denominator

- **Status**: Accepted
- **Date**: 2026-08-14

## Context

M172 required three equal ten-case strata, including twenty distinct cases with
an explicit runtime CAD card. The current card has direct evidence for only
three declared roles. The library has development-governed no-card candidates,
but a reference pack, script, or parameter family does not establish card
eligibility.

## Decision

Redesign the route into a 30-case, development-only no-card main cohort and a
separate three-case card-assisted closed-loop feasibility annex. The main cohort
reports bounded no-card terminal behavior; the annex preserves the existing
three direct card roles and M170-style closed-loop evidence. Neither is a
card-effect estimate, and their denominators are never pooled.

## Consequences

The main cohort may use the existing no-card evidence only after M173 audits
each row. The annex may use exactly one explicit hash-bound card per existing
role; it cannot expand card scope. M174 must reconcile the current authoritative
registry count with the older M145 descriptive report before row qualification.
No hosted request, provider authority, manifest, runtime change, or repair
policy widening follows.
