"""
Class to extract image metadata.

See 

`Requirements and Design <https://github.com/buda-base/ao-filedb-tools/issues/1>`__ 
"""
import os
from datetime import datetime
from pathlib import Path
from typing import Union, Any, IO
from PIL import Image, ExifTags

ImageReaderType = Union[str, Path, IO[Any]]


class ImageMetaData():
    def __init__(self, stream: ImageReaderType = None):
        self._image_path = stream
        self._image_object = None
        self.image_type = None
        self.image_mode = None
        self.width = None
        self.height = None
        self.compression = None
        self.quality = None
        self.resolution = None
        self.recorded_date = None
        self.modified_date = None

    @property
    def image_path(self) -> str:
        return str(self._image_path)


    @property
    def image_object(self) -> Image:
        if not self._image_object and not self._image_path:
            raise ValueError('_image_path required to open Image object. set self._image_path')
        if not self._image_object:
            self._image_object: Image = Image.open(self._image_path)

        self.populate_metadata(self._image_object)
        return self._image_object


def populate_metadata(self, image_object: Image):
    # Open the image file
    # Extract basic metadata
    self.image_type = image_object.format
    self.image_type = image_object.mode
    self.width, self.height = image_object.size

    # Extract compression type if available
    self.compression = image_object.info.get('compression', 'unknown')

    # Extract quality if available (JPEG specific)
    self.quality = image_object.info.get('quality', 'unknown')
    # Extract resolution
    self.resolution = image_object.info.get('dpi', 'unknown')

    # Extract EXIF data if available
    exif_data = image_object._getexif()
    if exif_data:
        for tag, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag, tag)
            if tag_name == 'DateTimeOriginal':
                self.recorded_date = value
                break
    else:
        self.recorded_date = 'unknown'

    # Extract file modified date
    _md = datetime.fromtimestamp(os.path.getmtime(self._image_path))
    self.modified_date = datetime(_md.year, _md.month, _md.day)
