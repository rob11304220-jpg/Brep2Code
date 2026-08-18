from __future__ import annotations

from typing import Final


CAPABILITY_LEVELS: Final = tuple(f"L{index}" for index in range(7))
CAPABILITY_LEVEL_SET: Final = frozenset(CAPABILITY_LEVELS)
COMPATIBILITY_TIERS: Final = ("T0", "T1", "T2")
COMPATIBILITY_TIER_SET: Final = frozenset(COMPATIBILITY_TIERS)


def validate_capability_level(value: object, label: str = "capability_level") -> str:
    if not isinstance(value, str) or value not in CAPABILITY_LEVEL_SET:
        raise ValueError(f"{label} must be one of {list(CAPABILITY_LEVELS)}")
    return value


def validate_compatibility_tier(value: object, label: str = "compatibility_tier") -> str:
    if not isinstance(value, str) or value not in COMPATIBILITY_TIER_SET:
        raise ValueError(f"{label} must be one of {list(COMPATIBILITY_TIERS)}")
    return value
