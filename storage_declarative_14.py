# coding: utf-8
from sqlalchemy import BINARY, Column, Enum, ForeignKey, Index, String, TIMESTAMP
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, SMALLINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class File(Base):
    __tablename__ = 'files'
    __table_args__ = (
        Index('files_index_1', 'digest', 'size', unique=True),
        {'comment': 'Table of all the (deduplicated) actual files handled by Archive Storage'}
    )

    id = Column(INTEGER, primary_key=True)
    digest = Column(BINARY(32), nullable=False, comment='the digest of the file')
    size = Column(BIGINT, nullable=False, comment='the size in bytes')
    pronom_number = Column(SMALLINT, comment='the PRONOM number or, if unavailable, null')
    persistent_id = Column(BINARY(32), nullable=False, unique=True, comment='The identifier is globally unique for the BDRC archive. By construction it is the sha256 or a random id in case of collision.')
    created_at = Column(TIMESTAMP, comment='the creation date of the file. Often unknown or unreliable, can be set to the earlier mtime exposed by the FS')
    validity = Column(Enum('seemingly_valid', 'fully_valid', 'cannot_read', 'partially_recoverable', 'not_set'), nullable=False, comment='the validity of the image')
    earliest_mdate = Column(TIMESTAMP, comment='the earliest modification date for the file (optional)')


class Root(Base):
    __tablename__ = 'roots'
    __table_args__ = {'comment': 'Storage roots (ex: Archive 1)'}

    id = Column(INTEGER, primary_key=True, comment='internal identifier of the root object')
    name = Column(VARCHAR(32), nullable=False, comment='name of the Storage root (in ASCII), used to fint it on disk (ex: Archive0). The actual disk path depends on the mount points on the servers.')
    layout = Column(VARCHAR(50), nullable=False, comment='name of the storage layout, ASCII')


class Object(Base):
    __tablename__ = 'objects'
    __table_args__ = (
        Index('objects_index_0', 'bdrc_id', 'root', unique=True),
        {'comment': 'Objects kept on archive storage'}
    )

    id = Column(INTEGER, primary_key=True, comment='internal identifier')
    bdrc_id = Column(String(32), nullable=False, comment='the BDRC RID (ex: W22084), unique persistent identifier, ASCII string no longer than 32 characters')
    created_at = Column(TIMESTAMP, comment='the timestamp of the creation of the object, or the equivalent object in a previous archive storage')
    last_modified_at = Column(TIMESTAMP, comment='the timestamp of the last known modification')
    root = Column(ForeignKey('roots.id'), nullable=False, index=True, comment='the OCFL storage root id that the object is stored in')

    root1 = relationship('Root')


class Path(Base):
    __tablename__ = 'paths'
    __table_args__ = {'comment': 'ImageFile Paths of objects'}

    id = Column(INTEGER, primary_key=True)
    file = Column(ForeignKey('files.id'), index=True)
    storage_object = Column(ForeignKey('objects.id'), index=True)
    path = Column(VARCHAR(1024), comment='Unicode string (256 Unicode characters max) representing the (case sensitive) content paths in OCFL objects for each content file.')
    image_group = Column(VARCHAR(32), comment='the BDRC image group RID (ex: I0886), unique persistent identifier, ASCII string no longer than 32 characters, when unknown set to NULL')
    root_folder = Column(Enum('images', 'archive', 'sources', 'backup', 'eBooks', 'web', 'other'), comment='should be obvious. other can be anything, not just the folder other')

    file1 = relationship('ImageFile')
    object = relationship('ArchiveObject')
