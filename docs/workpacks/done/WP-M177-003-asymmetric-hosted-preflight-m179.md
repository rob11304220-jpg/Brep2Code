# WP-M177-003: Asymmetric Hosted Preflight on M179

- Status: done
- Milestone: M177
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Complete fresh local-only preflight for M179's frozen dual-product identities and publish sanitized evidence for independent review, without provider construction or egress.

## Scope

- Audit M175 and the M179 inherited-hash/fresh-identity contract.
- Run M179 local preflight once and admission once; record zero-request, unauthorized checkpoints and the 102 completion-slot / 69 HTTP-request caps.
- Verify only boolean local configuration availability for DeepSeek V4 Pro and `wsl.exe`; never print credential or environment values.

## Boundaries

The future candidate is DeepSeek V4 Pro at `https://api.deepseek.com`: bounded Q01 facts for 30 main cases, those facts plus one hash-bound returned card for three annex cases; serial/no retry, 4096 output tokens, 120-second deadline, 102 completion slots and at most 69 HTTP requests. This is not authorization.

## Acceptance

- M175/M179 audits, M179 preflight/admission, governance and diff checks pass.
- Liaol independently reviews the zero-request local evidence.

## Owner completion boundary

Publish passing sanitized evidence and handoff, then obtain independent G3 review. Do not request authorization or execute hosted work before that review.

## Permitted stop conditions

Independent review, preflight/configuration/hash/identity failure, frozen-input drift, or a request to widen the contract.

## Out of scope

Provider construction/request, credential disclosure, egress authorization, hosted execution, retries, changed cases/cards/model/token/deadline/budget, or runtime/provider changes.

## Closure

Liaol independently approved the G3 review on 2026-08-14. The local evidence
remains zero-request and unauthorized; any hosted execution requires fresh,
itemized user authorization.
