# M97-004 Development Terminal Attribution Review

- **Date**: 2026-08-11
- **Workpack**: `WP-M97-004-development-terminal-attribution-review`
- **Mode**: offline retained-evidence audit; no provider request issued.

## Audit boundary

The audit inspected only the six M97-003 development records named in the
terminal report and their latest M97-003 revisions. It did not inspect a
held-out record, create a replacement script, replay a case, or copy a
provider payload/response into this tracked document.

## Six-condition disposition

| Row | Card | Baseline | Shared boundary checks |
|---|---|---|---|
| low | pass | pass | static OCP contract pass; no input mount; output/geometry gates pass; independent reconstruction |
| nominal | pass | fail | card passes shared checks; baseline has static-contract pass and no input mount, then script error before output |
| high | pass | pass | static OCP contract pass; no input mount; output/geometry gates pass; independent reconstruction |

The six record IDs and report accounting agree with the terminal report:
card conditions consume six issued requests and baseline conditions consume
three, for 9/9 total. All card runs record the fixed guidance role/card; no
baseline record has a guidance result. The nominal pair has the same one-entry
measured-fact transcript SHA-256, so this is not a card-side context substitution.

## Nominal baseline attribution

**Classification: `generated_script_ocp_constructor_arity_error`.**

The nominal baseline passes the static build-script API contract, starts in the
no-input `wsl-bwrap` sandbox, and exits in 5.29 seconds with `script_error`;
it is neither a provider deadline nor sandbox timeout. Retained stderr records
a Python `TypeError`: the generated script calls `BRepPrimAPI_MakeBox` with six
numeric positional arguments, but installed OCP supports only zero, three,
point-plus-three, point-pair, or axis-plus-three argument constructors.
No output STEP is created; output, bbox, volume and topology gates consequently
fail or skip.

This is a trace-supported generated-script API-use failure. It is not evidence
that the measured observation contract, card hash, provider lifecycle, input
mount boundary, or geometry gates malfunctioned. With no permitted second
baseline sample for nominal, the audit cannot estimate a card effect, model
reliability, or parameter generalization.

## Disposition

- Retain this nominal baseline as a development-only API-use counterexample.
- Do not retry, repair, change card/prompt/model, reuse capacity, inspect
  held-out rows, or select M98 from this evidence.
- **Knowledge disposition: no reusable runtime knowledge.**

## Reviewer checklist

1. Confirm the table agrees with the terminal report and 9/9 accounting.
2. Confirm attribution is limited to the retained TypeError and direct gates.
3. Confirm no card-effect, generalization or M98 claim is made.
