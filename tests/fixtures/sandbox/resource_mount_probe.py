"""Manual M5 probe: an explicitly selected resource bundle is readable at /resources."""

from pathlib import Path


resource = Path("/resources/example.txt")
print(f"resource_readable={resource.is_file()}; value={resource.read_text(encoding='utf-8') if resource.is_file() else ''}")
if not resource.is_file():
    raise RuntimeError("sandbox resource mount is unavailable")
