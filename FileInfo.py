"""
Generate a Files ORM object
"""
import hashlib
from datetime import datetime
from pathlib import Path

from ORMModel import ImageFile


def f_validity(f: Path) -> ():
    return 'not_set'


def f_pronoms(f: Path) -> ():
    """
    Return a tuple of the pronom number and text
    :param f: Path to file
    :return: Tuple of pronom number and text
    """
    # Until we get fido wired in
    from fido import fido

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


def f_created(f: Path) -> datetime:
    return datetime.fromtimestamp(f.stat().st_ctime)


def f_to_files(f: Path) -> ImageFile:
    """
    Generate a Files ORM object
    :param f: Path to file
    :return: Files ORM object
    """
    f_digest = f_md5(f)
    f_pronom: () = f_pronoms(f)
    return ImageFile(
        digest=f_digest,
        size=f_size(f),
        persistent_id=f_digest,  # provisional
        validity="not_set",
        pronom_number=f_pronom[0],
        created_at=f_created(f),
        earliest_mdate=None)
