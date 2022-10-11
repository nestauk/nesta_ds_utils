from io import BytesIO
from typing import Union
from pathlib import Path
from xmlrpc.client import Boolean
import zipfile
import os
import boto3
from fnmatch import fnmatch
import pickle
import json
from typing import List
import pandas as pd
import io
import csv
S3 = boto3.resource("s3")


def _convert_str_to_pathlib_path(path: Union[Path, str]) -> Path:
    """Converts a path written as a string to pathlib format

    :param path: file path in string format
    :type path: str or pathlib.path
    :return: path in pathlib format
    :rtype: pathlib.Path
    """
    return Path(path) if type(path) is str else path


def make_path_if_not_exist(path: Union[Path, str]):
    """Check if path exists, if it does not exist then create it

    :param path: file path 
    :type path: pathlib.Path or str
    """
    path = _convert_str_to_pathlib_path(path)
    if not path.exists():
        path.mkdir(parents=True)


def extractall(zip_path: Union[Path, str], out_path: Union[Path, str]=None, delete_zip: Boolean = True):
    """Takes path to zipped file and extracts it to specified output path
    :param zip_path: path to zipped file
    :type zip_path: str or pathlib.Path
    :param out_path: path where contents will be unzipped to
    :type out_path: str or pathlib.Path
    :param delete_zip: option to delete zip file after extracted
    :type delete_zip: Boolean
    """

    if out_path is None:
        out_path = zip_path.rsplit("/", 1)[0]

    make_path_if_not_exist(out_path)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(out_path)
    
    if delete_zip is True:
        os.remove(zip_path)


def get_s3_dir_files(bucket_name: str, dir_name: str='') -> List[str]:
    """Get a list of all files in bucket directory.

    Args:
        bucket_name (str): S3 bucket name
        dir_name (str, optional): S3 bucket directory name. Defaults to ''.

    Returns:
        List[str]: List of file names in bucket directory
    """

    my_bucket = S3.Bucket(bucket_name)
    return [
        object_summary.key
        for object_summary in my_bucket.objects.filter(Prefix=dir_name)
    ]


def load_from_s3(bucket_name: str, file_name: str) -> Union[pd.DataFrame, str, dict]:
    """Load data from S3 location.

    Args:
        bucket_name (str): The S3 bucket name
        file_name (str): S3 key to load

    Returns:
        Union[pd.DataFrame, str, dict]: Loaded data from S3 location.
    """

    obj = S3.Object(bucket_name, file_name)
    if fnmatch(file_name, "*.csv") or fnmatch(file_name, "*.tsv"):
        return pd.read_csv(f"s3://{bucket_name}/{file_name}")
    elif fnmatch(file_name, "*.tsv.zip"):
        return pd.read_csv(
            f"s3://{bucket_name}/{file_name}",
            compression="zip",
            sep="\t",
        )
    elif fnmatch(file_name, "*.pickle") or fnmatch(file_name, "*.pkl"):
        file = obj.get()["Body"].read()
        return pickle.loads(file)
    elif fnmatch(file_name, "*.txt"):
        file = obj.get()["Body"].read().decode()
        return [f.split("\t") for f in file.split("\n")]
    elif fnmatch(file_name, "*.json"):
        file = obj.get()["Body"].read().decode()
        return json.loads(file)
    else:
        raise Exception( 
        'Function not supported for file type other than "*.json", *.txt", "*.pickle", "*.tsv" and "*.csv"'
        )


def save_to_s3(bucket_name: str, output_file_dir: str, output_var: Union[pd.DataFrame, str, dict]):
    """Save data to S3 location.
    
    Args:
        bucket_name (str): The S3 bucket name
        output_file_dir (str): File path to save object to
        output_var (Union[pd.DataFrame, str, dict]): Data to be saved
    """

    obj = S3.Object(bucket_name, output_file_dir)

    if fnmatch(output_file_dir, "*.pkl") or fnmatch(output_file_dir, "*.pickle"):
        obj.put(Body=pickle.dumps(output_var))
    elif fnmatch(output_file_dir, "*.txt"):
        if not isinstance(output_var, str):
            raise Exception(
                'Saving in .txt format is supported only for \'str\' data.'
            )
        obj.put(Body=output_var)
    elif fnmatch(output_file_dir, "*.csv"):
        if isinstance(output_var, pd.DataFrame):
            output_var.to_csv("s3://" + bucket_name + "/" + output_file_dir, index=False)
        elif isinstance(output_var, dict):
            csv_stream = io.StringIO()
            with csv_stream as f:  
                w = csv.DictWriter(f, output_var.keys())
                w.writeheader()
                w.writerow(output_var)
                obj.put(Body=csv_stream.getvalue())
        else:
            obj.put(Body=output_var)          
    elif fnmatch(output_file_dir, "*.json"):
        if isinstance(output_var, pd.DataFrame):
            output_var.to_json("s3://" + bucket_name + "/" + output_file_dir)
        else:
            obj.put(Body=json.dumps(output_var))
    else:
        raise Exception(
            'Function not supported for file type other than "*.json", *.txt", "*.pickle" and "*.csv"'
        )