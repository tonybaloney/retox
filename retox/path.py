# -*- coding: utf-8 -*-

# Provide pathlib.Path here, using backported pathlib2 if needed.
try:
    from pathlib import Path
    Path().expanduser()
except (ImportError, AttributeError):
    from pathlib2 import Path
