import io
from typing import List
import boto3
from fnmatch import fnmatch
import pandas as pd
import geopandas as gpd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import json
import pickle
import warnings
from nesta_ds_utils.loading_saving import file_ops


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
        df_data (pd.DataFrame): Dataframe to convert.
        path_to (str): Saving file name.

    Returns:
        io.BytesIO: Bytes file object.
    """
    buffer = io.BytesIO()
    if fnmatch(path_to, "*.csv"):
        df_data.to_csv(buffer, **kwargs)
    elif fnmatch(path_to, "*.parquet"):
        df_data.to_parquet(buffer, **kwargs)
    elif fnmatch(path_to, "*.xlsx"):
        df_data.to_excel(buffer, **kwargs)
    elif fnmatch(path_to, "*.xlsm"):
        df_data.to_excel(buffer, **kwargs)
    else:
        raise NotImplementedError(
            "Uploading dataframe currently supported only for 'csv', 'parquet', 'xlsx' and xlsm'."
        )
    buffer.seek(0)
    return buffer


def _gdf_to_fileobj(df_data: gpd.GeoDataFrame, path_to: str, **kwargs) -> io.BytesIO:
    """Convert GeoDataFrame into bytes file object.

    Args:
        df_data (gpd.DataFrame): Dataframe to convert.
        path_to (str): Saving file name.

    Returns:
        io.BytesIO: Bytes file object.
    """
    buffer = io.BytesIO()
    if fnmatch(path_to, "*.geojson"):
        df_data.to_file(buffer, driver="GeoJSON", **kwargs)
    else:
        raise NotImplementedError(
            "Uploading geodataframe currently supported only for 'geojson'."
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
    elif fnmatch(path_to, "*.geojson"):
        if "type" in dict_data:
            if dict_data["type"] in [
                "Point",
                "MultiPoint",
                "LineString",
                "MultiLineString",
                "Polygon",
                "MultiPolygon",
                "GeometryCollection",
                "Feature",
                "FeatureCollection",
            ]:
                buffer.write(json.dumps(dict_data, **kwargs).encode())
            else:
                raise AttributeError(
                    "GeoJSONS must have a member with the name 'type', the value of the member must "
                    "be one of the following: 'Point', 'MultiPoint', 'LineString', 'MultiLineString',"
                    "'Polygon', 'MultiPolygon','GeometryCollection', 'Feature' or 'FeatureCollection'."
                )
    else:
        raise NotImplementedError(
            "Uploading dictionary currently supported only for 'json' and 'geojson'."
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
    elif fnmatch(path_to, "*.txt"):
        for row in list_data:
            buffer.write(bytes(str(row) + "\n", "utf-8"))
    elif fnmatch(path_to, "*.json"):
        buffer.write(json.dumps(list_data, **kwargs).encode())
    else:
        raise NotImplementedError(
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
        raise NotImplementedError(
            "Uploading string currently supported only for 'txt'."
        )
    buffer.seek(0)
    return buffer


def _np_array_to_fileobj(
    np_array_data: np.ndarray, path_to: str, **kwargs
) -> io.BytesIO:
    """Convert numpy array into bytes file object.

    Args:
        np_array_data (np.ndarray): Numpy array to convert.
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
        raise NotImplementedError(
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
        raise NotImplementedError(
            "This file type is not supported for this data. Use 'pkl' instead."
        )
    buffer.seek(0)
    return buffer


def upload_obj(
    obj: any,
    bucket: str,
    path_to: str,
    kwargs_boto: dict = {},
    kwargs_writing: dict = {},
):
    """Uploads data from memory to S3 location.

    Args:
        obj (any): Data to upload.
        bucket (str): Bucket's name.
        path_to (str): Path location to save data.
        kwargs_boto (dict, optional): Dictionary of kwargs for boto3 function 'upload_fileobj'.
        kwargs_writing (dict, optional): Dictionary of kwargs for writing data.

    """
    if isinstance(obj, gpd.GeoDataFrame):
        obj = _gdf_to_fileobj(obj, path_to, **kwargs_writing)
    elif isinstance(obj, pd.DataFrame):
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
            "Data uploaded as pickle. Please consider other accessible "
            "file types among the supported ones."
        )

    s3 = boto3.client("s3")
    s3.upload_fileobj(obj, bucket, path_to, **kwargs_boto)


