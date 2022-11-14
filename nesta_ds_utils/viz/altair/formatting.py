"""
Module containing utils for styling and exporting figures using Altair.
"""
import altair as alt
import os
from typing import Union, List, Type
import warnings
from matplotlib import font_manager
from pathlib import Path
import yaml


def _find_averta() -> str:
    """Search for averta font, otherwise return 'Helvetica' and raise a warning.

    Returns:
        str: Return averta installation name, if found. Return 'Helvetica' otherwise.
    """
    font = False
    for font_path in font_manager.findSystemFonts(fontext="ttf"):
        if "Averta" in font_path:
            font = "Averta"
            break
    if not font:
        warnings.warn("Averta font could not be located. Using 'Helvetica' instead")
        font = "Helvetica"
    return font


def _load_nesta_theme() -> dict:
    """Define Nesta's styling theme using format expected by altair."""
    font = _find_averta()
    with open("nesta_ds_utils/viz/themes/nesta_theme_" + font + ".yaml", "r") as stream:
        config = yaml.safe_load(stream)
    return config


def setup_theme(theme_name="nesta"):
    """Enable a theme for an altair figure. Currently only supports nesta theme.

    Args:
        theme_name (str, optional): Theme to load. Defaults to 'nesta'. Currently only acceptable value is 'nesta'.
    """
    if theme_name == "nesta":
        alt.themes.register("nesta_theme", _load_nesta_theme)
        alt.themes.enable("nesta_theme")
    else:
        warnings.warn("Invalid theme name. Currently only supports nesta theme.")
