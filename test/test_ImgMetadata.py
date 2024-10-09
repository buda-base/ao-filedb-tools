import os
from pathlib import Path

import pytest

# from image_info.ImageMetadata import ImageMetaData, ImageMetadataException
from image_info.BaseImage import BaseImage
from image_info.ImageInfoFactory import image_info_factory

# from image_info.PdfImage import PdfImage
# from image_info.PdfImage import PdfImage

test_source_dir: Path = Path(os.getcwd(), 'sources/')


@pytest.mark.parametrize("source, expected", [
    (test_source_dir / 'I1FEMC010315_0011.tif', {
        "image_type": "",
        "image_mode": "",
        "width": "",
        "height": "",
        "compression": "",
        "quality": "",
        "resolution": "",
        "recorded_date": "",
        "modified_date": ""
    }),
    (test_source_dir / 'I2PD181500001.tif', {
        "image_type": "",
        "image_mode": "",
        "width": "",
        "height": "",
        "compression": "",
        "quality": "",
        "resolution": "",
        "recorded_date": "",
        "modified_date": ""
    }),
    (test_source_dir / 'I2PD181500004.jpg', {
        "image_type": "",
        "image_mode": "",
        "width": "",
        "height": "",
        "compression": "",
        "quality": "",
        "resolution": "",
        "recorded_date": "",
        "modified_date": ""
    }),
    (test_source_dir / 'I1EAP71250007.ARW', {
        "image_type": "",
        "image_mode": "",
        "width": "",
        "height": "",
        "compression": "",
        "quality": "",
        "resolution": "",
        "recorded_date": "",
        "modified_date": ""
    })
])
def test_image_metadata(source, expected):
#    try:
    metadata: BaseImage = image_info_factory(source)
    # assert metadata.image_type == expected['image_type']
    # assert metadata.image_mode == expected['image_mode']
    # assert metadata.width == expected['width']
    # assert metadata.height == expected['height']
    # assert metadata.compression == expected['compression']
    # assert metadata.quality == expected['quality']
    # assert metadata.resolution == expected['resolution']
    # assert metadata.recorded_date == expected['recorded_date']
    # assert metadata.modified_date == expected['modified_date']

    from pprint import pp
    pp(f"{metadata.image_path=}")
    pp(f"{metadata.image_type=}")
    pp(f"{metadata.image_mode=}")
    pp(f"{metadata.width=}")
    pp(f"{metadata.height=}")
    pp(f"{metadata.compression=}")
    pp(f"{metadata.quality=}")
    pp(f"{metadata.resolution=}")
    pp(f"{metadata.recorded_date=}")
    pp(f"{metadata.modified_date=}")
