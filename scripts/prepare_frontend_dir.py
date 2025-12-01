#!/usr/bin/env python3
from pathlib import Path
import shutil

TARGET = Path("meshchatx") / "public"

if TARGET.exists():
    shutil.rmtree(TARGET)

TARGET.mkdir(parents=True, exist_ok=True)

