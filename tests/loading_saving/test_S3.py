import shutil
from pathlib import Path
import pytest
import pandas as pd
import numpy as np
from typing import List
import boto3
from moto import mock_s3
import io
from nesta_ds_utils.loading_saving import S3
from shapely.geometry import Point
import geopandas as gpd

TEST_GEODATAFRAME = gpd.GeoDataFrame({'col1': ['name1', 'name2'], 'geometry': [Point(1, 2), Point(2, 1)]})
TEST_DATAFRAME = pd.DataFrame({"test": [0, 0]})
TEST_DICT_GEO = {"type": "FeatureCollection", 
                 "features": [
                     {"id": "0", "type": "Feature", "properties": {"test": "name1"}, "geometry": {"type": "Point", "coordinates": [0, 0]}}
                     ], 
                     "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::3857"}}
                     }
TEST_DICT = {"test": [0, 0]}
TEST_LIST = [0, "test"]
TEST_STR = "test"
TEST_NP_ARRAY = np.array([0, 0])


@mock_s3
def test_get_bucket_filenames_s3():
    """Test that get_bucket_filenames_s3 returns a list containing dummy.csv."""
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="mybucket")
    mock_client = boto3.client("s3")
    mock_client.upload_fileobj(io.BytesIO(b"Test"), "mybucket", "dummy.csv")
    assert S3.get_bucket_filenames_s3("mybucket", "") == ["dummy.csv"]


@mock_s3
def test_upload_obj_dataframe_csv():
    """Tests that upload_obj does not return an exeption
    uploading dataframe as csv.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_obj(TEST_DATAFRAME, "test-bucket", "dummy.csv")

@mock_s3
def test_upload_obj_dataframe_xlsx():
    """Tests that upload_obj does not return an exeption
    uploading dataframe as xlsx.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_obj(TEST_DATAFRAME, "test-bucket", "dummy.xlsx")

@mock_s3
def test_upload_obj_dataframe_xlsm():
    """Tests that upload_obj does not return an exeption
    uploading dataframe as xlsm.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_obj(TEST_DATAFRAME, "test-bucket", "dummy.xlsm")

@mock_s3
def test_upload_obj_dataframe_geojson():
    """Tests that upload_obj does not return an exeption
    uploading dataframe as geojson.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_obj(TEST_GEODATAFRAME, "test-bucket", "dummy.geojson")

@mock_s3
def test_upload_obj_dataframe_parquet():
    """Tests that upload_obj does not return an exeption
    uploading dataframe as parquet.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_obj(TEST_DATAFRAME, "test-bucket", "dummy.parquet")


@mock_s3
def test_upload_obj_dict_json():
    """Tests that upload_obj does not return an exeption."""
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_obj(TEST_DICT, "test-bucket", "dummy.json")

@mock_s3
def test_upload_obj_dict_json():
    """Tests that upload_obj does not return an exeption."""
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_obj(TEST_DICT_GEO, "test-bucket", "dummy.geojson")


@mock_s3
def test_upload_obj_list_csv():
    """Tests that upload_obj does not return an exeption
    uploading list as csv.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_obj(TEST_LIST, "test-bucket", "dummy.csv")


@mock_s3
def test_upload_obj_list_txt():
    """Tests that upload_obj does not return an exeption
    uploading list as txt.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_obj(TEST_LIST, "test-bucket", "dummy.txt")


@mock_s3
def test_upload_obj_list_json():
    """Tests that upload_obj does not return an exeption
    uploading list as json.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_obj([TEST_DICT, TEST_DICT], "test-bucket", "dummy.json")


@mock_s3
def test_upload_obj_str_txt():
    """Tests that upload_obj does not return an exeption
    uploading string as txt.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_obj(TEST_STR, "test-bucket", "dummy.txt")


@mock_s3
def test_upload_obj_array_csv():
    """Tests that upload_obj does not return an exeption
    uploading numpy array as csv.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_obj(TEST_NP_ARRAY, "test-bucket", "dummy.csv")


@mock_s3
def test_upload_obj_array_parquet():
    """Tests that upload_obj does not return an exeption
    uploading numpy array as parquet.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_obj(TEST_NP_ARRAY, "test-bucket", "dummy.parquet")


@mock_s3
def test_upload_obj_unsup_data():
    """Tests that upload_obj does not return an exeption
    uploading unsupported data as pkl.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_obj(0, "test-bucket", "dummy.pkl")


@mock_s3
def test_download_obj_dataframe_csv():
    """Tests that download_obj returns the correct dataframe
    from csv file.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_file(
        "tests/artifacts/dummy_dataframe.csv", "test-bucket", "dummy.csv"
    )
    assert (
        S3.download_obj("test-bucket", "dummy.csv", download_as="dataframe").test[0]
        == 0
    )

@mock_s3
def test_download_obj_dataframe_xlsx():
    """Tests that download_obj returns the correct dataframe
    from xlsx file.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_file(
        "tests/artifacts/dummy_dataframe.xlsx", "test-bucket", "dummy.xlsx"
    )
    assert (
        S3.download_obj("test-bucket", "dummy.xlsx", download_as="dataframe").test[0]
        == 0
    )

