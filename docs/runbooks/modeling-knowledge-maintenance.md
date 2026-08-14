# B-Rep Modeling Knowledge Maintenance

Use this runbook after a case-family design, controlled production, replay
diagnostic, or evidence review that could change the project's modeling
knowledge. It implements ADR-0022.

1. Identify the Q01--Q04 decision gap and the coverage-matrix cells the work
   addresses. State the required observable, constrained hypothesis/action,
   expected evidence, counterexample, and stopping rule before candidate
   production. Do not select a case merely to increase feature or case coverage.
2. After review, update `coverage-matrix.json` with the actual evidence and
   remaining gap. Do not mark a gap closed from a single case-local result.
3. Classify each new case as oracle, discriminating control, negative control,
   regression, OOD robustness, or native-history validation. Record its role in
   the relevant preregistration/review and link it to the decision it tests.
4. Create or revise a modeling knowledge unit only when its bounded operation
   or pattern, B-Rep observables, prerequisites, sequence/dependencies,
   supporting cases, counterexamples, and review trigger are all recorded.
   Where the evidence supports an operation claim, fill its `operation_contract`
   with function family, parameter domain, expected B-Rep delta, topology
   invariants, numeric/tolerance boundary, and unverified properties. Do not
   invent a kernel/API signature or numeric tolerance that the tracked evidence
   does not establish.
5. Put the claim in its appropriate layer: `observables/` for Q01 measurement
   and ambiguity boundaries, `operations/` for Q02 constrained sequences,
   `execution/` for Q03/Q04 reusable gates/diagnostics/repairs, or `patterns/`
   for cross-layer counterexamples. Until a new layer has a reviewed entry, do
   not create placeholder facts merely to populate it.
6. Link authoritative case records, tracked audits, and architecture reviews;
   never copy ignored traces, provider messages, secrets, or complete
   workpacks into a unit.
7. If evidence is not reusable, retain the counterexample or explicitly record
   no reusable knowledge in the review. Do not create a positive unit merely
   to fill a matrix cell.
8. Treat the reviewed unit as a development-side modeling reference only. For a
   runtime card, analysis, helper, IR, or SDK proposal, first apply the distinct
   evidence and approval gates in
   [`modeling-knowledge-adoption.md`](../architecture/v1/modeling-knowledge-adoption.md).
   An experience card remains a compact projection and must follow
   `runtime-guidance-cards.md`; ADR-0016's evidence threshold and M19 evaluation
   boundary still apply.
9. Run JSON/schema validation when introduced, focused audits for linked case
   changes, and `git diff --check`. Update the relevant workpack, status, and
   active handoff.

10. When a changed source participates in the development-evidence crosswalk,
    update its declared relationship and SHA-256 only after the source itself is
    correct; then run `python tools\audit_development_evidence_crosswalk.py`.
    The crosswalk is derived navigation. Do not resolve drift by reading
    fixtures, reference scripts, held-out inputs, or runtime resources.

11. When a reviewed source explicitly changes a case-evidence role, update the
    companion mapping only with the already declared relationship; retain
    held-out evidence as documentary-only. Run
    `python tools\audit_case_evidence_relationships.py` and the crosswalk audit.
    The mapping cannot supply lifecycle, split, hash, manifest, admission, or
    runtime authority.

For a legacy-evidence migration, do not infer a claim from a catalog entry.
First add one disposition in `evidence-disposition.json`: reviewed knowledge
unit, reviewed boundary/counterexample, or retained asset with no reusable
knowledge. Link any existing experience card through that disposition. A
decision package may name a new gap but cannot relax a linked workpack's entry
condition.

The knowledge system cannot change case lifecycle, executable manifests,
runtime retrieval, provider use, training input, or kernel behavior.
