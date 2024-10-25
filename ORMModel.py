from typing import List, Optional

from sqlalchemy import BINARY, Enum, Index, TIMESTAMP, ForeignKeyConstraint, String, Integer, text
from sqlalchemy import MetaData
from sqlalchemy.dialects.mssql import TINYINT
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, SMALLINT, VARCHAR
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

__all__ = ['Files', 'Objects', 'Paths', 'Roots', 'PdfFileInfos', 'ImageFileInfos']
ContentBase = declarative_base(metadata=MetaData(schema='content'))
StorageBase = declarative_base(metadata=MetaData(schema='storage'))
Base = declarative_base()


class Files(Base):
    __tablename__ = 'files'
    __table_args__ = (
        Index('files_index_1', 'digest', 'size', unique=True),
        Index('persistent_id', 'persistent_id', unique=True),
        {'comment': 'Table of all the (deduplicated) actual files handled by ArchiveStorage',
         'schema': 'storage'}
    )
    id = mapped_column(INTEGER, primary_key=True)
    digest = mapped_column(BINARY(32), nullable=False, comment='the digest of the file')
    size = mapped_column(BIGINT, nullable=False, comment='the size in bytes')
    persistent_id = mapped_column(BINARY(32), nullable=False,
                                  comment='The identifier is globally unique for the BDRC archive. By construction it is the sha256 or a random id in case of collision.')
    validity = mapped_column(Enum('seemingly_valid', 'fully_valid', 'cannot_read', 'partially_recoverable', 'not_set'),
                             nullable=False, comment='the validity of the image')
    pronom_number = mapped_column(SMALLINT, comment='the PRONOM number or, if unavailable, null')
    created_at = mapped_column(TIMESTAMP,
                               comment='the creation date of the file. Often unknown or unreliable, can be set to the earlier mtime exposed by the FS')
    earliest_mdate = mapped_column(TIMESTAMP, comment='the earliest modification date for the file (optional)')

    def __eq__(self, other):
        return (
                self.digest == other.digest
                and self.size == other.size
                and self.persistent_id == other.persistent_id
                and self.validity == other.validity
                and self.pronom_number == other.pronom_number
                and self.created_at == other.created_at
                and self.earliest_mdate == other.earliest_mdate )
    # paths: Mapped[List['Paths']] = relationship('Paths', uselist=True, back_populates='files')
    # image_file_infos: Mapped[List['ImageFileInfos']] = relationship('ImageFileInfos', back_populates='files')
    # Try to test - see test_data_model_image


class Objects(Base):
    __tablename__ = 'objects'
    __table_args__ = (
        # When using multiple schemas, declare the FK in TableArgs.  The mapped_column(ForeignKey("table.column") cant
        # qualify the schema
        ForeignKeyConstraint(['root'], ['storage.roots.id'], name='objects_ibfk_1'),
        Index('objects_index_0', 'bdrc_id', 'root', unique=True),
        Index('root', 'root'),
        {'comment': 'Objects kept on archive storage',
         'schema': 'storage'}
    )

    id = mapped_column(INTEGER, primary_key=True, comment='internal identifier')
    bdrc_id = mapped_column(String(32), nullable=False,
                            comment='the BDRC RID (ex: W22084), unique persistent identifier, ASCII string no longer than 32 characters')
    root = mapped_column(INTEGER, nullable=False, comment='the OCFL storage root id that the object is stored in')
    created_at = mapped_column(TIMESTAMP,
                               comment='the timestamp of the creation of the object, or the equivalent object in a previous archive storage')
    last_modified_at = mapped_column(TIMESTAMP, comment='the timestamp of the last known modification')

    def __eq__(self, other):
        return (
                self.bdrc_id == other.bdrc_id
                and self.root == other.root
                and self.created_at == other.created_at
                and self.last_modified_at == other.last_modified_at)


class Paths(Base):
    __tablename__ = 'paths'
    __table_args__ = (
        ForeignKeyConstraint(['file'], ['storage.files.id'], name='paths_ibfk_1'),
        ForeignKeyConstraint(['storage_object'], ['storage.objects.id'], name='paths_ibfk_2'),
        Index('file', 'file'),
        Index('storage_object', 'storage_object'),
        {'comment': 'File Paths of objects',
         'schema': 'storage'}
    )

    id = mapped_column(INTEGER, primary_key=True)
    file = mapped_column(Integer, comment='storage.files.id FK')
    storage_object = mapped_column(Integer, comment='storage.objects.id FK')
    path = mapped_column(VARCHAR(1024),
                         comment='Unicode string (256 Unicode characters max) representing the (case sensitive) content paths in OCFL objects for each content file.')
    image_group = mapped_column(VARCHAR(32),
                                comment='the BDRC image group RID (ex: I0886), unique persistent identifier, ASCII string no longer than 32 characters, when unknown set to NULL')
    root_folder = mapped_column(Enum('images', 'archive', 'sources', 'backup', 'eBooks', 'web', 'other'),
                                comment='should be obvious. other can be anything, not just the folder other')

    def __eq__(self, other):
        return (
                self.file == other.file
                and self.storage_object == other.storage_object
                and self.path == other.path
                and self.image_group == other.image_group
                and self.root_folder == other.root_folder)

