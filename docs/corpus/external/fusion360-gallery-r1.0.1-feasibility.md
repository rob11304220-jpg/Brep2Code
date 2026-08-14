# Fusion 360 Gallery Reconstruction r1.0.1 — Offline Feasibility

## Decision

The Reconstruction dataset is a viable first **sequence-supervised candidate**, but it is not admitted. M12-002 reviewed only the official repository, documentation, and license; no archive or source model was downloaded.

The official documentation describes 8,625 reconstruction sequences containing final SMT/STEP B-Rep, JSON construction histories, and per-extrude geometry. Units are centimetres and angles radians. The source license confines use to non-commercial research and forbids redistribution of the complete dataset. See the [official repository](https://github.com/AutodeskAILab/Fusion360GalleryDataset), [reconstruction format documentation](https://raw.githubusercontent.com/AutodeskAILab/Fusion360GalleryDataset/master/docs/reconstruction.md), and [license](https://raw.githubusercontent.com/AutodeskAILab/Fusion360GalleryDataset/master/LICENSE.md).

## Narrow local mapping

| Source element | Local reference interpretation | Admission condition |
|---|---|---|
| `Sketch` closed profile | Profile input for a local deterministic reference script | Line/circle/arc profile only; preserve transform and reference plane. |
| `ExtrudeFeature` / `NewBodyFeatureOperation` | Initial solid extrusion | One body after replay. |
| `ExtrudeFeature` / `JoinFeatureOperation` | Fuse an extruded solid | Existing STEP gates pass after cm→mm conversion. |
| `ExtrudeFeature` / `CutFeatureOperation` | Cut an extruded solid | Existing STEP gates pass after cm→mm conversion. |

Unsupported for the first subset: `IntersectFeatureOperation`, non-distance extents, nonzero taper, two-sided/symmetric extent, unsupported sketch curves, multi-body outcomes, assemblies, and any operation outside Sketch/ExtrudeFeature. A native source history is supervision/reference evidence, not a claim that it is the unique inverse of the final B-Rep.

## Next gate

A new workpack may download the official archive only after confirming the license scope for the intended user and recording the exact source artifact and SHA-256. It must retain the archive under ignored `data/datasets/fusion360_gallery/r1.0.1/`, preserve the official train/test split, select a deterministic single-body subset, replay to local STEP, and pass the existing probe/gates before producing an explicit manifest.
