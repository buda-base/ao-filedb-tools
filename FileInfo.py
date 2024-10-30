"""
Generate a Files ORM object
"""
import hashlib
from datetime import datetime
from pathlib import Path

from ORMModel import Files


def f_validity(f: Path) -> ():
    # Call fido on the
# Create an MD5 hash of the file
def f_md5(f: Path) -> str:
    """
    Generate an MD5 hash of the file
    :param f: Path to file
    :return: MD5 hash
    """
    hash_md5 = hashlib.md5()
    with open(f, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.digest()

def f_size(f: Path) -> int:
    return f.stat().st_size

def f_create(f: Path) -> datetime:
    return datetime.fromtimestamp(f.stat().st_ctime)
def f_to_files(f: Path) -> Files:
    """
    Generate a Files ORM object
    :param f: Path to file
    :return: Files ORM object
    """
    f_digest = f_md5(f)
    return Files(
        digest=f_digest,
        size=f_size(f),
        persistent_id=f_digest, # provisional
        comment="f{f.name}",
                                  comment='The identifier is globally unique for the BDRC archive. By construction it is the sha256 or a random id in case of collision.')
    validity = mapped_column(Enum('seemingly_valid', 'fully_valid', 'cannot_read', 'partially_recoverable', 'not_set'),
                             nullable=False, comment='the validity of the image')
    pronom_number = mapped_column(SMALLINT, comment='the PRONOM number or, if unavailable, null')
    created_at = mapped_column(TIMESTAMP,
                               comment='the creation date of the file. Often unknown or unreliable, can be set to the earlier mtime exposed by the FS')
    earliest_mdate = mapped_column(TIMESTAMP, comment='the earliest modification date for the file (optional)')
