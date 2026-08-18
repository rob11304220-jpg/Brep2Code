# Brep2Code Development Rules

Build the smallest tested vertical slice from B-Rep input to executable CAD
script and validated output.

1. Code, tests, case metadata, and run artifacts are the project authorities.
2. Keep permanent docs limited to README and the three files under `docs/`.
3. Do not add workpacks, handoffs, status ledgers, route maps, or evidence ledgers.
4. A case is self-contained; runtime paths are relative to its case directory.
5. Never expose eval references, repository files, secrets, or host paths to the runtime LLM.
6. The default provider is fake. A real provider requires an explicit CLI selection.
7. API keys come only from environment variables and must be redacted from artifacts.
8. Every provider run has request, round, timeout, and cost/token bounds.
9. Generated code runs only inside its revision workspace with bounded resources.
10. Add focused tests with behavior changes; run Ruff and the relevant tests before handoff.
11. Write an ADR only for a costly-to-reverse cross-module decision.

## Worktree and commit discipline

12. Use `D:\coderemote\Brep2Code_new` on branch `codex/v2-lean-rebuild` by
    default. At the start of a task, check the current directory, branch, dirty
    status, worktree ownership, and HEAD relationship once. If they match, do
    not switch branches or create another worktree.
13. Ignore unrelated detached worktrees. If the expected branch is owned by a
    different worktree, the current checkout is detached, or HEAD has an
    unexpected relationship to the branch, stop before editing and report it.
14. Preserve pre-existing changes as user work. Do not reset, overwrite, or
    include them in a commit; first determine whether they overlap the task.
15. Keep each commit to one smallest tested vertical slice: one behavior change,
    its focused tests, and any directly required schema, case metadata, or docs.
    Run Ruff and the relevant tests before treating the slice as committable.
16. Do not accumulate independently valid slices in one checkpoint. Commit only
    when requested; if the user explicitly requests staged commits for a task,
    commit each verified slice before beginning the next one.

## Secure execution on Windows

17. Treat `wsl.exe -d Ubuntu-24.04`, `uv run pytest --run-secure`, and provider
    or campaign runs that execute generated code as secure-backend commands.
18. Before a secure run, perform the read-only backend preflight. If the
    restricted command environment reports WSL service or distro access failure,
    proactively request external execution approval for the narrowly scoped
    project command instead of asking the user to repeat the diagnosis.
19. Keep the project sandbox boundary: never work around an unavailable WSL
    backend by running generated code through the trusted local executor.
20. If approval is unavailable or denied, stop the secure run, report the exact
    blocker, and provide the corresponding PowerShell command for manual execution.
