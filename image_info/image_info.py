#!/usr/bin/env python3

from PIL import Image, ExifTags, UnidentifiedImageError
import os
from datetime import datetime
from pprint import pp

from .pdf_info import *


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


def extract_pdf_metadata(file_path):
    import pypdf
    reader = pypdf.PdfFileReader(file_path)

# Example usage
