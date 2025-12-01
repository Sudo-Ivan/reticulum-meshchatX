import shutil
from pathlib import Path

TARGET = Path("meshchatx") / "public"

if not Path("pyproject.toml").exists():
    raise RuntimeError("Must run from project root")

if TARGET.exists():
    if TARGET.is_symlink():
        raise RuntimeError(f"{TARGET} is a symlink, refusing to remove")
    shutil.rmtree(TARGET)

TARGET.mkdir(parents=True, exist_ok=True)