class Roots(Base):
    __tablename__ = 'roots'
    __table_args__ = {'comment': 'Storage roots (ex: Archive 1)',
                      'schema': 'storage'
                      }

    id = mapped_column(INTEGER, primary_key=True, comment='internal identifier of the root object')
    name = mapped_column(VARCHAR(32), nullable=False,
                         comment='name of the Storage root (in ASCII), used to fint it on disk (ex: Archive0). The actual disk path depends on the mount points on the servers.')
    layout = mapped_column(VARCHAR(50), nullable=False, comment='name of the storage layout, ASCII')

    def __eq__(self, other):
        return  ( self.name == other.name
                and self.layout == other.layout )


class PdfFileInfos(Base):
    __tablename__ = 'pdf_file_infos'
    __table_args__ = (
        ForeignKeyConstraint(['storage_file'], ['storage.files.id'], name='pdf_file_infos_ibfk_1'),
        Index('storage_file', 'storage_file')
    )

    id = mapped_column(INTEGER, primary_key=True)
    storage_file = mapped_column(INTEGER, comment='storage.files.id FK')
    number_of_pages = mapped_column(SMALLINT, comment='the number of pages')
    median_nb_chr_per_page = mapped_column(SMALLINT, comment='the average number of characters in a page')
    median_nb_images_per_page = mapped_column(SMALLINT, comment='the average number of images per page')
    recorded_date = mapped_column(TIMESTAMP, comment='the timestamp recorded in the exif metadata')
    storage_file_id = mapped_column(Integer, comment='storage.files.id FK')
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __eq__(self, other):
        return (
                self.number_of_pages == other.number_of_pages
                and self.median_nb_chr_per_page == other.median_nb_chr_per_page
                and self.median_nb_images_per_page == other.median_nb_images_per_page
                and self.recorded_date == other.recorded_date
                and self.storage_file_id == other.storage_file_id )


class ImageFileInfos(Base):
    __tablename__ = 'image_file_infos'
    __table_args__ = (
        ForeignKeyConstraint(['storage_file_id'], ['storage.files.id'], name='image_file_infos_ibfk_1'),
        Index('storage_file_id_IDX', 'storage_file_id'),
        {'comment': 'Table containing information about image files'}
    )

    id = mapped_column(INTEGER, primary_key=True)
    image_type = mapped_column(Enum('jpg', 'png', 'single_image_tiff', 'jp2', 'raw'), nullable=False)
    image_mode = mapped_column(Enum('1', 'L', 'RGB', 'RGBA', 'CMYK', 'P', 'OTHER'), nullable=False)
    width = mapped_column(SMALLINT, nullable=False,
                          comment='width of the bitmap (not taking a potential exif rotation into account)')
    height = mapped_column(SMALLINT, nullable=False,
                           comment='height of the bitmap (not taking a potential exif rotation into account)')
    bps_x = mapped_column(TINYINT, nullable=False, comment='bits per sample x')
    bps_y = mapped_column(TINYINT, nullable=False, comment='bits per sample y')
    # storage_file = mapped_column(ForeignKey("files.id"), comment='storage.files.id FK')
    storage_file_id = mapped_column(Integer, comment='storage.files.id FK')
    tiff_compression = mapped_column(
        Enum('raw', 'tiff_ccitt', 'group3', 'group4', 'tiff_lzw', 'tiff_jpeg', 'jpeg', 'tiff_adobe_deflate', 'lzma',
             'other'), comment='names are from PIL version 10')
    quality = mapped_column(TINYINT,
                            comment='relevant only for jpg, png and single_image_tiff encoded as jpg: quality of encoding. JPEG is represented between 0 and 100. For PNG this column encodes the compression between 0 and 9.')
    recorded_date = mapped_column(TIMESTAMP, comment='the timestamp recorded in the exif metadata')
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __eq__(self, other):
        return (
                self.image_type == other.image_type
                and self.image_mode == other.image_mode
                and self.width == other.width
                and self.height == other.height
                and self.bps_x == other.bps_x
                and self.bps_y == other.bps_y
                and self.storage_file_id == other.storage_file_id
                and self.tiff_compression == other.tiff_compression
                and self.quality == other.quality
                and self.recorded_date == other.recorded_date
                )


Objects.roots: Mapped[Roots] = relationship('Roots', back_populates='objects')
Roots.objects: Mapped[List[Objects]] = relationship('Objects', uselist=True, back_populates='roots')

Objects.paths: Mapped[List[Paths]] = relationship('Paths', uselist=True, back_populates='objects')
Paths.objects: Mapped[Optional[Objects]] = relationship('Objects', back_populates='paths')

Paths.files: Mapped[Optional[Files]] = relationship('Files', back_populates='paths')
Files.paths: Mapped[List[Paths]] = relationship(Paths, uselist=True, back_populates='files')

Files.image_file_infos: Mapped[List[ImageFileInfos]] = relationship('ImageFileInfos', back_populates='files')
ImageFileInfos.files: Mapped[Optional[Files]] = relationship('Files', back_populates='image_file_infos')

Files.pdf_file_infos: Mapped[List[PdfFileInfos]] = relationship('PdfFileInfos', back_populates='files')
PdfFileInfos.files: Mapped[Optional[Files]] = relationship('Files', back_populates='pdf_file_infos')
