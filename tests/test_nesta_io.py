import unittest
import zipfile
import shutil
import pathlib
import sys
sys.path.insert(1,'../nesta_ds_utils/')
import nesta_io

class TestNestaIO(unittest.TestCase):
    """Unittest class associated with nesta_io methods
    
    To run all tests: python -m unittest test_nesta_io.TestNestaIO

    To run specific tests: python -m unittest test_nesta_io.TestNestaIO.[test_method]
    (ex: python -m unittest test_nesta_io.TestNestaIO.test_zip_extraction)
    
    """

    def setUp(self) -> None:
        self.pathlibPath = nesta_io.convert_str_to_pathlib_path('temp/zipContents')
        nesta_io.make_path_if_not_exist(self.pathlibPath)
        nesta_io.extractall('artifacts/dummy_zip.zip',self.pathlibPath)
        

    def test_convert_str_to_pathlib_path(self):
        self.assertIsInstance(self.pathlibPath,pathlib.Path)
    
    def test_path_exists(self):
        self.assertTrue(self.pathlibPath.exists())
    
    def test_zip_extraction(self):
        with open('temp/zipContents/dummy_text_in_zip.txt','r') as f:
            text = f.read()
            self.assertEqual(text,"'Hello World'")
    
    def tearDown(self):
        shutil.rmtree('temp/')


if __name__ == '__main__':
    unittest.main()