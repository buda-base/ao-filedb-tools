"""
Test creation of data objects
"""
import os
from pathlib import Path
import pytest

import image_info as ii
from ORMModel import *

# from image_info.ImageInfoFactory import image_info_factory
# # from image_info.ImageMetadata import ImageMetaData, ImageMetadataException
# # from model.content.ImageFileInfos import ImageFileInfos
# from ORMModel import ImageFileInfos

# Bumstinator - in vscode, you have to set the cwd to be the project, so it finds library files.
# Means the source dir has to be the project root.  
# get the directory of the current python file  
test_source_dir: Path = Path(os.path.dirname(os.path.abspath(__file__)), 'sources/')
# test_source_dir: Path = Path(os.getcwd(), 'sources/')


@pytest.mark.parametrize("source, expected", [
    (test_source_dir / 'I1FEMC010315_0011.tif', ImageFileInfo(
        image_type='TIFF',
        image_mode='I;16',
        width=6200,
        height=653,
        tiff_compression='tiff_lzw',
        quality='tiff_lzw',
        bps_x=600,
        bps_y=600,
        recorded_date=None)),
    (test_source_dir / 'I2PD181500001.tif', ImageFileInfo(
        image_type='TIFF',
        image_mode='1',
        width=2550,
        height=3300,
        tiff_compression='group4',
        quality='group4',
        bps_x=300,
        bps_y=300,
        recorded_date=None)),
    (test_source_dir / 'I2PD181500004.jpg', ImageFileInfo(
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
    (test_source_dir / 'I1EAP71250007.ARW', ImageFileInfo(
        image_type='raw',
        image_mode='RGB',
        width=7968,
        height=5320,
        tiff_compression='raw',
        quality='raw',
        bps_x=7968,
        bps_y=5320,
        recorded_date=None)
     )
])
def test_data_model_image(source: Path, expected: ImageFileInfo):
    actual = ii.base_image_to_image_file_infos(ii.image_info_factory(source))
    assert (expected == actual)