def _fileobj_to_df(fileobj: io.BytesIO, path_from: str, **kwargs) -> pd.DataFrame:
    """Convert bytes file object into dataframe.

    Args:
        fileobj (io.BytesIO): Bytes file object.
        path_from (str): Path of loaded data.

    Returns:
        pd.DataFrame: Data as dataframe.
    """
    if fnmatch(path_from, "*.csv"):
        return pd.read_csv(fileobj, **kwargs)
    elif fnmatch(path_from, "*.parquet"):
        return pd.read_parquet(fileobj, **kwargs)
    elif fnmatch(path_from, "*.xlsx"):
        return pd.read_excel(fileobj, **kwargs)
    elif fnmatch(path_from, "*.xlsm"):
        return pd.read_excel(fileobj, **kwargs)


def _fileobj_to_gdf(fileobj: io.BytesIO, path_from: str, **kwargs) -> pd.DataFrame:
    """Convert bytes file object into geodataframe.

    Args:
        fileobj (io.BytesIO): Bytes file object.
        path_from (str): Path of loaded data.

    Returns:
        gpd.DataFrame: Data as geodataframe.
    """
    if fnmatch(path_from, "*.geojson"):
        return gpd.GeoDataFrame.from_features(
            json.loads(fileobj.getvalue().decode())["features"]
        )


def _fileobj_to_dict(fileobj: io.BytesIO, path_from: str, **kwargs) -> dict:
    """Convert bytes file object into dictionary.

    Args:
        fileobj (io.BytesIO): Bytes file object.
        path_from (str): Path of loaded data.

    Returns:
        dict: Data as dictionary.
    """
    return json.loads(fileobj.getvalue().decode(), **kwargs)


def _fileobj_to_list(fileobj: io.BytesIO, path_from: str, **kwargs) -> list:
    """Convert bytes file object into list.

    Args:
        fileobj (io.BytesIO): Bytes file object.
        path_from (str): Path of loaded data.

    Returns:
        list: Data as list.
    """
    if fnmatch(path_from, "*.csv"):
        list_data = pd.read_csv(fileobj, **kwargs)["0"].to_list()
    elif fnmatch(path_from, "*.txt"):
        list_data = fileobj.read().decode().splitlines()
    elif fnmatch(path_from, "*.json"):
        list_data = json.loads(fileobj.getvalue().decode())

    return list_data


def _fileobj_to_str(fileobj: io.BytesIO) -> str:
    """Convert bytes file object into string.

    Args:
        fileobj (io.BytesIO): Bytes file object.
        path_from (str): Path of loaded data.

    Returns:
        str: Data as string.
    """
    return fileobj.getvalue().decode("utf-8")


def _fileobj_to_np_array(fileobj: io.BytesIO, path_from: str, **kwargs) -> np.ndarray:
    """Convert bytes file object into numpy array.

    Args:
        fileobj (io.BytesIO): Bytes file object.
        path_from (str): Path of loaded data.

    Returns:
        np.ndarray: Data as numpy array.
    """
    if fnmatch(path_from, "*.csv"):
        np_array_data = np.genfromtxt(fileobj, delimiter=",", **kwargs)
    elif fnmatch(path_from, "*.parquet"):
        np_array_data = pq.read_table(fileobj, **kwargs)["data"].to_numpy()

    return np_array_data


