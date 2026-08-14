# M117 Hosted-Stability Re-entry Evidence Review

## Predicate

A later hosted development calibration can be proposed only after a fresh,
pre-registered stability set establishes all of the following:

1. every request has a parseable terminal report;
2. no issued request ends in a provider timeout or lifecycle error;
3. every report uses the same selected compatibility mode and stays within its
   authorized deadline; and
4. where a script exists, it is locally API-admissible before sandbox launch.

This is a re-entry prerequisite, not a claim about provider availability,
model quality, CAD correctness or any card effect. Old reports, capacities and
authorizations cannot be combined or reused to satisfy a fresh set.

## Retained-evidence assessment

| Record | Relevant terminal fact | Predicate disposition |
|---|---|---|
| M69 | Control completed; paired CAD request timed out after `http_started`. | Fails condition 2. |
| M72 | The only issued request reached terminal `provider_request_timeout`; remaining rows were not started. | Fails condition 2. |
| M80-v2 | Both lifecycle reports completed, but the returned box script imported unavailable `cadquery` and failed execution. | Fails condition 4. |
| M82 | Locally rejects unsupported `cadquery`/`OCC` imports before execution. | A prerequisite control only; no provider-lifecycle observation. |
| M89-003 | One fixed, bounded reference-assisted path completed 2/2 requests and all gates. | A positive bounded observation only; it cannot erase earlier failures or constitute a fresh stability set. |

## Conclusion

The retained evidence does **not** support direct entry into the M115
development calibration. It does support proposing one new, separately chosen
G3 **stability-only** workpack, provided it uses fresh reports, fresh
accounting, a frozen compatible mode and a predeclared no-retry stop rule. Its
read-only preflight must pass before asking the user for itemized hosted
authorization. If any authorized stability request times out, has a lifecycle
error, or returns a static API-inadmissible script, it closes that package and
does not advance to calibration.

M89-003's bounded-output/first-response-byte contract and M82's static API
gate may be adopted only as separately frozen prerequisites in that future
package. Neither supplies a reusable request, report, budget, authorization,
case selection or conclusion.
