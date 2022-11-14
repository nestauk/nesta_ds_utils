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
import pyarrow as pa
import pyarrow.parquet as pq
import json
import pickle
from dicttoxml import dicttoxml
import warnings


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
    bucket = s3_resources.Bucket(bucket_name)
    return [
        object_summary.key for object_summary in bucket.objects.filter(Prefix=dir_name)
    ]


def _df_to_fileobj(df_data: pd.DataFrame, path_to: str, **kwargs) -> io.BytesIO:
    """Convert DataFrame into bytes file object.

    Args:
        df (pd.DataFrame): Dataframe to convert.
        path_to (str): Saving file name.

    Returns:
        io.BytesIO: Bytes file object.
    """
    buffer = io.BytesIO()
    if fnmatch(path_to, "*.csv"):
        df_data.to_csv(buffer, **kwargs)
    elif fnmatch(path_to, "*.parquet"):
        df_data.to_.parquet(buffer, **kwargs)
    else:
        raise Exception(
            "Uploading dataframe currently supported only for 'csv' and 'parquet'."
        )
    buffer.seek(0)
    return buffer


def _dict_to_fileobj(dict_data: dict, path_to: str, **kwargs) -> io.BytesIO:
    """Convert dictionary into bytes file object.

    Args:
        dict_data (dict): Dictionary to convert.
        path_to (str): Saving file name.

    Returns:
        io.BytesIO: Bytes file object.
    """
    buffer = io.BytesIO()
    if fnmatch(path_to, "*.json"):
        buffer.write(json.dumps(dict_data, **kwargs).encode())
    elif fnmatch(path_to, ".xml"):
        buffer.write(dicttoxml(dict_data, **kwargs))
    else:
        raise Exception(
            "Uploading dictionary currently supported only for 'json' and 'xml'."
        )
    buffer.seek(0)
    return buffer


def _list_to_fileobj(list_data: list, path_to: str, **kwargs) -> io.BytesIO:
    """Convert list into bytes file object.

    Args:
        list_data (list): List to convert.
        path_to (str): Saving file name.

    Returns:
        io.BytesIO: Bytes file object.
    """
    buffer = io.BytesIO()
    if fnmatch(path_to, "*.csv"):
        pd.DataFrame(list_data).to_csv(buffer, **kwargs)
    elif fnmatch(path_to, ".txt"):
        for row in list_data:
            buffer.write(bytes(str(row) + "\n", "utf-8"))
    elif fnmatch(path_to, ".json"):
        buffer.write(json.dumps(dict_data, **kwargs).encode())
    else:
        raise Exception(
            "Uploading list currently supported only for 'csv', 'txt' and 'json'."
        )
    buffer.seek(0)
    return buffer


def _str_to_fileobj(str_data: str, path_to: str, **kwargs) -> io.BytesIO:
    """Convert str into bytes file object.

    Args:
        str_data (str): String to convert.
        path_to (str): Saving file name.

    Returns:
        io.BytesIO: Bytes file object.
    """
    if fnmatch(path_to, "*.txt"):
        buffer = io.BytesIO(bytes(str_data.encode("utf-8")))
    else:
        raise Exception("Uploading string currently supported only for 'txt'.")
    buffer.seek(0)
    return buffer


def _np_array_to_fileobj(
    np_array_data: np.ndarray, path_to: str, **kwargs
) -> io.BytesIO:
    """Convert numpy array into bytes file object.

    Args:
        np_array_data (str): Numpy array to convert.
        path_to (str): Saving file name.

    Returns:
        io.BytesIO: Bytes file object.
    """
    buffer = io.BytesIO()
    if fnmatch(path_to, "*.csv"):
        np.savetxt(buffer, np_array_data, delimiter=",", **kwargs)
    elif fnmatch(path_to, "*.parquet"):
        pq.write_table(pa.table({"data": np_array_data}), buffer, **kwargs)
    else:
        raise Exception(
            "Uploading numpy array currently supported only for 'csv' and 'parquet."
        )
    buffer.seek(0)
    return buffer


def _unsupp_data_to_fileobj(data: any, path_to: str, **kwargs) -> io.BytesIO:
    """Convert data into bytes file object using pickle file type.

    Args:
        data (any): Data to convert.
        path_to (str): Saving file name.

    Returns:
        io.BytesIO: Bytes file object.
    """
    buffer = io.BytesIO()
    if fnmatch(path_to, "*.pkl"):
        pickle.dump(data, buffer, **kwargs)
    else:
        raise Exception(
            "This file type is not supported for this data. Use 'pkl' instead."
        )
    buffer.seek(0)
    return buffer


def upload_obj(
    obj: any,
    bucket: str,
    path_to: str,
    kwargs_upload: dict = None,
    kwargs_writing: dict = None,
):
    """Uploads data from memory to S3 location.

    Args:
        obj (any): Data to upload.
        bucket (str): Bucket's name.
        path_to (str): Path location to save data.
        kwargs_upload (dict, optional): Dictionary of kwargs for boto3 function 'upload_fileobj'.
        kwargs_writing (dict, optional): Dictionary of kwargs for writing data.

    """
    if isinstance(obj, pd.DataFrame):
        obj = _df_to_fileobj(obj, path_to, **kwargs_writing)
    elif isinstance(obj, dict):
        obj = _dict_to_fileobj(obj, path_to, **kwargs_writing)
    elif isinstance(obj, list):
        obj = _list_to_fileobj(obj, path_to, **kwargs_writing)
    elif isinstance(obj, str):
        obj = _str_to_fileobj(obj, path_to, **kwargs_writing)
    elif isinstance(obj, np.ndarray):
        obj = _np_array_to_fileobj(obj, path_to, **kwargs_writing)
    else:
        obj = _unsupp_data_to_fileobj(obj, path_to, **kwargs_writing)
        warnings.warn(
            "Data uploaded using pickle. Please consider other accessible "
            "file types among the suppoted ones."
        )

    s3 = boto3.client("s3")
    s3.upload_fileobj(obj, bucket, path_to, **kwargs_upload)


def _fileobj_to_df(fileobj: io.BytesIO, load_file_dir: str, **kwargs) -> pd.DataFrame:
    """Convert bytes file object into DataFrame.

    Args:
        buffer (io.BytesIO): Bytes file object.
        load_file_dir (str): Loading file name.

    Returns:
        pd.DataFrame: Dataframe converted
    """
    if fnmatch(load_file_dir, "*.csv"):
        df = pd.read_csv(fileobj, **kwargs)
    elif fnmatch(load_file_dir, "*.parquet"):
        df = pd.read_parquet(fileobj, **kwargs)
    else:
        raise Exception(
            "Automatic convertion into pd.DataFrame currently supported "
            "only for 'csv'and 'parquet'."
        )
    return df

    obj = S3.Object(bucket_name, output_file_dir)

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
    s3.download_fileobj(bucket, file_name_from, fileobj)
    fileobj.seek(0)
    return _fileobj_to_df(fileobj, file_name_from, **kwargs) if asDataFrame else fileobj


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
