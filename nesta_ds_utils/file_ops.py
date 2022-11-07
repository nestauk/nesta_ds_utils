import io
from typing import Union, List
from pathlib import Path
from xmlrpc.client import Boolean
import zipfile
import os
import boto3
from fnmatch import fnmatch
import pandas as pd
import numpy as np


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
    delete_zip: Boolean = True,
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


def get_bucket_filenames_s3(bucket_name: str, dir_name: str = "") -> List[str]:
    """Get a list of all files in bucket directory.

    Args:
        bucket_name (str): S3 bucket name
        dir_name (str, optional): Directory or sub-directory within an S3 bucket.
            Defaults to '' (the top level bucket directory).

    Returns:
        List[str]: List of file names in bucket directory.
    """
    s3_resources = boto3.resource("s3")
    my_bucket = s3_resources.Bucket(bucket_name)
    return [
        object_summary.key
        for object_summary in my_bucket.objects.filter(Prefix=dir_name)
    ]


def _df_to_fileobj(df: pd.DataFrame, save_file_dir: str) -> io.BytesIO:
    """Convert DataFrame into bytes file object.

    Args:
        df (pd.DataFrame): Dataframe to convert.
        save_file_dir (str): Saving file name.

    Returns:
        io.BytesIO: Bytes file object.
    """
    buffer = io.BytesIO()
    if fnmatch(save_file_dir, "*.csv"):
        df.to_csv(buffer)
    elif fnmatch(save_file_dir, "*.json"):
        df.to_json(buffer)
    elif fnmatch(save_file_dir, "*.pkl"):
        df.to_pickle(buffer)
    elif fnmatch(save_file_dir, "*.xml"):
        df.to_xml(buffer)
    else:
        raise Exception(
            "Automatic convertion from pd.DataFrame currently supported only for 'csv', 'json', 'pkl' and 'xml'."
        )
    buffer.seek(0)
    return buffer


def _fileobj_to_df(fileobj: io.BytesIO, load_file_dir: str) -> pd.DataFrame:
    """Convert bytes file object into DataFrame.

    Args:
        buffer (io.BytesIO): Bytes file object.
        load_file_dir (str): Loading file name.

    Returns:
        pd.DataFrame: Dataframe converted
    """
    if fnmatch(load_file_dir, "*.csv"):
        df = pd.read_csv(fileobj)
    elif fnmatch(load_file_dir, "*.json"):
        df = pd.read_json(fileobj)
    elif fnmatch(load_file_dir, "*.pkl"):
        df = pd.read_pickle(fileobj)
    elif fnmatch(load_file_dir, "*.xml"):
        df = pd.read_xml(fileobj)
    else:
        raise Exception(
            "Automatic convertion into pd.DataFrame currently supported only for 'csv', 'json', 'pkl' and 'xml'."
        )
    return df

    obj = S3.Object(bucket_name, output_file_dir)

def upload_obj(
    obj: Union[io.BytesIO, pd.DataFrame], bucket: str, file_name_to: str, **kwargs
):
    """Uploads data from memory to S3 location.

    Args:
        obj (Union[io.BytesIO, pd.DataFrame]): Data to upload.
        bucket (str): Bucket's name.
        file_name_to (str): Path location to save data.

    Raises:
        Exception: Util supports data only as "io.BytesIO" or "pd.DataFrame".
    """
    s3 = boto3.client("s3")
    if isinstance(obj, pd.DataFrame):
        obj = _df_to_fileobj(obj, file_name_to)
    if isinstance(obj, io.BytesIO):
        s3.upload_fileobj(obj, bucket, file_name_to, kwargs)
    else:
        raise Exception('Util supports data only as "io.BytesIO" or "pd.DataFrame".')


def download_obj(
    bucket: str, file_name_from: str, asDataFrame: bool = False, **kwargs
) -> Union[io.BytesIO, pd.DataFrame]:
    """Download data to memory from S3 location.

    Args:
        bucket (str): Bucket's name.
        file_name_from (str): Path to data in S3.
        asDataFrame (bool, optional): If True: return the data as pd.DataFrame.
        If False: return data as io.BytesIO. Default: False.

    Returns:
        Union[io.BytesIO, pd.DataFrame]: Donwloaded data.
    """
    s3 = boto3.client("s3")
    fileobj = io.BytesIO()
    s3.download_fileobj(bucket, file_name_from, fileobj, kwargs)
    fileobj.seek(0)
    return _fileobj_to_df(fileobj, file_name_from) if asDataFrame else fileobj


def upload_file(file_name_from: str, bucket: str, file_name_to: str, **kwargs):
    """Upload local file from disk to S3 location.

    Args:
        file_name_from (str): Path to local file.
        bucket (str): Bucket's name.
        file_name_to (str): Destination path in S3.
    """
    s3 = boto3.client("s3")
    s3.upload_file(file_name_from, bucket, file_name_to, kwargs)


def download_file(file_name_from: str, bucket: str, file_name_to: str, **kwargs):
    """Download data from S3 to local file on disk.

    Args:
        file_name_from (str): Path to data in S3
        bucket (str): Buket's name
        file_name_to (str): Destination path to disk.
    """
    # Create folder if not existing
    make_path_if_not_exist(_convert_str_to_pathlib_path(file_name_to).parents[0])
    s3 = boto3.client("s3")
    s3.download_file(bucket, file_name_from, file_name_to, kwargs)
