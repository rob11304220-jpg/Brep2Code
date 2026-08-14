from pathlib import Path
import subprocess
import sys

Path("/input/model.step").read_bytes()
subprocess.run([sys.executable, "-c", "from pathlib import Path; Path('/input/model.step').read_bytes()"], check=True)
