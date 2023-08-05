import sys

import cbmcodecs

from d64 import DiskImage


fname = sys.argv[2].encode('petscii-c64en-uc')

with DiskImage(sys.argv[1], mode='w') as image:
    with image.path(fname).open('w', ftype='rel', record_len=220) as f:
        for n in range(0, 70):
            f.write(b'ONE')
            f.write(b'TWO')
            f.write(b'THREE')

with DiskImage(sys.argv[1]) as image:
    with image.path(fname).open() as f:
        count = 0
        while True:
            record = f.read_record()
            if not record:
                break
            print(count, record)
            count += 1