@mock_s3
def test_download_obj_dataframe_xlsm():
    """Tests that download_obj returns the correct dataframe
    from xlsm file.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_file(
        "tests/artifacts/dummy_dataframe.xlsm", "test-bucket", "dummy.xlsm"
    )
    assert (
        S3.download_obj("test-bucket", "dummy.xlsm", download_as="dataframe").test[0]
        == 0
    )

@mock_s3
def test_download_obj_dataframe_geojson():
    """Tests that download_obj returns the correct dataframe
    from geojson file.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_file(
        "tests/artifacts/dummy_dataframe.geojson", "test-bucket", "dummy.geojson"
    )
    assert (
        S3.download_obj("test-bucket", "dummy.geojson", download_as="geodf").geometry[0] 
        == Point(1, 2)
    )

@mock_s3
def test_download_obj_dataframe_parquet():
    """Tests that download_obj returns the correct dataframe
    from parquet file.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_file(
        "tests/artifacts/dummy_dataframe.parquet", "test-bucket", "dummy.parquet"
    )
    assert (
        S3.download_obj("test-bucket", "dummy.parquet", download_as="dataframe").test[0]
        == 0
    )


@mock_s3
def test_download_obj_dict_json():
    """Tests that download_obj returns the correct dictionary
    from json file.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_file(
        "tests/artifacts/dummy_dict.json", "test-bucket", "dummy.json"
    )
    assert (
        S3.download_obj("test-bucket", "dummy.json", download_as="dict")["test"][0] == 0
    )

@mock_s3
def test_download_obj_dict_geojson():
    """Tests that download_obj returns the correct dictionary
    from json file.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_file(
        "tests/artifacts/dummy_dict.geojson", "test-bucket", "dummy.geojson"
    )
    assert (
        S3.download_obj("test-bucket", "dummy.geojson", download_as="dict")["type"]=="FeatureCollection"
    )

@mock_s3
def test_download_obj_list_csv():
    """Tests that download_obj returns the correct list
    from csv file.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_file(
        "tests/artifacts/dummy_list.csv", "test-bucket", "dummy.csv"
    )
    assert S3.download_obj("test-bucket", "dummy.csv", download_as="list")[0] == "0"


@mock_s3
def test_download_obj_list_txt():
    """Tests that download_obj returns the correct list
    from txt file.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_file(
        "tests/artifacts/dummy_list.txt", "test-bucket", "dummy.txt"
    )
    assert S3.download_obj("test-bucket", "dummy.txt", download_as="list")[0] == "0"


@mock_s3
def test_download_obj_list_json():
    """Tests that download_obj returns the correct dataframe
    from json file.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_file(
        "tests/artifacts/dummy_list.json", "test-bucket", "dummy.json"
    )
    assert (
        S3.download_obj("test-bucket", "dummy.json", download_as="list")[0]["test"][0]
        == 0
    )


@mock_s3
def test_download_obj_str_txt():
    """Tests that download_obj returns the correct string
    from txt file.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_file("tests/artifacts/dummy_str.txt", "test-bucket", "dummy.txt")
    assert S3.download_obj("test-bucket", "dummy.txt", download_as="str") == "test\n"


@mock_s3
def test_download_obj_array_csv():
    """Tests that download_obj returns the correct numpy array
    from csv file.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_file(
        "tests/artifacts/dummy_array.csv", "test-bucket", "dummy.csv"
    )
    assert S3.download_obj("test-bucket", "dummy.csv", download_as="np.array")[0] == 0


@mock_s3
def test_download_obj_array_parquet():
    """Tests that download_obj returns the correct numpy array
    from parquet file.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_file(
        "tests/artifacts/dummy_array.parquet", "test-bucket", "dummy.parquet"
    )
    assert (
        S3.download_obj("test-bucket", "dummy.parquet", download_as="np.array")[0] == 0
    )


@mock_s3
def test_download_obj_unsup_data():
    """Tests that download_obj returns the correct integer
    from pkl file.
    """
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_file(
        "tests/artifacts/dummy_unsupp.pkl", "test-bucket", "dummy.pkl"
    )
    assert S3.download_obj("test-bucket", "dummy.pkl") == 0


@mock_s3
def test_download_obj_exeption():
    """Tests that download_obj returns an exception for unsupported file type."""
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    with pytest.raises(Exception):
        S3.download_obj("test-bucket", "dummy.html")


@mock_s3
def test_download_file():
    """Tests that download_file download mock txt file."""
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    mock_client.upload_fileobj(io.BytesIO(b"Test"), "test-bucket", "dummy.csv")
    S3.download_file("dummy.csv", "test-bucket", "tests/temp/dummy.csv")
    with open("tests/temp/dummy.csv", "r") as f:
        text = f.read()
        assert text == "Test"
    shutil.rmtree("tests/temp/")


@mock_s3
def test_upload_file():
    """Tests that upload_file upload mock txt file."""
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    mock_client = boto3.client("s3")
    S3.upload_file("tests/artifacts/dummy.txt", "test-bucket", "dummy.csv")
    Path("tests/temp/").mkdir(parents=True)
    mock_client.download_file("test-bucket", "dummy.csv", "tests/temp/dummy.csv")
    with open("tests/temp/dummy.csv", "r") as f:
        text = f.read()
        assert text == "Test\n"
    shutil.rmtree("tests/temp/")
