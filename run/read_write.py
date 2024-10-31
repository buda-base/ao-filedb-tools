"""
Test stub to do a read write
"""
import argparse
import os
from pathlib import Path

from BdrcDbLib.DbOrm.DrsContextBase import DrsDbContextBase
import image_info as ii
import FileInfo as fi


def must_exist_path(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"Path '{path}' does not exist.")
    return path
class RwArgParser():
    """
    inherit db connection methods
    """
    _parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Read images, put into db")
    def __init__(self):
        self._parser.add_argument("-s", "--storage-db", required=True, help="storage db config entry")
        self._parser.add_argument("-c", "--content-db", required=True, help="content db config entry")
        self._parser.add_argument("-p", "--path", required=True, help="path to read (file or dir)",type=must_exist_path)


    def parse_args(self):
        return self._parser.parse_args()


def main():
    """
    shell to read and write a file
    :return:
    """
    args = RwArgParser().parse_args()
    src: Path = Path(args.path)
    with DrsDbContextBase(args.content_db) as content_db:
        if src.is_dir():
            nlim: int = 0
            print(f"Reading directory {src}")
            for p in src.iterdir():
                print(f"Reading {str(p)}")
                _orm_image = read_one(p)
                _orm_image.file_path = str(p)
                _orm_file = fi.f_to_files(p)
                if not _orm_image.files:
                    _orm_image.files = [_orm_file]
                else:
                    _orm_image.files.append(_orm_file)
                if not _orm_image:
                    print(f"Skipping dir entry {str(p)}")
                    continue
                else:
                    content_db.session.add(_orm_image)
                    nlim += 1
                    if nlim > 10:
                        content_db.session.commit()
                        nlim = 0

        if src.is_file():
            print(f"Reading file {src}")
            _orm_image = read_one(src)
            if not _orm_image:
                print(f"Skipping file {str(src)}")
            else:
                content_db.session.add(_orm_image)
                content_db.session.commit()


def read_one(p: Path)-> object:
    """
    Returns a BaseImage ORMModel client to its caller, if it can
    :param p: Path to image
    """
    _orm_image = None
    try:
        _image: ii.BaseImage = ii.image_info_factory(p)
        if isinstance(_image, ii.PilImage) or isinstance(_image, ii.RawImage):
            _orm_image = ii.base_image_to_image_file_infos(_image)
        if isinstance(_image, ii.PdfImage):
            _orm_image = ii.base_image_to_pdf_file_infos(_image)
    except Exception as e:
        print(f"Could not image process {str(p)}. Error {e}")
    return _orm_image

if __name__ == '__main__':
    main()

