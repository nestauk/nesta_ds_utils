
from io import BytesIO
from typing import Union
import pathlib
import zipfile
import logging

logger = logging.getLogger(__name__)

def convert_str_to_pathlib_path(path: Union[pathlib.Path, str]) -> pathlib.Path:
    """Converts a path written as a string to pathlib format

    :param path: file path in string format
    :type path: str or pathlib.path
    :return: path in pathlib format
    :rtype: pathlib.Path
    """
    return pathlib.Path(path) if type(path) is str else path

def make_path_if_not_exist(path: Union[pathlib.Path, str]):
    """Check if path exists, if it does not exist then create it

    :param path: file path 
    :type path: pathlib.Path or str
    """
    path = convert_str_to_pathlib_path(path)
    if not path.exists():
        path.mkdir(parents=True)

def extractall(zipPath: Union[pathlib.Path, str], outPath: Union[pathlib.Path, str]):
    """Takes path to zipped file and extracts it to specified output path
    :param zipPath: path to zipped file
    :type zipPath: str or pathlib.Path
    :param outPath: path where contents will be unzipped to
    :type outPath: str or pathlib.Path
    """
    logger.info(f"Extracting to {outPath}")

    make_path_if_not_exist(outPath)
    with zipfile.ZipFile(zipPath,'r') as z:
        z.extractall(outPath)