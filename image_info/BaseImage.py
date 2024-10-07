# BaseImage class
from datetime import datetime
from pathlib import Path


class BaseImage:
    def __init__(self, reader: object, file_path: Path):
        self.file_path = file_path
        self._reader = reader

    @property
    def image_path(self) -> Path:
        return str(self.file_path)

    @property
    def image_reader_object(self) -> object:
        return self._reader
    @property
    def image_type(self) -> str:
        return self._get_image_type()

    @property
    def image_mode(self) -> str:
        return self._get_image_mode()

    @property
    def width(self) -> int:
        return self._get_width()

    @property
    def height(self) -> int:
        return self._get_height()

    @property
    def compression(self) -> str:
        return self._get_compression()

    @property
    def quality(self) -> str:
        return self._get_compression()

    @property
    def resolution(self) -> ():
        """
        Tuple?
        :return:
        """
        return self._get_resolution()

    @property
    def recorded_date(self) -> datetime:
        return self._get_recorded_date()

    @property
    def modified_date(self) -> datetime:
        import os
        _md = datetime.fromtimestamp(os.path.getmtime(self._image_path))
        return datetime(_md.year, _md.month, _md.day)


    def _get_object(self):
        raise NotImplementedError

    def _get_image_type(self):
        """image_file_infos.image_type"""
        raise NotImplementedError

    def _get_image_mode(self):
        """image_file_infos.image_mode"""
        raise NotImplementedError

    def _get_width(self):
        """image_file_infos.width"""
        raise NotImplementedError

    def _get_height(self):
        """image_file_infos.height"""
        raise NotImplementedError

    def _get_compression(self):
        """image_file_infos.tiff_compression"""
        raise NotImplementedError

    def _get_quality(self):
        """image_file_infos.quality"""
        raise NotImplementedError

    def _get_resolution(self):
        """image_file_infos.bps"""
        raise NotImplementedError

    def _get_recorded_date(self) -> datetime:
        """image_file_infos.recorded_date"""
        raise NotImplementedError
