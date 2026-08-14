# ADR-0066: Freeze One Bounded `shell-v1` Family

- Status: Accepted
- Date: 2026-08-11

## Decision

Select `shell-v1`, not `rib-v1`, as the next isolated complex-topology family. Freeze a rectangular solid with its complete top face removed by one inward uniform-thickness thick-solid operation. The preregistration contains three symmetric development and three asymmetric held-out rows, with no substitutions.

## Boundaries

The family requires one solid, exactly one complete top opening, uniform side and bottom wall thickness, unchanged outer bbox, and no bottom breakthrough. It excludes multiple/side/bottom openings, variable thickness, ribs, finishing operations, partitions and multi-solid output. This is an offline design only; candidate production, manifests, runtime/provider use and hosted evaluation require separate workpacks.

## Rationale

This advances the first unselected Order-6 coverage hypothesis while retaining a finite oracle and explicit complex-topology stop conditions. It makes no general shell-recognition or B-Rep-to-sequence claim.
