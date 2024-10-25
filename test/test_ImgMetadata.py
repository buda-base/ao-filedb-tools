import os
from datetime import datetime
from pathlib import Path

import pytest

from  image_info import *
# from image_info.ImageMetadata import ImageMetaData, ImageMetadataException


# from image_info.BaseImage import BaseImage
# from image_info.ImageInfoFactory import image_info_factory


# from image_info.PdfImage import PdfImage
# from image_info.PdfImage import PdfImage

test_source_dir: Path = Path(os.getcwd(), 'sources/')


@pytest.mark.parametrize("source, expected", [
    (test_source_dir / 'I1FEMC010315_0011.tif', {
        "image_type": 'TIFF',
        "image_mode": 'I;16',
        "width": 6200,
        "height": 653,
        "compression": 'tiff_lzw',
        "quality": 'tiff_lzw',
        "resolution": (600.0, 600.0),
        "recorded_date": None,
        "modified_date": datetime(2024, 9, 30, 0, 0)
    }),
    (test_source_dir / 'I2PD181500001.tif', {
        "image_type": 'TIFF',
        "image_mode": '1',
        "width": 2550,
        "height": 3300,
        "compression": 'group4',
        "quality": 'group4',
        "resolution": (300.0, 300.0),
        "recorded_date": None,
        "modified_date": datetime(2017, 11, 28, 0, 0)
    }),
    (test_source_dir / 'I2PD181500004.jpg', {
        "image_type": 'JPEG',
        "image_mode": 'RGB',
        "width": 2187,
        "height": 3033,
        "compression": 'unknown',
        "quality": 'unknown',
        "resolution": (300, 300),
        "recorded_date": None,
        "modified_date": datetime(2017, 11, 28, 0, 0)
    }),
    (test_source_dir / 'I1EAP71250007.ARW', {
        "image_type": 'raw',
        "image_mode": 'RGB',
        "width": 7968,
        "height": 5320,
        "compression": 'raw',
        "quality": 'raw',
        "resolution": (7968, 5320),
        "recorded_date": None,
        "modified_date": datetime(2024, 9, 30, 0, 0)
    })])
def test_image_metadata(source, expected):
    #    try:
    metadata: BaseImage = image_info_factory(source)

    assert metadata.image_type == expected['image_type']
    assert metadata.image_mode == expected['image_mode']
    assert metadata.width == expected['width']
    assert metadata.height == expected['height']
    assert metadata.compression == expected['compression']
    assert metadata.quality == expected['quality']
    assert metadata.resolution == expected['resolution']
    assert metadata.recorded_date == expected['recorded_date']
    # This is non-canonical assert metadata.modified_date == expected['modified_date']

    # DEBUG
    # from pprint import pp
    # pp(f"{metadata.image_path=}")
    # pp(f"{metadata.image_type=}")
    # pp(f"{metadata.image_mode=}")
    # pp(f"{metadata.width=}")
    # pp(f"{metadata.height=}")
    # pp(f"{metadata.compression=}")
    # pp(f"{metadata.quality=}")
    # pp(f"{metadata.resolution=}")
    # pp(f"{metadata.recorded_date=}")
    # pp(f"{metadata.modified_date=}")

#