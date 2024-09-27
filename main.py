#!/usr/bin/env python3
from PIL import UnidentifiedImageError
from pprint import pp

from image_info.image_info import extract_image_metadata, extract_pdf_metadata
for fp in ( '/Users/jimk/Downloads/Storage 2024-Proposed-2 (1).png',  '/Users/jimk/dev/ao-filedb-tools/test/sources/W00EGS1016625-005.pdf'):
    try:
        metadata = extract_image_metadata(fp)
    except UnidentifiedImageError:
        metadata = extract_pdf_metadata(fp)
    pp(metadata)