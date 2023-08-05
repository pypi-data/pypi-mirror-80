import sys

import cbmcodecs

from d64 import DiskImage, ProgramFile


with DiskImage(sys.argv[1]) as image:
    with image.path(sys.argv[2].encode('petscii-c64en-uc')).open() as f:
        p = ProgramFile(f)

for line in p.dump():
    print(line)
