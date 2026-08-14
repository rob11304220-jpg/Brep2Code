"""Templates for LLM-authored runtime files."""

DEFAULT_BUILD_SEQUENCE = '''\
"""Default M2 build script.

This smoke build uses the current OpenCascade backend to write a valid STEP
artifact. It is intentionally simple; LLM-authored scripts will replace it in
later repair loops.
"""

from pathlib import Path


def build(ctx=None):
    workspace = Path.cwd()
    output_dir = workspace / "output"
    intermediates_dir = workspace / "intermediates"
    output_dir.mkdir(parents=True, exist_ok=True)
    intermediates_dir.mkdir(parents=True, exist_ok=True)

    model_path = output_dir / "model.step"
    from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
    from OCP.IFSelect import IFSelect_RetDone
    from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer

    shape = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()
    writer = STEPControl_Writer()
    writer.Transfer(shape, STEPControl_AsIs)
    status = writer.Write(str(model_path))
    if status != IFSelect_RetDone:
        raise RuntimeError(f"failed to write STEP artifact: {status}")

    (intermediates_dir / "notes.txt").write_text(
        "M2 smoke build completed. Replace this script with reconstruction logic.\\n",
        encoding="utf-8",
    )
    print(f"Wrote {model_path.relative_to(workspace)}")
    return {"model": str(model_path)}


if __name__ == "__main__":
    build()
'''
