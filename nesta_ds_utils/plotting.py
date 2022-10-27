"""
Module containing utils for styling and exporting figures using Altair.
"""

import altair_saver as alt_saver
from altair.vegalite.v4.api import Chart
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
import os
from typing import Union, List, Type
from pathlib import Path
from nesta_ds_utils import file_ops


def _google_chrome_driver_setup() -> WebDriver:
    """Set up the driver to save figures"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chrome_options
    )
    return driver


def _save_png(fig: Chart, path: os.PathLike, name: str, driver: WebDriver):
    """Save altair chart as a  raster png file.

    Args:
        fig: Altair chart.
        path (os.PathLike): Path where to save the figure.
        name (str): Name of figure.
        driver (WebDriver): webdriver to use for saving.
    """
    alt_saver.save(
        fig,
        f"{path}/{name}.png",
        method="selenium",
        webdriver=driver,
        scale_factor=5,
    )


def _save_html(fig, path: os.PathLike, name: str):
    """Save altair chart as a html file.

    Args:
        fig: Altair chart.
        path (os.PathLike): Path where to save the figure.
        name (str): Name of figure.
    """
    fig.save(f"{path}/{name}.html")


def _save_svg(fig, path: os.PathLike, name: str, driver: WebDriver):
    """Save altair chart as vector svg file.

    Args:
        fig: Altair chart.
        path (os.PathLike): Path where to save the figure.
        name (str): Name of figure.
        driver (WebDriver): webdriver to use for saving.
    """
    alt_saver.save(fig, f"{path}/{name}.svg", method="selenium", webdriver=driver)


def save(
    fig,
    name: str,
    path: Union[os.PathLike, str] = "figures",
    driver: WebDriver = None,
    save_png: bool = True,
    save_html: bool = False,
    save_svg: bool = False,
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
    """
    path = file_ops._convert_str_to_pathlib_path(path)

    if not any([save_png, save_html, save_svg]):
        raise Exception(
            "At least one format needs to be selected. Example: save(.., save_png=True)."
        )

    if save_png or save_svg:
        driver = _google_chrome_driver_setup() if driver is None else driver

    # Export figures
    if save_png:
        file_ops.make_path_if_not_exist(path)
        _save_png(fig, path, name, driver)

    if save_html:
        file_ops.make_path_if_not_exist(path)
        _save_html(fig, path, name)

    if save_svg:
        file_ops.make_path_if_not_exist(path)
        _save_svg(fig, path, name, driver)
