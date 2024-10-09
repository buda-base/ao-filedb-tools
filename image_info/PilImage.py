# PILImage class
import os
from datetime import datetime
from pathlib import Path

from PIL import Image, ExifTags

from image_info.BaseImage import BaseImage


class PilImage(BaseImage):
    def __init__(self, reader: Image.Image, file_path: Path):
        """
        Initialize with open PIL Image
        """
        super().__init__(reader, file_path)
        # Just helps with resolving type hints
        self._type_hint_reader: Image.Image = self._reader

    def _get_image_type(self) -> str:
        return self._type_hint_reader.format

    def _get_image_mode(self) -> str:
        return self._type_hint_reader.mode

    def _get_width(self) -> int:
        return self._type_hint_reader.size[0]

    def _get_height(self) -> int:
        return self._type_hint_reader.size[1]

    def _get_compression(self):
        return self._type_hint_reader.info.get('compression', 'unknown')

    def _get_quality(self):
        # ? type
        return self._type_hint_reader.info.get('quality', 0)

    def _get_resolution(self) -> int:
        # ? type?
        return self._type_hint_reader.info.get('dpi', 0)

    def _get_recorded_date(self) -> datetime:
        exif_data = self._type_hint_reader.getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name == 'DateTimeOriginal':
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        return None

    def _get_modified_date(self) -> datetime:
        modified_time = os.path.getmtime(self.file_path)
        return datetime.fromtimestamp(modified_time)
