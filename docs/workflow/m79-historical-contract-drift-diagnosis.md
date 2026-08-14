# M79 Historical Contract Drift Diagnosis

- **Date**: 2026-08-10
- **Workpack**: `WP-M79-001-historical-contract-drift-diagnosis`
- **Mode**: offline comparison only; no provider constructed or contacted

## Decision-use summary

The retained M51 result establishes one earlier successful minimal path: P0
`box` passed its no-input `wsl-bwrap` build and all existing geometry gates.
The later M72 timeout instead occurred for P2 `param_additive_boss_low`, after
the provider worker started HTTP and before any response or generated script.
Those cases are not comparable as a test of CAD-task complexity.

The committed request path from the M51/M52 implementation point to the
current implementation is structurally equivalent for the one-request
observation-to-build payload: the same model/endpoint family, non-streaming
JSON-object envelope, response replacement contract, path-free observation
policy, and no-input executor boundary remain. Current additions are request
telemetry, lifecycle/report fields, and a multi-case adapter; they do not
alter the single-case outbound instruction or transport fields.

Exact historic payload equality is **unknown**, not assumed. Sanitized reports
do not retain raw prompts, responses, headers, credentials, or payload hashes.
Therefore M79 does not attribute the M72 timeout to prompt drift, task
complexity, the provider, or the network.

## Evidence matrix

| Field | Earlier successful evidence (M51) | Current / M72 evidence | Disposition |
|---|---|---|---|
| Case and input | P0 `box`; input SHA-256 `C3C80420EAF7376DA5675EC1D5EA8FA93EF7A60F7EE24A516454C71E0797227C`; all gates passed. | M72 used P2 `param_additive_boss_low`; its recorded SHA-256 differs. | Different input and difficulty; M80 must use `box`. |
| Provider/model/endpoint | DeepSeek `deepseek-v4-pro`; M51 closure records one successful request. | DeepSeek `deepseek-v4-pro` at `https://api.deepseek.com`; M72 reached `http_started` then timed out at 300 s. | Structurally equivalent configuration; actual remote service state is unknown. |
| Transport envelope | M52/M51 single-case adapter used the DeepSeek JSON-object path. | Non-streaming Chat Completions JSON-object request; no `stream`; no output cap. | Equivalent at the committed-contract level. |
| System-instruction contract | Source at the M52 implementation point contains the same observation-build instruction and adapter response envelope. Historic emitted bytes/hash were not retained. | Current hashes: observation-build instruction `acc94d8f5092679fab58497c941020b5b442c2779b0000ea63fe7fcfa0de86a5` (145 UTF-8 bytes); adapter instruction `5d71eb57800082c6977a7ed287e3d38f41fa0a238a46c56f35299ce13d94d3e9` (522 UTF-8 bytes). | Source-equivalent; exact historic payload hash unknown. |
| Observation policy | M51 used the M48 path-free bounded transcript for `box`. | M72 used the same M48 path-free bounded transcript policy, with one `probe_summary` call. | Equivalent policy, different B-Rep-derived transcript. |
| Observation transcript length/hash | Not retained in the M51 closure evidence. | M72 retained content-free telemetry only; no transcript hash/length is available in the tracked report. | Unknown; M80 preflight must record current content-free counts/hash. |
| Request deadline and accounting | One first-pass request, no repair; historic deadline value is not retained in the M51 closure text. | One request, no repair, 300-second provider deadline; it is consumed. | Historic deadline unknown; M80 freezes a new value and never reuses either budget. |
| Executor and gates | `wsl-bwrap`, no original STEP mount; script exit, readable STEP, bbox, volume, topology all passed. | `wsl-bwrap` was preflighted, but no generated script reached execution. | Same boundary; only M51 has successful generated-build evidence. |
| Lifecycle/report schema | M51 has a terminal success summary but no preserved raw report in this checkout. | M72 terminal `interrupted`, one request used, `worker_started` and `http_started`, with count/timing-only telemetry. | Schema/telemetry evolved; it does not change outbound semantics. |

## Noise and interpretation controls

1. **Do not compare M72 to M51 as matched task samples.** `box` is a primitive;
   `param_additive_boss_low` is a different P2 model. The successful M51 case
   is nevertheless the correct minimal regression for verifying the route.
2. **Do not call the current goal “history recovery.”** The runtime returns a
   replacement `build_sequence.py`, assessed for a geometry-equivalent STEP;
   it does not prove recovery of the source CAD feature history. M73, not M80,
   is the output/repair-contract gate.
3. **Do not infer prompt drift from redaction.** Source comparison finds no
   material single-case outbound-contract change, while privacy-preserving
   evidence makes byte-for-byte historic equality unavailable.
4. **Do not infer a global outage from M72.** M64's fixed provider control
   completed within its separate 120-second bound; it only rejects a blanket
   endpoint/authentication failure, not request-specific server or transport
   behavior.
5. **Keep the control and box requests separate.** A successful control is a
   lifecycle baseline only. It does not make the box outcome predictable, and
   either failure stops M80 without retry.

## reproduction-profile-v1

This profile freezes only observable, current fields for an M80 preflight. It
does not select credentials, authorize egress, or reserve request capacity.

| Field | Frozen value for later preflight |
|---|---|
| Control | `provider-control-v1`; one request; content is the existing fixed control and must remain absent from reports. |
| B-Rep case | P0 `box`, `case-library/self-authored/box/input.step`, SHA-256 `C3C80420EAF7376DA5675EC1D5EA8FA93EF7A60F7EE24A516454C71E0797227C`. |
| Build policy | `q01-observation-build-v1`; one `probe_summary` call; path-free M48 transcript only; freeze its current count and SHA-256 during read-only preflight. |
| Provider contract | DeepSeek configured model and endpoint must be checked non-secretly; Chat Completions non-streaming JSON-object envelope; no `stream`, no `max_output_chars`, no temperature override. |
| Instruction identities | Observation-build SHA-256 `acc94d8f5092679fab58497c941020b5b442c2779b0000ea63fe7fcfa0de86a5`; adapter SHA-256 `5d71eb57800082c6977a7ed287e3d38f41fa0a238a46c56f35299ce13d94d3e9`. A mismatch stops preflight. |
| Execution | `observed-first-pass`, `wsl-bwrap`, no original STEP mount, zero repair rounds, exactly one request budget. |
| Reports and monitors | Two fresh paths, one request capacity each, each observed by an M70 monitor; no `running` or `interrupted` checkpoint may be reused. |
| Deadline | A single positive provider deadline must be stated in fresh preflight and separately authorized. It is deliberately not inferred from M51. |
| Success condition | Control terminal and parseable without timeout/lifecycle error, then box terminal and parseable with script exit, readable output, bbox, volume, and topology gates passing. |

## Limits

This diagnosis is not a causal experiment and has made no hosted request. The
profile is ready for independent review only; M80 still requires acceptance of
M79, a new full G3 preflight, and explicit itemized authorization.
