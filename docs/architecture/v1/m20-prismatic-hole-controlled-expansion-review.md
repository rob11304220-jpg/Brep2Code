---
type: review
related-project: Brep2Code
status: completed
---

# M20-002 Review: Prismatic-Hole Controlled Expansion

## Scope and result

M20-002 preregistered exactly nine `prismatic-hole-v1` rows before candidate
production or audit: three M12 `through_hole` development variants, three new
experimental `counterbore` development candidates, and three M12 `blind_hole`
held-out variants.  The families stayed isolated by split and the grammar
remained `SketchRect -> ExtrudeBase -> CutCylinder`.

All nine cases passed the three offline evidence layers.  Deterministic OCP
replay produced readable STEP with zero bbox, volume, and topology deltas
under the existing Harness gates.  Canonical sequences passed exact
normalization; each counterbore candidate's separately written sequence also
matched its preregistered oracle.  Every row passed its base-length mutation
and its declared hole-radius, hole-depth, or bore-depth mutation.

The new counterbore producer writes only its three experimental candidate
directories.  It normalizes OCP's timestamp and session counter in the STEP
header so a second generation has the same SHA-256 as the checked-in local
asset.  It makes no registry or manifest update.

## Interpretation

The frozen grammar and three-layer audit remained stable for this limited
parameter variation and family-isolated held-out set.  This supports proposing
a distinct governance-promotion workpack if the user elects to do so.

It does not establish generic B-Rep-to-sequence inference, native-history
truth, a model benchmark, automatic case admission, or a general construction
IR.  The counterbore assets are still self-authored deterministic candidates,
not source-history data.

## Governance disposition

Do not change the long-term case-library contract, ADR-0014, active registry,
or executable manifests in this workpack.  Any promotion must be scoped and
accepted separately, including its own ADR if it creates lasting governance.

No experience card was created.  The evidence is bounded to this grammar and
does not meet the criterion for reusable runtime guidance.
