import unittest
import zipfile
import shutil
from pathlib import Path
import sys
sys.path.insert(1, "../nesta_ds_utils/")
import nesta_io

class TestNestaIO(unittest.TestCase):
    """Unittest class associated with nesta_io methods
    
    To run all tests: python -m unittest test_nesta_io.TestNestaIO

    To run specific tests: python -m unittest test_nesta_io.TestNestaIO.[test_method]
    (ex: python -m unittest test_nesta_io.TestNestaIO.test_zip_extraction)
    
    """
    def setUp(self):
        self.outPath = nesta_io._convert_str_to_pathlib_path("temp/zipContents")
        self.zipPath = nesta_io._convert_str_to_pathlib_path("artifacts/dummy_zip.zip")
        nesta_io.make_path_if_not_exist(self.outPath)
        nesta_io.extractall("artifacts/dummy_zip.zip", self.outPath, delete_zip = False)
        nesta_io.extractall("artifacts/dummy_zip.zip", delete_zip = False)
        
    def test_convert_str_to_pathlib_path(self):
        self.assertIsInstance(self.outPath,Path)
    
    def test_path_exists(self):
        self.assertTrue(self.outPath.exists())
    
    def test_zip_extraction_with_outpath(self):
        with open("temp/zipContents/dummy_text_in_zip.txt", "r") as f:
            text = f.read()
            self.assertEqual(text, "'Hello World'")
    
    def test_zip_extraction_no_outpath(self):
        with open("artifacts/dummy_text_in_zip.txt", "r") as f:
            text = f.read()
            self.assertEqual(text, "'Hello World'")
    
    def test_zip_not_deleted(self):
        self.assertTrue(self.zipPath.exists())
    
    def tearDown(self):
        shutil.rmtree("temp/")


if __name__ == "__main__":
    unittest.main()