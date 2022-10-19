import shutil
import os
from pathlib import Path
import sys
import pytest
import pandas as pd
from typing import List
import boto3
from moto import mock_s3
import io

from nesta_ds_utils import file_ops


@pytest.fixture
def test_output_path():
    """Generates pathlib.Path to dump intermediate test data.

    Yields:
        Output path to dump intermetiate test data.
    """
    test_output_path = file_ops._convert_str_to_pathlib_path("tests/temp/")
    file_ops.make_path_if_not_exist(test_output_path)
    yield test_output_path
    shutil.rmtree("tests/temp/")


def test_convert_str_to_pathlib_path(test_output_path: Path):
    """Tests that file_ops method convert_str_to_pathlib_path.
        returns type patlib.Path.

    Args:
        test_output_path (pathlib.Path): output path to dump intermetiate test data
    """
    assert isinstance(test_output_path, Path)


def test_path_exists(test_output_path: Path):
    """Tests that the path generated by file_ops method
        make_path_if_not_exist exists.

    Args:
        test_output_path (pathlib.Path): Output path to dump intermetiate test data.
    """
    assert test_output_path.exists()


def test_extract_zip_to_output_path(test_output_path: Path):
    """Tests that the file_ops method extractall dumped a
        text file to an output path and that text file could be read.

    Args:
        test_output_path (pathlib.Path): Output path to dump intermetiate test data.
    """
    file_ops.extractall(
        "tests/artifacts/dummy_zip.zip", test_output_path, delete_zip=False
    )

    with open("tests/temp/dummy_text_in_zip.txt", "r") as f:
        text = f.read()
        assert text == "'Hello World'"


def test_extract_zip_no_output_path():
    """Tests that the file_ops method extractall dumped a
    text file to the directory of the zip file.
    """
    file_ops.extractall("tests/artifacts/dummy_zip.zip", delete_zip=False)

    with open("tests/artifacts/dummy_text_in_zip.txt", "r") as f:
        text = f.read()
        assert text == "'Hello World'"

    os.remove("tests/artifacts/dummy_text_in_zip.txt")


def test_zip_not_deleted():
    """Tests that the zip file was not deleted when extractall
    was called without a delete_zip flag.
    """
    assert file_ops._convert_str_to_pathlib_path(
        "tests/artifacts/dummy_zip.zip"
    ).exists()


@mock_s3
def test_get_bucket_filenames_s3():
    """Test that get_dir_files_s3 returns a List."""
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="mybucket")
    assert isinstance(file_ops.get_bucket_filenames_s3("mybucket", ""), List)


@mock_s3
def test_upload_s3_exception():
    """Tests that upload_data_s3 rasies an Exception for unsupported data."""
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="mybucket")
    with pytest.raises(Exception):
        file_ops.upload_data_s3(0, "mybucket", "dummy.csv")


@mock_s3
def test_download_s3_fileobj():
    """Tests that download_data_s3 returns a bytes file object."""
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    s3 = boto3.client("s3")
    s3.upload_fileobj(io.BytesIO(b"Test"), "test-bucket", "dummy.csv")
    assert isinstance(file_ops.download_data_s3("test-bucket", "dummy.csv"), io.BytesIO)


@mock_s3
def test_download_s3_dataframe():
    """Tests that download_data_s3 returns a bytes file object."""
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-bucket")
    s3 = boto3.client("s3")
    s3.upload_fileobj(io.BytesIO(b"Test"), "test-bucket", "dummy.csv")
    assert isinstance(
        file_ops.download_data_s3("test-bucket", "dummy.csv", asDataFrame=True),
        pd.DataFrame,
    )
