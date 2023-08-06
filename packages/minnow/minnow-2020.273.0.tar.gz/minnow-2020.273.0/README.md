# Minnow Python

Utilities for the Minnow file processing framework.

```python
import minnow
```

## Create a processor

A processor can be created by subclassing `minnow.Processor` and overriding its `process` method, which must take a metadata file path, a data file path, and an output path.  The built-in `run` method will take care of finding files to process in the input directory.

```python
import sys

from pathlib import Path

import minnow

class MyProcessor(minnow.Processor):
    def process(metadata_file_path, data_file_path, output_path):
        metadata_dict = minnow.load_properties(metadata_file_path)
        data_file = data_file_path.open('rb')  # Use 'r' for text and 'rb' for binary

        # Do whatever work here

        # Write 0, 1, or many data/metadata pairs as output
        output_path.joinpath('mydata').write_bytes(my_output_data)
        minnow.save_properties(my_output_metadata_dict, output_path.joinpath('mydata.properties'))

def main():
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    my_processor = MyProcessor(input_path, output_path)  # Create an instance of your processor
    my_processor.run()

if __name__ == "__main__":
    main()
```

## Utilities

The `minnow.Processor` class is basically a wrapper for many of the utilities below.  If you need more manual control, these utilities can be used directly.

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
save_properties(props, Path('path/to/file.properties'))
```

### Finding files to process

This function will return pairs of data/metadata files in a directory as `DataMetaPair` instances.

```python
pairs_to_process = list_pairs_at_path(Path('path/to/input/directory'))

for pair in pairs_to_process:
    data_path = pair.data_path
    properties_path = pair.metadata_path

    # read the properties if you need to
    properties_dict = load_properties(properties_path)

    # do some processing on each pair
```
