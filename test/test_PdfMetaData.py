from datetime import timezone, timedelta

import pytest

from pathlib import Path
import os
from datetime import datetime

from image_info import *

test_source_dir: Path = Path(os.getcwd(), 'sources/')


@pytest.mark.parametrize("source, expected", [
    (test_source_dir / 'MultiPageCharTibetanMultiImage.pdf',
     {'num_pages': 3, 'creation_date': datetime(2024, 1, 31, 6, 23, 48),
      'modification_date': datetime(2024, 1, 31, 6, 23, 48), 'median_nb_chr_per_page': 1364,
      'median_nb_images_per_page': 1}),
    (test_source_dir / 'MultiPageImage1.pdf',
     {'num_pages': 13, 'creation_date': datetime(2021, 7, 4, 11, 14, 25, tzinfo=timezone.utc),
      'modification_date': datetime(2021, 8, 17, 10, 1, 43,
                                             tzinfo=timezone(timedelta(days=-1, seconds=61200))),
      'median_nb_chr_per_page': 0, 'median_nb_images_per_page': 1}),
    (test_source_dir / 'MultiPageCharMultiImage.pdf',
     {'num_pages': 16,
      'creation_date':  datetime(2016, 9, 30, 10, 50, 1, tzinfo=timezone(timedelta(days=-1, seconds=61200))),
      'modification_date': datetime(2016, 9, 30, 10, 52, 24, tzinfo=timezone(timedelta(days=-1, seconds=61200))),
      'median_nb_chr_per_page': 1402.5, 'median_nb_images_per_page': 0}),
    (test_source_dir / 'Typical_BdrcPdf.pdf',
     {'num_pages': 5,
      'creation_date':  datetime(2024, 9, 29),
      'modification_date':  datetime(2024, 9, 30),
      'median_nb_chr_per_page': 1395, 'median_nb_images_per_page': 0})
])
def test_pdf_metadata(source, expected):
    metadata: PdfImage = image_info_factory(source)
    # pp(f"{metadata.num_pages=}")
    # pp(f"{metadata.creation_date=}")
    # pp(f"{metadata.modification_date=}")
    # pp(f"{metadata.median_nb_chr_per_page=}")
    # pp(f"{metadata.median_nb_images_per_page=}")
    assert metadata.num_pages == expected['num_pages']
    assert metadata.creation_date == expected['creation_date']
    assert metadata.modification_date == expected['modification_date']
    assert metadata.median_nb_chr_per_page == expected['median_nb_chr_per_page']
    assert metadata.median_nb_images_per_page == expected['median_nb_images_per_page']
