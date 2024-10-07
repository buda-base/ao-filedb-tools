"""
return a BaseImage subclass depending on the file
"""

from PIL import Image, UnidentifiedImageError
import rawpy

from pathlib import Path
from os import PathLike

from rawpy._rawpy import LibRawFileUnsupportedError

from image_info.BaseImage import BaseImage
from image_info.PilImage import PilImage
from image_info.RawImage import RawImage
from image_info.PdfImage import PdfImage


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
        return RawImage(rawpy.imread(file_path), Path(file_path))
    except LibRawFileUnsupportedError:
        return PdfImage(file_path, Path(file_path))
    except Exception as e:
        raise ValueError(f"File {file_path} not supported - error {e}")
