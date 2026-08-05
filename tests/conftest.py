import sys
import os
from pathlib import Path

import pytest

# Run Qt headlessly (no real display needed) — must be set before any
# PySide6/Qt import happens anywhere in the test session.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# QWebEngineView's sandboxed renderer process often can't start inside
# containers/CI (no real display, restricted namespaces) and will hang on
# creation instead of failing loudly. Disabling it is standard practice for
# testing, not something to carry into the shipped app.
os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")

# Only needed if pdf_reader isn't installed (editable or otherwise) and
# resolvable on sys.path already — delete this block if `import pdf_reader`
# already works without it.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
