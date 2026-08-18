# Architecture

The implemented pipeline is case loading, Harness-selected path-free geometry
observation, model generation, workspace execution, geometry gates, and
structured repair feedback. The fixed runner uses one observation context; the
active runner adds model-directed bounded probes and approved reference
retrieval behind a provider-neutral action contract. A run contains sessions;
a session contains immutable revisions. Each revision keeps the model exchange,
generated script, execution output, geometry signals, and terminal status.
Runtime models see only assembled prompts, declared tools, the selected case
input, and their revision workspace.

Cases live under `cases/<split>/<case_id>` and are declared exactly once by a
split manifest. Case metadata contains runtime facts and expected geometry but
never a reference solution. Runtime case loading accepts `smoke` and `train`;
the Harness owns evaluation loading and does not expose the `eval` split or its
private comparison material to the runtime model.

The offline Harness requests one complete `build.py` per revision from an
explicit provider. It checkpoints before and after model, execution, and
validation stages. Failed execution or geometry signals become bounded
feedback for the next revision; prior revision files are never modified.

## Fixed and active Harness loops

The fixed runner constructs one model context and permits only a full script
response. Its revision loop is a small form of counterexample-guided
inductive synthesis (CEGIS): propose a CAD program, execute and verify it, then
use a structured failure as a counterexample for the next proposal. It cannot
represent “information is insufficient,” request another observation, or look
up an approved binding reference. `max_rounds` currently combines generation
and repair opportunities.

The implemented active Harness adds a provider-neutral action envelope. The
initial task payload contains only the case identity, unit, initial path-free
observations, available tool declarations, typed budgets, and current revision.
A model turn selects exactly one action with the corresponding payload:

```json
{
  "action": "probe | retrieve | submit | finish",
  "probe": {"tool": "edge_candidates", "arguments": {}},
  "retrieve": {"topic": "TopoDS.Edge_s"},
  "submit": {"script": "complete build.py"},
  "finish": {"reason": "required gates are expected to pass"}
}
```

The controller owns a bounded state machine: `OBSERVING`, `PROBING`,
`RETRIEVING`, `SYNTHESIZING`, `EXECUTING`, `VERIFYING`, `REPAIRING`, and a
terminal `SUCCEEDED` or `EXHAUSTED` state. `probe` performs an allowlisted,
bounded query over the input B-Rep; `retrieve` returns an approved modeling or
binding reference; `submit` supplies a complete candidate script for
compatibility checking, secure execution, and gates. `finish` is advisory: it
cannot bypass execution or verification, and only the Harness verifier may
enter `SUCCEEDED`.

The submission verifier persists each immutable revision, rejects an unchanged
failed repair, applies compatibility diagnostics, checks the execution budget,
and only then enters the secure backend. Stable Python/OCP binding mistakes are
therefore generation counterexamples rather than sandbox attempts and do not
consume execution budget. Compatibility feedback may recommend a
`reference_topic` only when that exact topic exists in the `ocp_symbol`
allowlist; binding knowledge stays in retrieval rather than growing the system
prompt.

The active loop is implemented offline with deterministic providers and for one
fresh hosted runtime case with explicit HTTPS selection and authorization.
Hosted continuation remains HTTP-stub-only. This is the bounded L2 vertical
slice, not a general-purpose agent or authorization for broader hosted cohorts.

This design combines four bounded methods:

- CEGIS supplies typed execution, compatibility, geometry, and semantic
  counterexamples for program repair.
- Active perception treats the target B-Rep as partially observed and lets the
  model spend a probe only when it reduces relevant uncertainty.
- Retrieval-augmented program synthesis supplies approved OCP symbols, binding
  notes, and general modeling recipes instead of growing the system prompt into
  an API cookbook.
- A constrained state machine accounts independently for model requests,
  probes, retrievals, script submissions, executions, repairs, tokens, and
  cost.

Prompt text defines the stable goal, safety boundary, action schemas, visible
data, budgets, and completion rule. Session-local probe results, retrieved
references, candidates, and typed feedback belong to controller state rather
than the permanent prompt.

Evaluation cases occupy the `eval` split and are loaded only by the
Harness-owned evaluation path. Evaluation emits JSON plus a compact Markdown
projection and classifies generation, execution, geometry, provider, and
budget failures. Untrusted execution is a separate secure boundary: if its
verified backend is unavailable, execution fails closed and never falls back
to the trusted local adapter.

## Case-program contract

The project grows through a mechanism-organized hosted case program. A
mechanism definition is shared by cases through
cases/registry/mechanisms.json; a case-local dossier.json binds that
definition to its Harness assets. The dossier is Harness-only metadata. It may
name expected geometry, topology oracles, kernel operations, failure modes,
applicable gates, repair policy, controls, and hosted budgets, but none of
those private fields are assembled into runtime observations.

`capability_level` is the only semantic ladder and is valid for L0 through L6.
The current primitive and analytic-surface cases map to L0, while the ordered
boolean-cut cases map to L1. T0/T1/T2 remain only as an explicit
`compatibility_tier` mapping for the first campaign and must not be used for
capability aggregation or report grouping. This is an initial slice of the
planned L0-L6 ladder, not a claim that all levels are implemented.

The initial L0/L1 development cohort is declared in each dossier as the
ordered coverage tuple `nominal`, `parameter_variation`, and
`failure_sensitive`. The latter requires a negative control; these controls
are Harness assets and are never runtime observations.

The durable expansion order is:

1. Extend the mechanism registry and case dossier schema.
2. Add observation, topology, semantic, and sequence-sensitive gates only when
   a case dossier declares them applicable.
3. Add mechanism-level and capability-level report aggregation.
4. Run a small L0-L2 hosted pilot with nominal, parameter-variation, and
   failure-sensitive coverage where applicable.
5. Add L3-L6 mechanisms and held-out parameter/geometry generalization only
   after the earlier results are interpretable.

This order is a forward design rule, not a progress ledger. The phase boundary
is enforced by schemas and focused tests rather than by session notes or
workpacks.

## Asset and visibility boundary

The geometry asset layer contains input.step, its hash, expected geometry, and
topology counts. The modeling layer contains the registry and dossier fields
for mechanism, operations, dependencies, parameter dimensions, parser notes,
and failure modes. The Harness layer contains gates, repair policy, controls,
split membership, and hosted budget policy. Runtime providers receive only
path-free observations, the declared tool contract, and bounded feedback;
reference, oracle, dossier, registry, repository, and host-path data remain
outside the runtime prompt.

Those assets have distinct roles in the active Harness. STEP is the private
geometry source on which the Harness executes bounded probes. Case metadata
binds runtime facts and expected-geometry validation without containing a
reference solution. The mechanism registry is durable modeling knowledge, and
the dossier binds case-specific gates, controls, held-out fixtures, repair
policy, and hosted budgets. Neither asset is exposed wholesale. An allowlisted
projection layer may derive answer-free OCP API summaries, general modeling
recipes, and kernel binding notes for on-demand retrieval; it must exclude eval
references, target solutions, private oracles, repository content, host paths,
and secrets. Controls and held-out assets test the Harness, while geometry and
semantic gates remain the final authority and the source of CEGIS feedback.
