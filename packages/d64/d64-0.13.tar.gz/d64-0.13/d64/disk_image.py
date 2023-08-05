import shutil
import tempfile

from pathlib import Path

from .d64_image import D64Image
from .d71_image import D71Image
from .d81_image import D81Image


class DiskImage(object):
    raw_modes = {'r': 'rb', 'w': 'r+b'}

    def __init__(self, filepath, mode='r'):
        self.filepath = Path(filepath) if isinstance(filepath, str) else filepath
        self.mode = self.raw_modes.get(mode, 'rb')

    def __enter__(self):
        if self.mode == 'r+b':
            self.org_filepath = self.filepath
            tempf = tempfile.NamedTemporaryFile(prefix='d64-', dir=self.filepath.parent,
                                                delete=False)
            # copy existing file to temporary
            with self.org_filepath.open('rb') as inh:
                shutil.copyfileobj(inh, tempf)
            tempf.close()
            self.filepath = Path(tempf.name)

        for cls in (D64Image, D71Image, D81Image):
            if cls.valid_image(self.filepath):
                self.image = cls(self.filepath)
                self.image.open(self.mode)
                return self.image

        raise NotImplementedError("Unsupported image format")

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.image.close()

        if self.mode == 'r+b':
            if exc_type is None:
                # update original with modified file
                self.filepath.replace(self.org_filepath)
            else:
                self.filepath.unlink()
