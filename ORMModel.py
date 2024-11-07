# coding: utf-8
from sqlalchemy import BINARY, Column, Enum, ForeignKey, Index, Integer, TIMESTAMP, text, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

__all__ = ['ImageFile', 'ArchiveObject', 'ImagePath', 'Root', 'PdfFileInfo', 'ImageFileInfo']
Base = declarative_base()
metadata = Base.metadata

def eq_if(a, b):
    """
    Returns true if both a and b are None or if a == b
    :param a:
    :param b:
    :return:
    """
    return (a is None and b is None) or (a == b)

class ImageFileInfo(Base):
    __tablename__ = 'image_file_infos'
    __table_args__ = {'schema':'content','comment': 'Table containing information about image files'}

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

    # Must have same name as PdfFileInfo
    file = relationship('ImageFile')

    def __eq__(self, other):
        return (
                eq_if(self.image_type , other.image_type)
                and eq_if( self.image_mode , other.image_mode)
                and eq_if( self.width , other.width)
                and eq_if( self.height , other.height)
                and eq_if( self.bps_x , other.bps_x)
                and eq_if( self.bps_y , other.bps_y)
                and eq_if( self.storage_file_id , other.storage_file_id)
                and eq_if( self.tiff_compression , other.tiff_compression)
                and eq_if( self.quality , other.quality)
                and eq_if( self.recorded_date , other.recorded_date)
        )

class PdfFileInfo(Base):
    __tablename__ = 'pdf_file_infos'
    __table_args__ = {'schema':'content'}

    id = Column(INTEGER, primary_key=True)
    storage_file = Column(ForeignKey('storage.files.id'), index=True, comment='storage.files.id FK')
    number_of_pages = Column(SMALLINT, comment='the number of pages')
    median_nb_chr_per_page = Column(SMALLINT, comment='the average number of characters in a page')
    median_nb_images_per_page = Column(SMALLINT, comment='the average number of images per page')
    recorded_date = Column(TIMESTAMP, comment='the timestamp recorded in the exif metadata')
    storage_file_id = Column(Integer, comment='storage.files.id FK')
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # Must have same name as ImageFileInfo
    file = relationship('ImageFile')

    def __eq__(self, other):
        return (
                eq_if(self.number_of_pages , other.number_of_pages)
                and eq_if( self.median_nb_chr_per_page , other.median_nb_chr_per_page)
                and eq_if( self.median_nb_images_per_page , other.median_nb_images_per_page)
                and eq_if( self.recorded_date , other.recorded_date)
                and eq_if( self.storage_file_id , other.storage_file_id ))


class ImageFile(Base):
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

    def __eq__(self, other):
        return (
                self.digest , other.digest
                and eq_if( self.size , other.size)
                and eq_if( self.persistent_id , other.persistent_id)
                and eq_if( self.validity , other.validity)
                and eq_if( self.pronom_number , other.pronom_number)
                and eq_if( self.created_at , other.created_at)
                and eq_if( self.earliest_mdate , other.earliest_mdate ))
    # paths: Mapped[List['Paths']] = relationship('Paths', uselist=True, back_populates='files')
    # image_file_infos: Mapped[List['ImageFileInfos']] = relationship('ImageFileInfos', back_populates='files')
    # Try to test - see test_data_model_image

class Root(Base):
    __tablename__ = 'roots'
    __table_args__ = {'schema': 'storage','comment': 'Storage roots (ex: Archive 1)'}

    id = Column(INTEGER, primary_key=True, comment='internal identifier of the root object')
    name = Column(VARCHAR(32), nullable=False, comment='name of the Storage root (in ASCII), used to fint it on disk (ex: Archive0). The actual disk path depends on the mount points on the servers.')
    layout = Column(VARCHAR(50), nullable=False, comment='name of the storage layout, ASCII')

    def __eq__(self, other):
        return  ( self.name , other.name
                  and eq_if( self.layout , other.layout ))


class ArchiveObject(Base):
    __tablename__ = 'objects'
    __table_args__ = (
        Index('objects_index_0', 'bdrc_id', 'root', unique=True),
        {'schema': 'storage','comment': 'Objects kept on archive storage'}
    )

    id = Column(INTEGER, primary_key=True, comment='internal identifier')
    bdrc_id = Column(String(32), nullable=False, comment='the BDRC RID (ex: W22084), unique persistent identifier, ASCII string no longer than 32 characters')
    created_at = Column(TIMESTAMP, comment='the timestamp of the creation of the object, or the equivalent object in a previous archive storage')
    last_modified_at = Column(TIMESTAMP, comment='the timestamp of the last known modification')
    root = Column(ForeignKey('storage.roots.id'), nullable=False, index=True, comment='the OCFL storage root id that the object is stored in')

    object_root = relationship('Root')

    def __eq__(self, other):
        return (
                self.bdrc_id , other.bdrc_id
                and eq_if( self.root , other.root)
                and eq_if( self.created_at , other.created_at)
                and eq_if( self.last_modified_at , other.last_modified_at))

class ImagePath(Base):
    __tablename__ = 'paths'
    __table_args__ = {'schema': 'storage','comment': 'ImageFile Paths of objects'}

    id = Column(INTEGER, primary_key=True)
    file = Column(ForeignKey('storage.files.id'), index=True)
    storage_object = Column(ForeignKey('storage.objects.id'), index=True)
    path = Column(VARCHAR(1024), comment='Unicode string (256 Unicode characters max) representing the (case sensitive) content paths in OCFL objects for each content file.')
    image_group = Column(VARCHAR(32), comment='the BDRC image group RID (ex: I0886), unique persistent identifier, ASCII string no longer than 32 characters, when unknown set to NULL')
    root_folder = Column(Enum('images', 'archive', 'sources', 'backup', 'eBooks', 'web', 'other'), comment='should be obvious. other can be anything, not just the folder other')

    image_file = relationship('ImageFile')
    image_object = relationship('ArchiveObject')

    def __eq__(self, other):
        return (
                self.file , other.file
                and eq_if( self.storage_object , other.storage_object)
                and eq_if( self.path , other.path)
                and eq_if( self.image_group , other.image_group)
                and eq_if( self.root_folder , other.root_folder))
