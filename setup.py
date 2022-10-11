#!/usr/bin/env python
 
from setuptools import setup

if __name__ == "__main__":
      setup({extras_require={
      'dev': [
      "Sphinx==5.2.3",
      "sphinxcontrib-applehelp==1.0.2",
      "sphinxcontrib-devhelp==1.0.2",
      "sphinxcontrib-htmlhelp==2.0.0",
      "sphinxcontrib-jsmath==1.0.1",
      "sphinxcontrib-qthelp==1.0.3",
      "sphinxcontrib-serializinghtml==1.1.5",
      "pytest==7.1.3"
        ]
    })