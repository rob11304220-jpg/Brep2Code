"""Download, verify, and safely unpack the official Fusion 360 r1.0.1 archive.

This development-only tool stores every raw artifact below ignored ``data/``.  It
does not select cases, create a manifest, invoke the Harness, or contact a model
provider.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import urllib.request
import zipfile
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath


ARCHIVE_URL = (
    "https://fusion-360-gallery-dataset.s3.us-west-2.amazonaws.com/"
    "reconstruction/r1.0.1/r1.0.1.zip"
)
ROOT = Path("data/datasets/fusion360_gallery/r1.0.1")
ARCHIVE = ROOT / "archives/r1.0.1.zip"
EXTRACTED = ROOT / "extracted"
CATALOG = ROOT / "cache-catalog.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def unsafe_member(info: zipfile.ZipInfo) -> str | None:
    member = PurePosixPath(info.filename)
    if not info.filename or member.is_absolute() or ".." in member.parts:
        return "path is empty, absolute, or escapes the extraction root"
    mode = info.external_attr >> 16
    if stat.S_IFMT(mode) == stat.S_IFLNK:
        return "symbolic links are not permitted"
    return None


def validate_archive(archive: Path) -> list[zipfile.ZipInfo]:
    with zipfile.ZipFile(archive) as bundle:
        bad = [(entry.filename, unsafe_member(entry)) for entry in bundle.infolist()]
        bad = [(name, reason) for name, reason in bad if reason]
        if bad:
            details = "; ".join(f"{name}: {reason}" for name, reason in bad[:5])
            raise ValueError(f"refusing unsafe ZIP member(s): {details}")
        failing = bundle.testzip()
        if failing:
            raise ValueError(f"ZIP CRC verification failed for {failing}")
        return bundle.infolist()


def download_archive(proxy: str | None) -> None:
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    partial = ARCHIVE.with_suffix(".zip.partial")
    offset = partial.stat().st_size if partial.exists() else 0
    request = urllib.request.Request(ARCHIVE_URL, headers={"Range": f"bytes={offset}-"})
    print(f"downloading {ARCHIVE_URL} from byte {offset}", flush=True)
    proxies = {"https": proxy} if proxy else {}
    opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxies))
    with opener.open(request, timeout=120) as response:
        if offset and response.status != 206:
            partial.unlink()
            return download_archive(proxy)
        with partial.open("ab" if offset else "wb") as output:
            shutil.copyfileobj(response, output, length=1024 * 1024)
    partial.replace(ARCHIVE)


def promote_verified_partial() -> bool:
    """Promote a fully received partial file after an interrupted final rename."""
    partial = ARCHIVE.with_suffix(".zip.partial")
    if not partial.exists():
        return False
    try:
        validate_archive(partial)
    except (OSError, ValueError, zipfile.BadZipFile):
        return False
    partial.replace(ARCHIVE)
    return True


def safe_extract(entries: list[zipfile.ZipInfo]) -> int:
    partial = ROOT / "extracted.partial"
    if partial.exists():
        shutil.rmtree(partial)
    partial.mkdir(parents=True)
    root = partial.resolve()
    files = 0
    try:
        with zipfile.ZipFile(ARCHIVE) as bundle:
            for entry in entries:
                target = (partial / PurePosixPath(entry.filename)).resolve()
                if os.path.commonpath((root, target)) != str(root):
                    raise ValueError(f"ZIP member escaped root during extraction: {entry.filename}")
                if entry.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                with bundle.open(entry) as source, target.open("xb") as output:
                    shutil.copyfileobj(source, output, length=1024 * 1024)
                files += 1
        if EXTRACTED.exists():
            shutil.rmtree(EXTRACTED)
        partial.replace(EXTRACTED)
        return files
    except BaseException:
        if partial.exists():
            shutil.rmtree(partial)
        raise


def write_catalog(entries: list[zipfile.ZipInfo], extracted_files: int) -> None:
    paths = sorted({entry.filename.split("/", 1)[0] for entry in entries if entry.filename})
    split_paths = [
        entry.filename
        for entry in entries
        if PurePosixPath(entry.filename).name.lower() in {"train_test.json", "train.json", "test.json"}
    ]
    catalog = {
        "schema_version": 1,
        "status": "completed",
        "dataset_id": "fusion360_gallery",
        "release": "r1.0.1",
        "official_url": ARCHIVE_URL,
        "downloaded_at_utc": datetime.now(UTC).isoformat(),
        "archive": {
            "path": ARCHIVE.as_posix(),
            "sha256": sha256(ARCHIVE),
            "bytes": ARCHIVE.stat().st_size,
            "zip_member_count": len(entries),
            "listed_uncompressed_bytes": sum(entry.file_size for entry in entries),
        },
        "extraction": {
            "root": EXTRACTED.as_posix(),
            "file_count": extracted_files,
            "top_level_paths": paths,
            "archive_crc_verified": True,
            "safe_member_validation": "passed",
        },
        "split_layout": {
            "detected_paths": split_paths,
            "note": "No samples have been selected or admitted.",
        },
    }
    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    temporary = CATALOG.with_suffix(".json.partial")
    temporary.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    temporary.replace(CATALOG)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="download the official archive if absent")
    parser.add_argument("--proxy", help="optional HTTP(S) proxy URL for the archive download")
    parser.add_argument(
        "--refresh-catalog",
        action="store_true",
        help="rewrite the catalog from an existing verified archive and extracted cache",
    )
    args = parser.parse_args()
    if not ARCHIVE.exists() and not promote_verified_partial():
        if not args.download:
            parser.error(f"archive is absent: {ARCHIVE}; rerun with --download")
        download_archive(args.proxy)
    entries = validate_archive(ARCHIVE)
    if args.refresh_catalog:
        if not EXTRACTED.is_dir():
            parser.error(f"extracted cache is absent: {EXTRACTED}")
        write_catalog(entries, sum(1 for path in EXTRACTED.rglob("*") if path.is_file()))
        print(f"refreshed: {CATALOG}")
        return 0
    extracted_files = safe_extract(entries)
    write_catalog(entries, extracted_files)
    print(f"completed: {CATALOG}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
