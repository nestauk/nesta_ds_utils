import shutil
from pathlib import Path
from nesta_ds_utils.viz.altair import saving
from selenium.webdriver.chromium.webdriver import ChromiumDriver
import pandas as pd
import altair as alt
import pytest


def test_save_png_altair():
    """Test that that figures saved as png exist."""
    fig = alt.Chart(pd.DataFrame()).mark_bar()
    path = "tests/temp/"
    saving.save(fig, "test_fig", path)
    assert Path(f"tests/temp/test_fig.png").exists()
    shutil.rmtree("tests/temp/")


def test_save_html_altair():
    """Test that that figures saved as html exist."""
    fig = alt.Chart(pd.DataFrame()).mark_bar()
    path = "tests/temp/"
    saving.save(fig, "test_fig", path, save_png=False, save_html=True)
    assert Path(f"tests/temp/test_fig.html").exists()
    shutil.rmtree("tests/temp/")


def test_save_svg_altair():
    """Test that that figures saved as svg exist."""
    fig = alt.Chart(pd.DataFrame()).mark_bar()
    path = "tests/temp/"
    saving.save(fig, "test_fig", path, save_png=False, save_svg=True)
    assert Path(f"tests/temp/test_fig.svg").exists()
    shutil.rmtree("tests/temp/")


def test_save_altair_exception():
    """Test that function returns exception no format is selected."""
    fig = alt.Chart(pd.DataFrame()).mark_bar()
    path = "tests/temp/"
    with pytest.raises(Exception):
        saving.save(
            fig, "test_fig", path, save_png=False, save_html=False, save_svg=False
        )


def test_webdriver():
    """Test that Chrome WebDriver is created by default is a ChromiumDriver, and context manager stops the webdriver."""
    driver = saving._google_chrome_driver_setup()
    assert isinstance(driver, ChromiumDriver)

    with saving.webdriver_context(driver) as some_driver:
        # No actions needed here,
        # just testing that the context manager calls .quit() on driver to terminate.
        pass

    # If subprocess not terminated, .poll() returns None
    # https://docs.python.org/3/library/subprocess.html#subprocess.Popen.returncode
    assert driver.service.process.poll() is not None
