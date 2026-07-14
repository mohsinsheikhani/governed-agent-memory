"""Put the repo root on sys.path so entrypoints in scripts/ can import `auth` and `src`.

Imported purely for its side effect. Put `import _paths` at the top of a script in this
directory, before any `auth` or `src` import. It resolves because a script run as
`uv run scripts/foo.py` has scripts/ on the path first, and this module then adds the
repo root above it.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
