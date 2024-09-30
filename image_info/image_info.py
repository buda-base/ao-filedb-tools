#!/usr/bin/env python3

from PIL import Image, ExifTags, UnidentifiedImageError
import os
from datetime import datetime

from image_info.PdfMetaData import PdfMetaData


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


def extract_pdf_metadata(file_path) -> {}:
    import pypdf
    pdf_info = PdfMetaData(stream=file_path)
    metadata = {
        'num_pages': pdf_info.num_pages,
        'creation_date': pdf_info.creation_date,
        'modification_date': pdf_info.modification_date,
        'median_nb_chr_per_page': pdf_info.median_nb_chr_per_page,
        'median_nb_images_per_page': pdf_info.median_nb_images_per_page
    }
    return metadata

# Example usage
