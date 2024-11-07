#!/usr/bin/env python3
import os
import statistics
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import Union, IO, Any

import rawpy
from PIL import ExifTags
from PIL import Image, UnidentifiedImageError
from pypdf import PdfReader
from rawpy._rawpy import LibRawFileUnsupportedError, RawPy

from ORMModel import PdfFileInfo, ImageFileInfo

__all__ = ['ImageMetadataException', 'PdfReaderType', 'BaseImage', 'PdfImage', 'PilImage', 'RawImage',
           'extract_image_metadata', 'image_info_factory', 'base_image_to_image_file_infos',
           'base_image_to_pdf_file_infos']


class ImageMetadataException(Exception):
    pass


PdfReaderType = Union[str, Path, IO[Any]]


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
        _md = datetime.fromtimestamp(os.path.getmtime(self.image_path))
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


class PdfImage(BaseImage):
    """

    """

    def __init__(self, reader: PdfReader, file_path: Path):
        """
        Class to analyze a pdf file.
        :param reader: Open pypdf.PdfReader
        :param file_path: Path to the object that's opened
        """
        super().__init__(reader, file_path)
        self._type_hint_reader: PdfReader = self._reader
        self._median_nb_chr_per_page = None
        self._median_nb_images_per_page = None

    @property
    def num_pages(self):
        return self._type_hint_reader.get_num_pages()

    @property
    def creation_date(self):
        return self._type_hint_reader.metadata.creation_date

    @property
    def modification_date(self):
        return self._type_hint_reader.metadata.modification_date

    @property
    def median_nb_chr_per_page(self):
        self.refresh_medians()
        return self._median_nb_chr_per_page

    @property
    def median_nb_images_per_page(self):
        self.refresh_medians()
        return self._median_nb_images_per_page

    def calc_median_nb_chars_per_page(self):
        """
        Calculate the median number of characters per page in the pdf
        """
        char_counts = [len(page.extract_text()) for page in self._type_hint_reader.pages]
        return statistics.median(char_counts)

    def calc_median_nb_images_per_page(self):
        """
        Calculate the median number of images per page in the pdf
        """
        image_counts = [len(page.images) for page in self._type_hint_reader.pages]
        return statistics.median(image_counts)

    def refresh_medians(self):
        if not self._median_nb_chr_per_page:
            self._median_nb_chr_per_page = self.calc_median_nb_chars_per_page()

        if not self._median_nb_images_per_page:
            self._median_nb_images_per_page = self.calc_median_nb_images_per_page()


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
        return self._type_hint_reader.sizes.width, self._type_hint_reader.sizes.height

    def _get_recorded_date(self) -> datetime:
        # RAW images may not have EXIF data, so this is a placeholder
        return None


def extract_image_metadata(file_path):
    metadata = {}

    # Open the image file
    with Image.open(file_path) as img:
        # Extract basic metadata
        metadata['image_type'] = img.format
        metadata['image_mode'] = img.mode
        metadata['width'], metadata['height'] = img.size

        # Extract compression type if available
        compression = img.info.get('compression', 'unknown')
        metadata['compression'] = compression

        # Extract quality if available (JPEG specific)
        quality = img.info.get('quality', 'unknown')
        metadata['quality'] = quality

        # Extract resolution
        metadata['resolution'] = img.info.get('dpi', 'unknown')

        # Extract EXIF data if available
        exif_data = img._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name == 'DateTimeOriginal':
                    metadata['recorded_date'] = value
                    break
        else:
            metadata['recorded_date'] = 'unknown'

    # Extract file modified date
    modified_time = os.path.getmtime(file_path)
    metadata['modified_date'] = datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')

    return metadata


# def extract_pdf_metadata(file_path) -> {}:
#     import pypdf
#     pdf_info = PdfMetaData(stream=file_path)
#     metadata = {
#         'num_pages': pdf_info.num_pages,
#         'creation_date': pdf_info.creation_date,
#         'modification_date': pdf_info.modification_date,
#         'median_nb_chr_per_page': pdf_info.median_nb_chr_per_page,
#         'median_nb_images_per_page': pdf_info.median_nb_images_per_page
#     }
#     return metadata


def image_info_factory(file_path: PathLike[str]) -> BaseImage:
    """
    Return a BaseImage subclass depending on the file
    :param file_path: Path to the file
    :return: BaseImage subclass
    """
    # return the first thing that opens:

    try:
        return PilImage(Image.open(file_path), Path(file_path))
    except UnidentifiedImageError:
        pass
    try:
        return RawImage(rawpy.imread(str(file_path)), Path(file_path))
    except LibRawFileUnsupportedError:
        pass

    try:
        return PdfImage(PdfReader(file_path), Path(file_path))
    except Exception as e:
        raise ValueError(f"ImageFile {file_path} not supported - error {e}")


# convert a BaseImage object into an ImageFileInfos object
def base_image_to_image_file_infos(base_image: BaseImage) -> ImageFileInfo:
    return ImageFileInfo(
        image_type=base_image.image_type,
        image_mode=base_image.image_mode,
        width=base_image.width,
        height=base_image.height,
        tiff_compression=base_image.compression,
        quality=base_image.quality,
        bps_x=base_image.resolution[0],
        bps_y=base_image.resolution[1],
        recorded_date=base_image.recorded_date
    )


def base_image_to_pdf_file_infos(actual_pdf: PdfImage) -> PdfFileInfo:
    return PdfFileInfo(
        number_of_pages=actual_pdf.num_pages,
        median_nb_chr_per_page=actual_pdf.median_nb_chr_per_page,
        median_nb_images_per_page=actual_pdf.median_nb_images_per_page,
        recorded_date=actual_pdf.creation_date
    )
