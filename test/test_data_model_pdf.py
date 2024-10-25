import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

import pytest

from ORMModel import PdfFileInfos
import image_info as ii

test_source_dir: Path = Path(os.getcwd(), 'sources/')


@pytest.mark.parametrize("source, expected", [
    (test_source_dir / 'MultiPageCharTibetanMultiImage.pdf',
     PdfFileInfos(number_of_pages=3,
                  recorded_date=datetime(2024, 1, 31, 6, 23, 48),
                  median_nb_chr_per_page=1364,
                  median_nb_images_per_page=1)),
    (test_source_dir / 'MultiPageImage1.pdf',
     PdfFileInfos(number_of_pages=13,
                  recorded_date=datetime(2021, 7, 4, 11, 14, 25, tzinfo=timezone.utc),
                  median_nb_chr_per_page=0,
                  median_nb_images_per_page=1)),
    (test_source_dir / 'MultiPageCharMultiImage.pdf',
     PdfFileInfos(number_of_pages=16,
                  recorded_date=datetime(2016, 9, 30, 10, 50, 1, tzinfo=timezone(timedelta(days=-1, seconds=61200))),
                  median_nb_chr_per_page=1402.5,
                  median_nb_images_per_page=0)),
    (test_source_dir / 'Typical_BdrcPdf.pdf',
     PdfFileInfos(number_of_pages=5,
                  recorded_date=datetime(2024, 9, 29),
                  median_nb_chr_per_page=1395,
                  median_nb_images_per_page=0))
])

def test_pdf_metadata(source, expected):
    actual: PdfFileInfos = ii.base_image_to_pdf_file_infos(ii.image_info_factory(source))
    assert actual == expected

