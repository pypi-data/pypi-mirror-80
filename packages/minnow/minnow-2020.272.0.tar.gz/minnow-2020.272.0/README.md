# Minnow Python

Utilities for the Minnow file processing framework.

```python
import minnow
```

### Load a .properties file

This function will return the properties from a file as a dictionary.

```python
from pathlib import Path

props = load_properties(Path('path/to/file.properties'))
```

### Save to a .properties file

This function will save a dictionary as a .properties file.

```python
props = {'type': 'blueprints', 'orientation': 'above', 'size': 2}
save_properties(props, Path('path/to/file.properties')
```

### Finding files to process

This function will return pairs of data/metadata files in a directory as `DataMetaPair` instances.

```python
pairs_to_process = list_pairs_at_path(Path('path/to/input/directory')

for pair in pairs_to_process:
    data_path = pair.data_file
    properties_path = pair.metadata_file

    # read the properties if you need to
    properties_dict = load_properties(properties_path)

    # do some processing on each pair
```
