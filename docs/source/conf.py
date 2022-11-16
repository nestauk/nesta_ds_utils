import os
import sys

sys.path.insert(1, "../../nesta_ds_utils")
sys.path.insert(1, "../../tests")
import test_file_ops, data_manipulation, test_data_manipulation, plotting, test_plotting
from nesta_ds_utils.loading_saving import file_ops, S3

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "nesta_ds_utils"
copyright = "2022, DAP"
author = "DAP"
release = "0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "nature"
html_static_path = ["_static"]
html_logo = "_static/Nesta_Logo_Blue_RGB.png"
# html_theme_options = {
#   "headingcolor": "#0000FF"
#    "bodyfont": "averta",
#    "headfont": "averta",
#    "sidebarbgcolor": "#0000FF",
#    "footerbgcolor": "#9A1BBE",
#    "textcolor": "#0F294A",
#    "linkcolor": "0F294A",
#    "headtextcolor": "#0F294A",
#    "sidebarwidth": 400,
# }
