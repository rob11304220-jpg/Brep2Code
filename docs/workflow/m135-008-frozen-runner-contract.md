# M135-008 Frozen Runner Contract

- **Date**: 2026-08-12
- **Workpack**: `WP-M135-008-frozen-runner-contract`
- **Scope**: offline-only; no provider construction, credentials or egress

## Frozen request boundary

Every condition constructs exactly one `ProviderRequest` locally. Its system
instruction is the shared no-input build instruction with SHA-256
`f22e625ea874a7ecec10a0bc88b37f40ec05cb4086a4f777dcde9d3a5d19d7a1`;
the user message is the pre-existing path-free frozen transcript. The request
keeps the M135 `deepseek-v4-pro` model, no output-token cap and `single_request`
metadata; this function does not construct or call a provider.

For the three prismatic `card` rows only, the third and final message is the
direct `get_guidance_card` tool message for the declared `single boolean-cut
tool` role. The source card SHA-256 is
`55341683e3e7df3e058a845193e34fba20b0650c0db28a31489ad5d343b60d30` and
the exact existing direct-guidance JSON injection bytes have SHA-256
`e43c0599d133f86ed3f11ba9e15b907f9a37af4098b8a0645611910c3f0c54de`.
No-card rows have precisely two messages and no card hashes.

## Request-to-terminal boundary

The fake-provider regression submits the same direct-card bytes through
`ObservedBuildLoopRunner`, whose no-input `ManualHarness` uses
`WslBubblewrapExecutor`. No completion is classified successful solely because
a script was returned. Provider paths ending before a Harness result map to
`lifecycle_ended_before_script`; card scripts first pass M115's static API
classifier, otherwise map to `static_api_inadmissible`; nonzero sandbox exit
maps to `sandbox_execution_failed`; a non-passing completed Harness result maps
to `downstream_gate_failed`; only a passing Harness result maps to
`full_success`.

This is local Harness compatibility evidence only. It is not hosted model,
card-effect or readiness evidence, and it does not authorize a serial runner,
provider construction or a request.
