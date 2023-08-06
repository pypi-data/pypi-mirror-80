from pathlib import Path

# Filesystem
ROOT = Path(__file__).absolute().parent
RESC = ROOT / "resc"
assert RESC.exists()
ELKI_FILEPATH = RESC / "elki.jar"
ELKI_URL = "https://elki-project.github.io/releases/release0.7.5/elki-bundle-0.7.5.jar"
