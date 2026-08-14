# Hosted Terminal Triage

## Purpose

Classify one hosted campaign's terminal outcome into a bounded next action.
This runbook is for post-run interpretation only. It does not replace
preflight, authorization, terminal review, or workpack selection.

## Authority boundary

- `docs/workflow/status.md` remains the task-selection authority.
- The active or completed G3 workpack, frozen policy, terminal report, and
  independent review remain the authoritative sources for one hosted run.
- This runbook may route the next bounded package, but it does not authorize a
  retry, fresh request, provider change, or policy mutation.

## Core rule

Keep these classes separate in every hosted terminal interpretation:

- provider timeout or lifecycle failure;
- script/API failure;
- sandbox/provenance failure; and
- downstream geometry/semantic/editability gate failure.

Do not merge them into one capability score or a cross-policy pass rate.

For a frozen batch epoch, also separate a **condition terminal** from an
**epoch-integrity fault**. A condition terminal is recorded against that fixed
case/condition and normally does not stop other frozen conditions. Only the
epoch's predeclared integrity rules may halt further issuance; any remediation
belongs to a later selected epoch.

## Decision table

| Terminal class | Allowed conclusion | Immediate action | Prohibited shortcut | Next admissible package |
|---|---|---|---|---|
| `pass` | Only this frozen case/policy/gate path completed successfully. | Record terminal review and add the registry row after independent review. | Do not treat one pass as general stability, card efficacy, or portfolio readiness. | A separately selected next campaign for the same family, or one portfolio update package. |
| `provider timeout` / lifecycle failure | Only this fixed request path failed to complete within its frozen lifecycle boundary. | Close the run as terminal, preserve accounting, and register the lifecycle class separately from downstream gates. | Do not infer provider-wide, model-wide, network-wide, or geometry-complexity cause. Do not retry in place. | A fresh hosted-stability or family-scoped re-entry package with fresh accounting, preflight, and authorization. |
| `script/API failure` | Only the generated result failed the frozen output or supported API contract. | State whether the failure is no script, static API rejection, or runtime API failure. Record downstream gates as `not evaluated` when they were not reached. | Do not relabel this as a geometry failure or use the same report path for another try. | A fresh output-contract or family-scoped remediation package, then new preflight if hosted work is still desired. |
| `sandbox/provenance failure` | Only the secure execution or provenance boundary failed on this path. | Preserve the sandbox/provenance evidence and terminate the run. | Do not fill a hosted `pass` from offline oracle results. Do not keep issuing requests under the same package. | A fresh executor-boundary or hosted re-entry package with new paths and authorization. |
| `geometry` / `semantic` / `editability` gate failure | Only this frozen policy reached the applicable gate and did not satisfy it. | Record lifecycle, script/API, sandbox, provenance, and gate states separately. | Do not treat one failing row as a family-wide impossibility claim. | A fresh same-family package with its own frozen question, policy, preflight, and authorization. |
| `interrupted` | Partial evidence only. It is not a reviewed terminal campaign result. | Keep the partial report as evidence only and stop the monitor/process lifecycle cleanly. | Do not reuse remaining request counts or reinterpret the partial state as pass/fail. | A newly selected package only after fresh accounting and authorization. |

## Adjustment budget

Hosted feedback may change only the next bounded package choice. It may not
change the finished campaign.

Allowed adjustment:

- choose which already prepared family goes next when a later hosted slot opens;
- choose whether the next package is hosted-stability re-entry, output-contract
  remediation, family-scoped readiness, or portfolio review; and
- narrow a later question using the retained terminal evidence.

Forbidden adjustment:

- mutate a frozen family charter;
- swap in new rows or held-out inputs;
- tune the current run's token cap, deadline, model, endpoint, or retry policy
  and continue counting it as the same campaign;
- reuse a report path, monitor path, budget, or authorization; or
- treat a bounded success as satisfying another track's gate.

## Route by current portfolio state

When the five-family route is in force:

1. For the frozen M134 epoch, condition terminals are recorded separately and
   the next frozen condition continues unless an epoch-integrity stop occurs.
2. After M135 reaches a terminal state, select M136 for independent epoch
   review before any remediation or next-epoch choice.
3. For prismatic cylindrical cut, continue only from the completed M114/M115
   successor-policy line and its later family-scoped charter records.
4. For repeated-feature, axisymmetric-revolve, dependent-face-selection, and
   multi-inner-loop-pocket, use the completed M123 through M126 planning-only
   charters as frozen inputs. These families remain no-card unless a separate
   reviewed package changes that status.

## Registry recording rule

After independent terminal review, every hosted row added to
`docs/workflow/hosted-experiment-registry.md` should preserve:

- fixed policy/split/case scope;
- request accounting;
- terminal lifecycle status;
- script/API state;
- sandbox/provenance state;
- geometry/semantic/editability gate states, using `not evaluated` when needed;
- one allowed conclusion; and
- one explicit non-inference.

## Related records

- [Four-track program roadmap](../architecture/v1/four-track-program-roadmap.md)
- [Five-family hosted capability delivery roadmap](../architecture/v1/five-family-hosted-capability-roadmap.md)
- [Hosted campaign charter template](hosted-campaign-charter-template.md)
- [Evidence portfolio maintenance](evidence-portfolio-maintenance.md)
- [Hosted experiment registry](../workflow/hosted-experiment-registry.md)
