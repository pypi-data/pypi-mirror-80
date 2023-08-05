# d64

This Python module enables access to disk image files (.d64, .d71, .d81) used by various Commodore microcomputer emulators and tools.

It provides familiar interfaces for developers to read and write program and data files within an image.

In addition it contains tools useful to inspect and modify images, for example a script to check the integrity of an image.


## Examples

Classes and functions reside in the `d64` module, the whole module may be imported or just those definitions referenced by the user.

### Displaying an image contents

To perform a directory list

```python
import cbmcodecs
from d64 import DiskImage

with DiskImage('squadron.d64') as image:
    for line in image.directory('petscii-c64en-uc'):
        print(line)
```

This prints out

```
0 "SQUADRON        " Q9 2A
15   "SQUADRON PAL"     PRG
15   "SQUADRON NTSC"    PRG
634 BLOCKS FREE.
```

### Listing a BASIC program

To display a BASIC program as text

```python
import cbmcodecs
from d64 import DiskImage, ProgramFile

with DiskImage('test.d64') as image:
    with image.path('METEOR'.encode('petscii-c64en-uc')).open() as f:
        p = ProgramFile(f)

for line in p.list():
    print(line)
```


## TODO

- Detailed documentation
- interactive shell utility
- support for .d81 partitions and subdirectories
- support for .d81 relative files
- better docstrings
- more examples
- Selectable BASIC token sets
