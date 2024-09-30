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

# https://pypdf.readthedocs.io/en/latest/modules/PdfReader.html


from pypdf import PdfReader

PdfReaderType = Union[str, Path, IO[Any]]


class PdfMetaData():
    """
    initializer. Usage  PdfMetadata(file name string, pathlib.Path object, or file-like object (open _pdf_path)
    """

    def __init__(self, stream: PdfReaderType = None):
        self._pdf_path = stream
        self._pdf_object = None
        self._median_nb_chr_per_page = None
        self._median_nb_images_per_page = None

    @property
    def pdf_object(self) -> PdfReader:
        if not self._pdf_object and not self._pdf_path:
            raise ValueError('_pdf_path required to open pdf object. set self._pdf_path')
        if not self._pdf_object:
            self._pdf_object = PdfReader(self._pdf_path)
        return self._pdf_object

    @property
    def num_pages(self):
            return self.pdf_object.get_num_pages()

    @property
    def creation_date(self):
        return self.pdf_object.metadata.creation_date

    @property
    def modification_date(self):
        return self.pdf_object.metadata.modification_date
    
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
        char_counts = [len(page.extract_text()) for page in self.pdf_object.pages]
        return statistics.median(char_counts)

    def calc_median_nb_images_per_page(self):
        """
        Calculate the median number of images per page in the pdf
        """
        image_counts = [len(page.images) for page in self.pdf_object.pages]
        return statistics.median(image_counts)

    def refresh_medians(self):
        if not self._median_nb_chr_per_page:
            self._median_nb_chr_per_page = self.calc_median_nb_chars_per_page()

        if not self._median_nb_images_per_page:
            self._median_nb_images_per_page = self.calc_median_nb_images_per_page()
