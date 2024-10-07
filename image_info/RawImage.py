# RawImage class
import datetime
from pathlib import Path

from rawpy._rawpy import RawPy

from image_info.BaseImage import BaseImage


class RawImage(BaseImage):
    def __init__(self, reader: RawPy, file_path: Path):
        super().__init__(reader, file_path)
        self._type_hint_reader: RawPy = self._reader

    def _get_image_type(self):
        # TODO: Find a way to align with database restrictions
        return 'raw'

    def _get_image_mode(self):
        return 'RGB'  # Assuming RAW images are typically in RGB mode

    def _get_width(self):
        return self._type_hint_reader.sizes.width

    def _get_height(self):
        return self._type_hint_reader.sizes.height

    def _get_compression(self):
        return 'raw'  # RAW images are typically uncompressed

    def _get_quality(self) -> int:
        return 0  # Not really implemented for RAW

    def _get_resolution(self) -> ():
        return self._type_hint_reader.sizes.x_resolution, self._type_hint_reader.sizes.y_resolution

    def _get_recorded_date(self) -> datetime:
        # RAW images may not have EXIF data, so this is a placeholder
        return None
