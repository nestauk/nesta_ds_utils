import sys
sys.path.insert(1, "nesta_ds_utils/")
import file_ops
import pytest
import pandas as pd
from typing import List
import boto3
from moto import mock_s3
import io

@mock_s3
def test_get_dir_files_s3():
    """tests that get_dir_files_s3 returns a List 
    """

    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='mybucket')
    assert isinstance(file_ops.get_dir_files_s3('mybucket',''), List)

@mock_s3
def test_upload_s3_exception():
    """tests that upload_data_s3 rasies an Exception for unsupported data
    """

    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='mybucket')
    with pytest.raises(Exception):
        file_ops.upload_data_s3(0,'mybucket','dummy.csv')

@mock_s3
def test_download_s3_fileobj():
    """tests that download_data_s3 returns a bytes file object
    """

    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='test-bucket')
    s3 = boto3.client('s3')
    s3.upload_fileobj(io.BytesIO(b"Test"), 'test-bucket', 'dummy.csv')
    assert isinstance(file_ops.download_data_s3('test-bucket','dummy.csv'), io.BytesIO)

@mock_s3
def test_download_s3_dataframe():
    """tests that download_data_s3 returns a bytes file object
    """

    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='test-bucket')
    s3 = boto3.client('s3')
    s3.upload_fileobj(io.BytesIO(b"Test"), 'test-bucket', 'dummy.csv')
    assert isinstance(
        file_ops.download_data_s3('test-bucket','dummy.csv', asDataFrame=True),
        pd.DataFrame)
