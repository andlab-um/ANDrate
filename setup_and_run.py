"""Create a local virtual environment once, then start ANDrate."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import venv

def main():
    if sys.version_info < (3, 10):
        print("Please install Python 3.10 or newer. Python 3.12 is the tested version.")
        return 1
    root = Path(__file__).resolve().parent
    env = root / ".venv"
    python = env / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.exists():
        print("Creating the ANDrate environment...", flush=True)
        venv.EnvBuilder(with_pip=True).create(env)
    requirements = root / "requirements.txt"
    digest = hashlib.sha256(requirements.read_bytes()).hexdigest()
    marker = env / ".andrate-requirements"
    if not marker.exists() or marker.read_text() != digest:
        subprocess.run([str(python), "-m", "pip", "install", "-r", str(requirements)], check=True)
        marker.write_text(digest)
    subprocess.run([str(python), "-c", "import flask, requests"], check=True)
    return subprocess.call([str(python), str(root / "launch.py"), *sys.argv[1:]], cwd=root)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nANDrate stopped.")
        sys.exit(0)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"Setup failed: {exc}\nSee docs/Troubleshooting.md. Your data have not been deleted.", file=sys.stderr)
        sys.exit(1)
