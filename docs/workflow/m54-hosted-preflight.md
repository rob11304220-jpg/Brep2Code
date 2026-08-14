# M54 Hosted Preflight — Stopped Before Authorization

- **Date**: 2026-08-08
- **Candidate**: `WP-M54-001-fixed-development-split-secure-llm-evaluation`
- **Provider/model (not authorized)**: DeepSeek `deepseek-v4-pro` at
  `https://api.deepseek.com`
- **Selected split**: all 12 rows of
  `case-library/manifests/self-authored/parametric-development.json`
- **Manifest SHA-256**:
  `DC4C6E8F3302367A3B1082FAD602FE36FF2A59901E59079695DA75724892A593`

## Input identity

| Case | SHA-256 |
|---|---|
| `param_additive_boss_low` | `EBED3D6F6CDFED1F2531E8FB9FDD1F7AF9B0E384433A7CB4A8115890E476D6F0` |
| `param_additive_boss_nominal` | `2860A07B9BC87C55E59A5308B8F223FF3AEDB3B0B0C12147C9637523A4802887` |
| `param_additive_boss_high` | `554472C62EA489FF7B3A467282A9739C9AFFBE77A8E68DBA00091CB9F661B143` |
| `param_through_hole_low` | `6239673BB3A2556FC7DB2FAA0FB35E384377E672E3980CD874C9C33A160B3109` |
| `param_through_hole_nominal` | `D8991A52FE0ABD5BDD120A062D211F3587F5C1ED9FFD453A80C28758BEF917DF` |
| `param_through_hole_high` | `4E3583150432ED09F1A276640EB4F236385D4866BF9C1935270DA393BD1D39AB` |
| `param_rounded_slot_low` | `F9FB195C2D805FB0DE57412E89B5348D4F59AECA5F6DB71195244A46992C825D` |
| `param_rounded_slot_nominal` | `290E59D06307DBF979666AB1A66F78D8A24C6EDF3289604FF2C5794D3143D228` |
| `param_rounded_slot_high` | `BF202C06586CD8BDDA9653A53A43A22F20A5EB1ED1C858F79A5F2F41AF06D959` |
| `param_fillet_low` | `B34BF66BB0B92F4BEFEF36197D8805D37EDBF0504C1380E000F5F9DD56F68902` |
| `param_fillet_nominal` | `F27981C1A0421DD43F21EE2CFCF68E73F3247FD04079D8A3C9FA059838AAE273` |
| `param_fillet_high` | `381A3961F21AF2E4376BE4EA56471D5CAD484A1642AE93ED28D266F651A403CC` |

## Checks

- The local configuration has non-secret entries for `DEEPSEEK_API_KEY`,
  `DEEPSEEK_MODEL`, and `DEEPSEEK_BASE_URL`; no value was displayed.
- WSL makes `/usr/bin/bwrap` and `/usr/bin/python3` available.
- Offline reference replay through `wsl-bwrap` completed at
  `data/m54-preflight/reference-repair-wsl-bwrap.json`: 12/12 repair passes
  and 12/12 reconstruction-eligible no-input provenance controls.
- The planned new hosted report path
  `data/corpus-runs/m54-parametric-development-deepseek-observation.json`
  does not exist.
- Proposed, but unauthorized, bound would be 12 cases × (one first pass + at
  most one repair) = 24 requests, with a 120-second per-request deadline.
  A batch may exceed an interactive command limit and would need durable
  monitoring.

## Stop condition

No authorization request may be made. The manifest has no fake first-pass
fixtures, so the matching offline first-pass preflight fails. More critically,
the existing multi-case `corpus --first-pass` egress is its older
filename-bearing `probe_summary`, whereas M54 requires the M48 path-free
observation transcript. No provider request was made. A separately selected
G2 multi-case observation-only adapter must close this gap before M54 resumes.
