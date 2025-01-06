"""
Generate a Files ORM object
"""
import csv
import hashlib
import sys
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
    from fido.fido import Fido
    import io

    image_fi = Fido(format_files=['formats-v109.xml',
                                  'format_extensions.xml'])
    #
    # Redirect output
    try:

        # Create a StringIO object to capture the output
        captured_output = io.StringIO()

        # Redirect sys.stdout to the StringIO object
        sys.stdout = captured_output
        image_fi.identify_file(str(f))
        # Read cpptured_output as a csv

        # 'OK,930,fmt/353,"Tagged Image File Format","TIFF generic (little-endian)",19572,"/Users/***/dev/tmp/Archive1/34/W23834/images/W23834-3187/31870009.tif","image/tiff","signature"
        _sample_output = """
        %(info.time)s,   930
        %(info.puid)s,   fmt/353//
        %(info.formatname)s,'Tagged Image File Format
        %(info.signaturename)s, 'TIFF generic (little-endian
        %(info.filesize)s,\" 19752
        %(info.filename)s"  ...../.../.../images/W23834-3187/31870009.tif
        %(info.mimetype)s\"    "image/tiff"
        %(info.matchtype)s\"         "signature"
        """
        csv_reader =  csv.reader(captured_output.getvalue().split('\n'))
        for row in csv_reader:
            pronom_number = row[0]
            pronom_text = row[1]
           # return pronom_number, pronom_text
    except Exception as e:
        sys.stderr.print(f"Error: {e}")
    finally:
        sys.stdout = sys.__stdout__


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
