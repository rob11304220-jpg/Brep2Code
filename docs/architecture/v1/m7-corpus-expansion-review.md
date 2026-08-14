# M7-003 Corpus Expansion Review

## Evidence reviewed

The committed self-authored corpus now contains 21 cases: P0=3, P1=4, P2=9, and P3=5. P2/P3 add multi-operation feature interactions, feature placement/depth/orientation, scale and aspect-ratio variation, and same-envelope topology controls.

All four manifests completed through the local, credential-free corpus path with `--repair`. The default scaffold passed only the intended `box` baseline; the other 20 cases failed their primary geometry gates and then passed with their deterministic local reference replay. P2 was 9/9 replay pass and P3 was 5/5 replay pass. The registry audit found no missing fixture, reference script, or case card, and no SHA-256 mismatch.

## Decision

The evidence does not justify a runtime operation helper, new probe, new gate, project-level IR, CAD SDK, or CAD workplace. The primary failures are expected because the default scaffold is deliberately a fixed box, while every reference script reconstructs its own fixture and passes existing gates. This does not identify a repeated attributable OCP/API, parameter, or dependency-sequencing failure in the Harness.

The corpus remains self-authored and offline-reproducible. This review makes no hosted-model comparison or benchmark claim. Any hosted evaluation remains a separately authorized work item.
