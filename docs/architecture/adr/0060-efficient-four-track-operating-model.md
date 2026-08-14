# ADR-0060: Run Four Tracks Through Shared Evidence Products

- **Status**: Accepted
- **Date**: 2026-08-11

## Context

The four tracks correctly isolate hosted stability, reference-assisted
construction, parameter variation and modeling-sequence coverage. In practice,
case assets, packs/cards, policies and reports are discovered through different
documents, which can make one case appear to require a new long workflow even
when it contributes only one item of existing evidence.

## Decision

Retain the four tracks and their current gates, but run them through five
shared, read-only work products:

1. **Mechanism dossier**: links required Q01 facts, constrained Q02 action,
   Q03/Q04 gates, counterexamples and supporting cases for one bounded
   mechanism.
2. **Family design freeze** and **family release**: separate preregistration
   from batched production/audit; variants are rows of one release, not
   separate projects.
3. **Card qualification dossier**: records independent direct evidence,
   no-card/wrong-card offline controls and runtime-projection eligibility.
4. **Hosted campaign charter**: freezes policy, split, conditions, accounting,
   interpretation and stop rules before preflight/authorization.
5. **Campaign readiness check**: confirms provider lifecycle, script API,
   sandbox/provenance, applicable gates and fresh-path evidence before a G3
   request is proposed.

These are linkable sections of existing decision packages, workpacks,
contracts and portfolio pages, not new runtime schemas or authorities. At most
one hosted campaign is active at a time; offline family/card/coverage packages
may progress independently when their scopes do not overlap.

## Consequences

- New cases augment an existing mechanism/family dossier by default; they do
  not automatically create a card or hosted request.
- Hosted work is spent only on a question that cannot be answered by the
  frozen offline controls, and terminates at its predeclared evidence class.
- Each G2/G3 package still follows the existing reviewer, workpack, preflight
  and authorization rules. This ADR cannot select M98, alter M73's gate or
  reuse a prior budget.
