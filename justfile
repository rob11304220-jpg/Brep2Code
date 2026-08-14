run record="demo":
    python -m brep2code.cli run --record {{record}}

probe input="tests\\fixtures\\brep\\smoke\\box.step":
    python -m brep2code.cli probe --input {{input}}

test:
    python -m pytest

lint:
    python -m ruff check .

check:
    python -m pytest
    python -m ruff check .
