# Runtime Guidance Cards

Use this runbook when a completed case-extension, replay diagnostic, or
attribution review may have reusable operational evidence.

1. Classify the result in the modeling knowledge system as a reusable
   operation/diagnosis, a counterexample, or no reusable evidence. Do not
   summarize an unreviewed hypothesis as a card.
2. Create a JSON card below `runtime_resources/experience-cards/cards/` and
   add it to `index.json`.  Keep the card concise; link to tracked reviews or
   contracts, never ignored logs, secrets, provider responses, workpacks, or
   handoffs.
3. State scope, evidence level, supporting cases, counterexamples, a bounded
   runtime action, and a review trigger.  Case-local observations remain
   `experimental`.
4. Run `uv run python tools/audit_runtime_guidance.py` and the focused test.
5. Keep cards absent by default. The completed M19-003 bridge may expose one
   explicit, hash-bound card to one revision; it is not a default mount,
   directory search, automatic prompt injection or provider authorization.
   A new card mechanism or broader retrieval needs a separate workpack and
   development-only evaluation under ADR-0016. Hosted work also needs its
   normal explicit authorization.
6. For the existing M19-003 opt-in bridge, bind one revision to explicit index/card
   hashes, one selected card path, and that bundle's declared compatible roles;
   retain only returned card IDs plus the index hash in the trace. Missing/invalid
   bundles fail closed; do not substitute a card or search a directory. The default
   revision retains no-card behavior.

The card corpus is a projection of reviewed modeling knowledge, and a
supplement to `signal_bundle.json`; it is not a replacement for execution,
artifact, probe, or gate facts.
