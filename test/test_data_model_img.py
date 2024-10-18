"""
Test creation of data objects
"""
import os
from datetime import datetime
from pathlib import Path

import pytest

from image_info.BaseImage import BaseImage
from image_info.ImageInfoFactory import image_info_factory
# from image_info.ImageMetadata import ImageMetaData, ImageMetadataException
# from model.content.ImageFileInfos import ImageFileInfos
from ORMModel import ImageFileInfos


test_source_dir: Path = Path(os.getcwd(), 'sources/')


@pytest.mark.parametrize("source, expected", [
    (test_source_dir / 'I1FEMC010315_0011.tif', ImageFileInfos(
        image_type='TIFF',
        image_mode='I;16',
        width=6200,
        height=653,
        tiff_compression='tiff_lzw',
        quality='tiff_lzw',
        bps_x=600,
        bps_y=600,
        recorded_date=None)),
    (test_source_dir / 'I2PD181500001.tif', ImageFileInfos(
        image_type='TIFF',
        image_mode='1',
        width=2550,
        height=3300,
        tiff_compression='group4',
        quality='group4',
        bps_x=300,
        bps_y=300,
        recorded_date=None)),
    (test_source_dir / 'I2PD181500004.jpg', ImageFileInfos(
        image_type='JPEG',
        image_mode='RGB',
        width=2187,
        height=3033,
        tiff_compression='unknown',
        quality='unknown',
        bps_x=300,
        bps_y=300,
        recorded_date=None)
    ),
    (test_source_dir / 'I1EAP71250007.ARW', ImageFileInfos(
        image_type='raw',
        image_mode='RGB',
        width=7968,
        height=5320,
        tiff_compression='raw',
        quality='raw',
        bps_x=7968,
        bps_y= 5320,
        recorded_date=None)
     )
    ])


def test_data_model_image(source: Path, expected: ImageFileInfos):
    from model.storage.Files import Files
    from sqlalchemy.orm import relationship
    # Files.image_file_infos = relationship('ImageFileInfos', back_populates='files')
    # ImageFileInfos.files = relationship('Files', back_populates='image_file_infos')

    blarg = base_image_to_image_file_infos(image_info_factory(source))
    assert(expected == blarg)



# convert a BaseImage object into an ImageFileInfos object
def base_image_to_image_file_infos(base_image: BaseImage) -> ImageFileInfos:
    return ImageFileInfos(
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