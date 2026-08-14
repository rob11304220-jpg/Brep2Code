---
type: contract
related-project: Brep2Code
version: v1
status: active
---

# Contract: Frozen Hosted Campaign Launcher

## Artifacts

`campaign.json` is immutable, provider-independent campaign intent.  It may
reference local authorities but no local path is included in outbound content.
`campaign-report.json` is a fresh atomic checkpoint that binds the canonical
spec digest and all derived local digests after offline preflight.

## Campaign-spec minimum fields

```json
{
  "schema_version": 1,
  "campaign_id": "example-development-r1",
  "case": {
    "case_id": "registered-case",
    "input_sha256": "<sha256>",
    "data_split": "development",
    "split_authority": "<repository-relative preregistration>",
    "split_authority_sha256": "<sha256>"
  },
  "q01": {"transcript": {"schema_version": 1, "...": "allowlisted facts"}},
  "reference": {"mode": "none"},
  "generation": {"first_pass": true, "repair_policy": "none", "max_repair_rounds": 0},
  "execution": {"provider": "deepseek", "model": "deepseek-v4-pro", "executor": "wsl-bwrap", "provider_deadline_seconds": 120, "max_output_tokens": 4096, "max_requests": 1}
}
```

The exact Q01 schema is profile-specific.  Its canonical JSON SHA-256 is
computed locally and recorded in the checkpoint; only the validated transcript
may later cross the provider boundary.

## Prepare invariants

Prepare must reject when any of the following fails: schema/identity shape,
case input hash, split membership/hash, transcript data split, card registry or
hash/role, zero-repair policy, request arithmetic, deadline/token bounds,
fresh/distinct report-monitor paths, or no-input executor control.  It writes:

```text
run_status=running
request_state=prepared
authorization=not_authorized
provider_constructed=false
requests_used=0
```

Monitor setup remains read-only with respect to this report.  A prepared report
does not supply hosted capacity; an existing path is never reusable.

## Future execute boundary

Future G3 execution must require explicit itemized authorization and compare
the checkpoint's campaign identity to the spec before provider construction.
It must not accept execution-time overrides for input, Q01 transcript, card,
repair policy, model, executor, deadline, token cap, request cap or report/
monitor identity.
