"""
Utils for styling and exporting figure using Altair.
"""

import altair_saver as alt_saver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver
import os
from typing import Iterator
from pathlib import Path
from nesta_ds_utils import file_ops


def google_chrome_driver_setup() -> WebDriver:
    """Set up the driver to save figures"""
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver


def create_paths(path: os.PathLike, filetypes: Iterator[list]):
    """Checks if the paths exist and if not creates them.

    Args:
        path (os.PathLike: Path to save figure.
        filetypes (Iterator[list]): List of file types to save figure.
    """
    for filetype in filetypes:
        os.makedirs(f"{path}/{filetype}", exist_ok=True)


def save_png(fig, path: os.PathLike, name: str, driver: WebDriver):
    """Save altair chart as a  raster png file.

    Args:
        fig: Altair chart.
        path (os.PathLike): Path where to save the figure.
        name (str): Name of figure.
        driver (WebDriver): webdriver to use for saving.
    """
    alt_saver.save(
        fig,
        f"{path}/png/{name}.png",
        method="selenium",
        webdriver=driver,
        scale_factor=5,
    )


def save_html(fig, path: os.PathLike, name: str):
    """Save altair chart as a html file.

    Args:
        fig: Altair chart.
        path (os.PathLike): Path where to save the figure.
        name (str): Name of figure.
    """
    fig.save(f"{path}/html/{name}.html")


def save_svg(fig, path: os.PathLike, name: str, driver: WebDriver):
    """Save altair chart as vector svg file.

    Args:
        fig: Altair chart.
        path (os.PathLike): Path where to save the figure.
        name (str): Name of figure.
        driver (WebDriver): webdriver to use for saving.
    """
    alt_saver.save(fig, f"{path}/svg/{name}.svg", method="selenium", webdriver=driver)


def save(
    fig,
    name: str,
    path: os.PathLike = None,
    driver: WebDriver = None,
    filetypes: Iterator[list] = None,
):
    """Saves an altair figure in multiple formats (png, html and svg files).

    Args:
        fig: Altair chart.
        name (str): Name to save the figure.
        path (os.PathLike, optional): Path where to save the figure. Defaults to 'None'.
        driver (WebDriver, optional): Webdriver to use. Defaults to 'None'.
        filetypes (Iterator[list], optional): List of filetypes, eg: ['png', 'svg', 'html']. Defaults to None.
    """
    # Default values
    path = (
        Path(f"figures")
        if path is None
        else file_ops._convert_str_to_pathlib_path(path)
    )
    driver = google_chrome_driver_setup() if driver is None else driver
    filetypes = ["png", "svg", "html"] if filetypes is None else filetypes
    # Check paths
    create_paths(path, filetypes)
    # Export figures
    if "png" in filetypes:
        save_png(fig, path, name, driver)
    if "html" in filetypes:
        save_html(fig, path, name)
    if "svg" in filetypes:
        save_svg(fig, path, name, driver)
