import io 
from typing import Union, List
from pathlib import Path
from xmlrpc.client import Boolean
import zipfile
import os
import boto3
from fnmatch import fnmatch
import pandas as pd


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
    out_path: Union[Path, str]=None, 
    delete_zip: Boolean = True):
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


def get_dir_files_s3(bucket_name: str, dir_name: str='') -> List[str]:
    """Get a list of all files in bucket directory.

    Args:
        bucket_name (str): S3 bucket name
        dir_name (str, optional): S3 bucket directory name. Defaults to ''.

    Returns:
        List[str]: List of file names in bucket directory
    """
    s3_resources = boto3.resource("s3")
    my_bucket = s3_resources.Bucket(bucket_name)
    return [
        object_summary.key
        for object_summary in my_bucket.objects.filter(Prefix=dir_name)
    ]


def df_to_fileobj(df: pd.DataFrame, save_file_dir: str) -> io.BytesIO:
    """Convert DataFrame into bytes file object.
    
    Args:
        df (pd.DataFrame): Dataframe to convert.
        save_file_dir (io.BytesIO): Saving file name.

    Returns:
        io.BytesIO: Bytes file object.
    """
    buffer = io.BytesIO()
    if fnmatch(save_file_dir, "*.csv"):
        df.to_csv(buffer)
    elif fnmatch(save_file_dir, "*.json"):
        df.to_json(buffer) 
    buffer.seek(0)
    return buffer


def fileobj_to_df(fileobj: io.BytesIO, load_file_dir: str) -> pd.DataFrame:
    """Convert bytes file object into DataFrame.

    Args:
        buffer (io.BytesIO): Bytes file object.
        file_dir (str): Loading file name.

    Returns:
        pd.DataFrame: Dataframe converted
    """
    if fnmatch(load_file_dir, "*.csv"):
        df = pd.read_csv(fileobj)
    elif fnmatch(load_file_dir, "*.json"):
        df = pd.read_json(fileobj) 
    return df


def upload_data_s3(
    data: Union[io.BytesIO, pd.DataFrame], 
    bucket: str, 
    save_file_path: str):
    """Upload data to S3 location.

    Args:
        data (Union[io.BytesIO, pd.DataFrame]): Data to upload.
        bucket (str): Bucket's name.
        save_file_path (str): Path location to save data.
    """
    s3 = boto3.client('s3')
    if isinstance(data, pd.DataFrame):
        obj =  df_to_fileobj(data, save_file_path)
        s3.upload_fileobj(obj, bucket, save_file_path)      
    elif isinstance(data, io.BytesIO):
        s3.upload_fileobj(data, bucket, save_file_path)
    else:
        raise Exception(
            'Function supports data only as "io.BytesIO" or "io.DataFrame".'
        )


def download_data_s3(
    bucket: str, 
    file_path: str, 
    asDataFrame: bool=False) -> Union[io.BytesIO, pd.DataFrame]:
    """Download data from S3 location.

    Args:
        bucket (str): Bucket's name.
        file_path (str): File path to loading data.
        asDataFrame (bool, optional): If True: return the data as pd.DataFrame. If False: return data as io.BytesIO. Default: False. 

    Returns:
        Union[io.BytesIO, pd.DataFrame]: Downloaded data.
    """
    s3 = boto3.client('s3')
    fileobj= io.BytesIO()
    s3.download_fileobj(bucket, file_path, fileobj)
    fileobj.seek(0)
    return (fileobj_to_df(fileobj, file_path) 
            if asDataFrame else fileobj)