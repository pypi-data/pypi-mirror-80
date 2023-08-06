# vim: expandtab tabstop=4 shiftwidth=4

from pathlib import Path
from typing import Dict

class MinnowPropertiesException(Exception):
    pass

def has_reserved_characters(s: str) -> bool:
    if '=' in s: return True
    if '\n' in s: return True
    return False

def load_properties(path: Path) -> Dict[str, str]:
    with path.open('r') as f:
        lines = f.read().split('\n')

    pairs = [line.split('=') for line in lines]
    valid_pairs = [pair for pair in pairs if len(pair) == 2]
    return {k.strip(): v.strip() for k, v in valid_pairs}

def save_properties(properties: Dict, path:Path) -> None:
    pairs = [(str(k).strip(), str(v).strip()) for k, v in properties.items()]

    for k, v in pairs:
        if has_reserved_characters(k):
            raise MinnowPropertiesException('"{}" is not a valid property key: contains reserved characters'.format(k))

        if has_reserved_characters(v):
            raise MinnowPropertiesException('"{}" is not a valid property value: contains reserved characters'.format(k))

    lines = ['{k} = {v}'.format(k=k, v=v) for k, v in pairs]
    data = '\n'.join(lines)

    with path.open('w') as f:
        f.write(data)
