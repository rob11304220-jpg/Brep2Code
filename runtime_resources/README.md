# Runtime Resource Bundles

This directory is not mounted by default and is not development governance material. A caller must explicitly pass a selected bundle with `--runtime-resources`; the `wsl-bwrap` executor then makes it read-only at `/resources` for one revision.

Do not place secrets, `AGENTS.md`, workpacks, handoffs, ADRs, or broad repository copies in a runtime bundle.

`experience-cards/` is an experimental, static bundle of bounded operational
guidance. It is audited offline and remains absent by default. The completed
M19-003 bridge can expose one explicitly selected, hash-bound card to one
revision through `get_guidance_card`; it is not directory search, automatic
prompt injection, or broad runtime access. See its README and ADR-0016 before
any use.
