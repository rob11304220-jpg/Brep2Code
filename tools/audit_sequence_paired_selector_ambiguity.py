"""Run the family-specific M29 selector-ambiguity audit."""

from build_m29_selector_ambiguity_candidates import audit


if __name__ == "__main__":
    print(f"selector-ambiguity audit passed: {len(audit())} records")
