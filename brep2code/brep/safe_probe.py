"""Bounded process-isolated B-Rep summary probing."""

from __future__ import annotations

import multiprocessing as mp
from pathlib import Path
from queue import Empty
from typing import Callable

from brep2code.brep.probes import ProbeError, load_model, probe_summary


INPUT_PROBE_TIMEOUT_SECONDS = 45
OUTPUT_PROBE_TIMEOUT_SECONDS = 15


def safe_probe_summary(
    path: Path,
    trace_dir: Path | None = None,
    *,
    timeout_seconds: int = OUTPUT_PROBE_TIMEOUT_SECONDS,
    worker: Callable | None = None,
) -> dict:
    """Return a structured B-Rep summary without letting a probe block its caller."""

    context = mp.get_context("spawn")
    result_queue = context.Queue()
    process = context.Process(
        target=worker or _probe_summary_worker,
        args=(str(path), str(trace_dir) if trace_dir is not None else None, result_queue),
    )
    process.start()
    process.join(timeout_seconds)
    if process.is_alive():
        process.terminate()
        process.join()
        return {
            "ok": False,
            "input": str(path),
            "error": {
                "code": "probe_timeout",
                "message": f"B-Rep summary probe exceeded {timeout_seconds} seconds and was terminated.",
            },
        }
    try:
        return result_queue.get_nowait()
    except Empty:
        return {
            "ok": False,
            "input": str(path),
            "error": {"code": "probe_worker_failed", "message": "B-Rep summary probe worker returned no result."},
        }


def _probe_summary_worker(path_value: str, trace_value: str | None, result_queue) -> None:
    try:
        path = Path(path_value)
        trace_dir = Path(trace_value) if trace_value is not None else None
        summary = probe_summary(load_model(path), trace_dir=trace_dir, limit_bytes=12_000)
        result_queue.put({"ok": True, **summary})
    except ProbeError as exc:
        result_queue.put(
            {"ok": False, "input": path_value, "error": {"code": exc.code, "message": exc.message}}
        )
