"""
Module containing utils for styling and exporting figures using Altair.
"""

import altair_saver as alt_saver
from altair.vegalite.v4.api import Chart
import altair as alt
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
import os
from typing import Union, List, Type
import warnings
from matplotlib import font_manager
from pathlib import Path
from nesta_ds_utils.loading_saving import file_ops
import yaml


def _google_chrome_driver_setup() -> WebDriver:
    """Set up the driver to save figures"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chrome_options
    )
    return driver


def _save_png(
    fig: Chart, path: os.PathLike, name: str, scale_factor: int, driver: WebDriver
):
    """Save altair chart as a  raster png file.

    Args:
        fig: Altair chart.
        path (os.PathLike): Path where to save the figure.
        name (str): Name of figure.
        scale_factor (int): Saving scale factor.
        driver (WebDriver): webdriver to use for saving.
    """
    alt_saver.save(
        fig,
        f"{path}/{name}.png",
        method="selenium",
        webdriver=driver,
        scale_factor=scale_factor,
    )


def _save_html(fig: Chart, path: os.PathLike, name: str, scale_factor: int):
    """Save altair chart as a html file.

    Args:
        fig: Altair chart.
        path (os.PathLike): Path where to save the figure.
        name (str): Name of figure.
        scale_factor (int): Saving scale factor.
    """
    fig.save(f"{path}/{name}.html", scale_factor=scale_factor)


def _save_svg(
    fig: Chart, path: os.PathLike, name: str, scale_factor: int, driver: WebDriver
):
    """Save altair chart as vector svg file.

    Args:
        fig: Altair chart.
        path (os.PathLike): Path where to save the figure.
        name (str): Name of figure.
        scale_factor (int): Saving scale factor.
        driver (WebDriver): webdriver to use for saving.
    """
    alt_saver.save(
        fig,
        f"{path}/{name}.svg",
        method="selenium",
        scale_factor=scale_factor,
        webdriver=driver,
    )


def save(
    fig: Chart,
    name: str,
    path: Union[os.PathLike, str] = "figures",
    driver: WebDriver = None,
    save_png: bool = True,
    save_html: bool = False,
    save_svg: bool = False,
    scale_factor: int = 5,
):
    """Saves an altair figure in multiple formats (png, html and svg files).

    Args:
        fig: Altair chart.
        name (str): Name to save the figure.
        path (Union[os.PathLike, str], optional): Path where to save the figure. Defaults to 'figures'.
        driver (WebDriver, optional): Webdriver to use. Defaults to 'webdriver.Chrome'.
        save_png (bool, optional): Option to save figure as 'png'. Default to True.
        save_html (bool, optional): Option to save figure as 'html'. Default to False.
        save_svg (bool, optional): Option to save figure as 'svg'. Default to False.
        scale_factor (int, optional): Saving scale factor. Default to 5.
    """
    path = file_ops._convert_str_to_pathlib_path(path)

    if not any([save_png, save_html, save_svg]):
        raise Exception(
            "At least one format needs to be selected. Example: save(.., save_png=True)."
        )

    if save_png or save_svg:
        driver = _google_chrome_driver_setup() if driver is None else driver

    file_ops.make_path_if_not_exist(path)
    # Export figures
    if save_png:
        _save_png(fig, path, name, scale_factor, driver)

    if save_html:
        _save_html(fig, path, name, scale_factor)

    if save_svg:
        _save_svg(fig, path, name, scale_factor, driver)


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
    with open("nesta_ds_utils/themes/nesta_theme_" + font + ".yaml", "r") as stream:
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
