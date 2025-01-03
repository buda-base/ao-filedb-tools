# coding: utf-8
from sqlalchemy import BINARY, Column, Enum, ForeignKey, Index, Integer, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class File(Base):
    __tablename__ = 'files'
    __table_args__ = (
        Index('files_index_1', 'digest', 'size', unique=True),
        {'schema': 'storage', 'comment': 'Table of all the (deduplicated) actual files handled by Archive Storage'}
    )

    id = Column(INTEGER, primary_key=True)
    digest = Column(BINARY(32), nullable=False, comment='the digest of the file')
    size = Column(BIGINT, nullable=False, comment='the size in bytes')
    pronom_number = Column(SMALLINT, comment='the PRONOM number or, if unavailable, null')
    persistent_id = Column(BINARY(32), nullable=False, unique=True, comment='The identifier is globally unique for the BDRC archive. By construction it is the sha256 or a random id in case of collision.')
    created_at = Column(TIMESTAMP, comment='the creation date of the file. Often unknown or unreliable, can be set to the earlier mtime exposed by the FS')
    validity = Column(Enum('seemingly_valid', 'fully_valid', 'cannot_read', 'partially_recoverable', 'not_set'), nullable=False, comment='the validity of the image')
    earliest_mdate = Column(TIMESTAMP, comment='the earliest modification date for the file (optional)')


class ImageFileInfo(Base):
    __tablename__ = 'image_file_infos'
    __table_args__ = {'comment': 'Table containing information about image files'}

    id = Column(INTEGER, primary_key=True)
    storage_file_id = Column(ForeignKey('storage.files.id'), index=True, comment='storage.files.id FK')
    image_type = Column(Enum('jpg', 'png', 'single_image_tiff', 'jp2', 'raw'), nullable=False)
    image_mode = Column(Enum('1', 'L', 'RGB', 'RGBA', 'CMYK', 'P', 'OTHER'), nullable=False)
    tiff_compression = Column(Enum('raw', 'tiff_ccitt', 'group3', 'group4', 'tiff_lzw', 'tiff_jpeg', 'jpeg', 'tiff_adobe_deflate', 'lzma', 'other'), comment='names are from PIL version 10')
    width = Column(SMALLINT, nullable=False, comment='width of the bitmap (not taking a potential exif rotation into account)')
    height = Column(SMALLINT, nullable=False, comment='height of the bitmap (not taking a potential exif rotation into account)')
    quality = Column(TINYINT, comment='relevant only for jpg, png and single_image_tiff encoded as jpg: quality of encoding. JPEG is represented between 0 and 100. For PNG this column encodes the compression between 0 and 9.')
    bps_x = Column(TINYINT, nullable=False, comment='bits per sample x')
    bps_y = Column(TINYINT, nullable=False, comment='bits per sample y')
    recorded_date = Column(TIMESTAMP, comment='the timestamp recorded in the exif metadata')
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    storage_file = relationship('File')


class PdfFileInfo(Base):
    __tablename__ = 'pdf_file_infos'

    id = Column(INTEGER, primary_key=True)
    storage_file = Column(ForeignKey('storage.files.id'), index=True, comment='storage.files.id FK')
    number_of_pages = Column(SMALLINT, comment='the number of pages')
    median_nb_chr_per_page = Column(SMALLINT, comment='the average number of characters in a page')
    median_nb_images_per_page = Column(SMALLINT, comment='the average number of images per page')
    recorded_date = Column(TIMESTAMP, comment='the timestamp recorded in the exif metadata')
    storage_file_id = Column(Integer, comment='storage.files.id FK')
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    file = relationship('File')