def download_obj(
    bucket: str,
    path_from: str,
    download_as: str = None,
    kwargs_boto: dict = {},
    kwargs_reading: dict = {},
) -> any:
    """Download data to memory from S3 location.

    Args:
        bucket (str): Bucket's name.
        path_from (str): Path to data in S3.
        download_as (str, optional): Type of object downloading. Choose between
        ('dataframe', 'geodataframe', 'dict', 'list', 'str', 'np.array'). Not needed for 'pkl files'.
        kwargs_boto (dict, optional): Dictionary of kwargs for boto3 function 'download_fileobj'.
        kwargs_reading (dict, optional): Dictionary of kwargs for reading data.

    Returns:
        any: Downloaded data.
    """
    if not path_from.endswith(
        tuple(
            [".csv", ".parquet", ".json", ".txt", ".pkl", ".geojson", ".xlsx", ".xlsm"]
        )
    ):
        raise NotImplementedError(
            "This file type is not currently supported for download in memory."
        )
    s3 = boto3.client("s3")
    fileobj = io.BytesIO()
    s3.download_fileobj(bucket, path_from, fileobj, **kwargs_boto)
    fileobj.seek(0)
    if download_as == "dataframe":
        if path_from.endswith(tuple([".csv", ".parquet", ".xlsx", ".xlsm"])):
            return _fileobj_to_df(fileobj, path_from, **kwargs_reading)
        else:
            raise NotImplementedError(
                "Download as dataframe currently supported only "
                "for 'csv','parquet','xlsx' and 'xlsm'."
            )
    elif download_as == "geodataframe":
        if path_from.endswith(tuple([".geojson"])):
            return _fileobj_to_gdf(fileobj, path_from, **kwargs_reading)
        else:
            raise NotImplementedError(
                "Download as geodataframe currently supported only " "for 'geojson'."
            )
    elif download_as == "dict":
        if path_from.endswith(tuple([".json"])):
            return _fileobj_to_dict(fileobj, path_from, **kwargs_reading)
        elif path_from.endswith(tuple([".geojson"])):
            warnings.warn(
                "Please check geojson has a member with the name 'type', the value of the member must be one of the following:"
                "'Point', 'MultiPoint', 'LineString', 'MultiLineString', 'Polygon', 'MultiPolygon', 'GeometryCollection',"
                "'Feature' and 'FeatureCollection'. Else downloaded dictionary will not be valid geojson."
            )
            return _fileobj_to_dict(fileobj, path_from, **kwargs_reading)
        else:
            raise NotImplementedError(
                "Download as dictionary currently supported only "
                "for 'json' and 'geojson'."
            )
    elif download_as == "list":
        if path_from.endswith(tuple([".csv", ".txt", ".json"])):
            return _fileobj_to_list(fileobj, path_from, **kwargs_reading)
        else:
            raise NotImplementedError(
                "Download as list currently supported only "
                "for 'csv', 'txt' and 'json'."
            )
    elif download_as == "str":
        if path_from.endswith(tuple([".txt"])):
            return _fileobj_to_str(fileobj)
        else:
            raise NotImplementedError(
                "Download as string currently supported only " "for 'txt'."
            )
    elif download_as == "np.array":
        if path_from.endswith(tuple([".csv", ".parquet"])):
            return _fileobj_to_np_array(fileobj, path_from, **kwargs_reading)
        else:
            raise NotImplementedError(
                "Download as numpy array currently supported only "
                "for 'csv' and 'parquet'."
            )
    elif not download_as:
        if path_from.endswith(tuple([".pkl"])):
            return pickle.load(fileobj, **kwargs_reading)
        else:
            raise ValueError("'download_as' is required for this file type.")
    else:
        raise ValueError(
            "'download_as' not provided. Choose between ('dataframe', "
            "'dict', 'list', 'str', 'np.array'). Not needed for 'pkl files'.'"
        )


def upload_file(path_from: str, bucket: str, path_to: str, **kwargs):
    """Upload local file from disk to S3 location.

    Args:
        path_from (str): Path to local file.
        bucket (str): Bucket's name.
        path_to (str): Destination path in S3.
    """
    s3 = boto3.client("s3")
    s3.upload_file(path_from, bucket, path_to, kwargs)


def download_file(path_from: str, bucket: str, path_to: str, **kwargs):
    """Download data from S3 to local file on disk.

    Args:
        path_from (str): Path to data in S3
        bucket (str): Buket's name
        path_to (str): Destination path to disk.
    """
    # Create folder if not existing
    file_ops.make_path_if_not_exist(
        file_ops._convert_str_to_pathlib_path(path_to).parents[0]
    )
    s3 = boto3.client("s3")
    s3.download_file(bucket, path_from, path_to, kwargs)
