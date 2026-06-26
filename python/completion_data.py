import json
import inspect
import sys

try:
    import gcoordinator as gc
except ImportError:
    gc = None

try:
    import numpy as np
except ImportError:
    np = None


def extract_items(obj, depth=0):
    items = []
    for name in dir(obj):
        if name.startswith('_'):
            continue
        try:
            member = getattr(obj, name)
        except Exception:
            continue
        if inspect.isclass(member):
            kind = 'class'
        elif callable(member):
            kind = 'function'
        else:
            kind = 'value'

        sig = None
        doc = None
        try:
            sig = str(inspect.signature(member))
        except Exception:
            pass
        try:
            raw = inspect.getdoc(member) or ''
            doc = raw[:400]
        except Exception:
            pass

        entry = {'name': name, 'kind': kind, 'signature': sig, 'doc': doc}

        # Recurse one level into classes to expose static/class methods
        if inspect.isclass(member) and depth == 0:
            entry['members'] = extract_items(member, depth=1)

        items.append(entry)
    return items


result = {}

if gc is not None:
    result['gc'] = extract_items(gc)

if np is not None:
    # Only include callables (functions/classes); skip constants and dtype aliases
    result['np'] = [
        item for item in extract_items(np)
        if item['kind'] in ('function', 'class')
    ]

json.dump(result, sys.stdout)
