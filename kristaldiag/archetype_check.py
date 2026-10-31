"""Read-only bridge to the independent Arketype structural observer."""
from __future__ import annotations
import importlib.util
from pathlib import Path


def observer(arketype_root=None):
    root = Path(arketype_root).expanduser().resolve() if arketype_root else Path(__file__).resolve().parents[2] / 'Arketype'
    file = root / 'arketype' / 'structural_observer.py'
    if not file.is_file():
        raise FileNotFoundError(f'Module Arketype absent : {file}')
    spec = importlib.util.spec_from_file_location('_kristal_arketype_structural_observer', file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, root


def inspect(target, arketype_root=None, all_projects=False):
    mod, root = observer(arketype_root)
    return mod.inspect_many(target, root) if all_projects else mod.inspect(target, root)
