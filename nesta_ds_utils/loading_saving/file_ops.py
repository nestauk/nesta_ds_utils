from typing import Union
from pathlib import Path
import zipfile
import os


def _convert_str_to_pathlib_path(path: Union[Path, str]) -> Path:
    """Converts a path written as a string to pathlib format.

    Args:
        path (Union[Path, str]): File path in string format.

    Returns:
        Path: Path in pathlib format.
    """
    return Path(path) if type(path) is str else path


def make_path_if_not_exist(path: Union[Path, str]):
    """Check if path exists, if it does not exist then create it.

    Args:
        path (Union[Path, str]): File path.
    """
    path = _convert_str_to_pathlib_path(path)
    if not path.exists():
        path.mkdir(parents=True)


def extractall(
    zip_path: Union[Path, str],
    out_path: Union[Path, str] = None,
    delete_zip: bool = True,
):
    """Takes path to zipped file and extracts it to specified output path.

    Args:
        zip_path (Union[Path, str]): Path to zipped file.
        out_path (Union[Path, str], optional): Path where contents will be unzipped to. Defaults to None.
        delete_zip (Boolean, optional): Option to delete zip file after extracted. Defaults to True.
    """
    if out_path is None:
        out_path = zip_path.rsplit("/", 1)[0]

    make_path_if_not_exist(out_path)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(out_path)

    if delete_zip is True:
        os.remove(zip_path)
