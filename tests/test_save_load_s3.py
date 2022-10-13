from os import supports_fd
import sys
sys.path.insert(1, "nesta_ds_utils/")
import file_ops
import pytest
import pandas as pd
from moto import mock_s3
from typing import List
import boto3

# def test_get_s3_dir_files():
#     """tests that file_ops method get_s3_dir_files returns type List
#     """
#     assert isinstance(file_ops.get_s3_dir_files('nesta-ds-utils-example'), List)

# def test_load_from_s3():
#     """tests that the load data from load_from_s3 exis exist for all supported formats.
#     """
#     supp_frm = ['txt', 'csv', 'pkl', 'tsv', 'tsv.zip', 'json']
#     assert all([isinstance(file_ops.load_from_s3(
#         'nesta-ds-utils-example', 'test_dir/dummy.' + frm), 
#         (List, str, pd.DataFrame, dict)) for frm in supp_frm])


def test_get_s3_dir_files():
    """tests that file_ops method get_s3_dir_files returns type List
    """
    mock = mock_s3()
    mock.start()
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='mock_bucket')
    
    assert isinstance(file_ops.get_s3_dir_files('mock_bucket'), List)
    mock.stop()

# def test_save_to_s3():
#     """tests that the load data from load_from_s3 exis exist for all supported formats.
#     """
#     supp_frm = ['txt', 'csv', 'pkl', 'json']
#     assert all([isinstance(file_ops.save_to_s3(
#         'nesta-ds-utils-example', 'test_dir/dummy_upload.' + frm), 
#         (List, str, pd.DataFrame, dict)) for frm in supp_frm])
