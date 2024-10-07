"""
Wrapper for pypdf PdfReader.
dfn:

`PdfReader <https://pypdf.readthedocs.io/en/latest/modules/PdfReader.html>`__

Some of the attributes in

`Requirements and Design <https://github.com/buda-base/ao-filedb-tools/issues/1>`__ are calculated.
"""
import statistics
# copied from pypdf._utils. Don't want to depend on privates
from pathlib import Path
from typing import Union, Any, IO

from pypdf import PdfReader

from image_info.BaseImage import BaseImage

# https://pypdf.readthedocs.io/en/latest/modules/PdfReader.html

PdfReaderType = Union[str, Path, IO[Any]]


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
