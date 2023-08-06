# vim: expandtab tabstop=4 shiftwidth=4

from pathlib import Path
from typing import List

from .exceptions import MinnowPathException

class DataMetadataPair:
    def __init__(self, data_path: Path, metadata_path: Path) -> None:
        self.data_path = data_path
        self.metadata_path = metadata_path

def list_pairs_at_path(input_dir: Path) -> List[DataMetadataPair]:
    if not input_dir.exists():
        raise MinnowPathException('Cannot list_pairs_at_path. Path does not exist: {}'.format(input_dir))

    metadata_paths = list(input_dir.glob('*.properties'))
    data_paths = [Path(mp.with_suffix('')) for mp in metadata_paths]
    pairs = [DataMetadataPair(data_paths[i], metadata_paths[i]) for i in range(len(data_paths)) if data_paths[i].exists()]
    return pairs
