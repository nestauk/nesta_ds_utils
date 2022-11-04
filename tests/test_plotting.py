import shutil
from pathlib import Path
from nesta_ds_utils import plotting
import pandas as pd
import altair as alt
import pytest


def test_save_png_altair():
    """Test that that figures saved as png exist."""
    fig = alt.Chart(pd.DataFrame()).mark_bar()
    path = "tests/temp/"
    plotting.save(fig, "test_fig", path)
    assert Path(f"tests/temp/test_fig.png").exists()
    shutil.rmtree("tests/temp/")


def test_save_html_altair():
    """Test that that figures saved as html exist."""
    fig = alt.Chart(pd.DataFrame()).mark_bar()
    path = "tests/temp/"
    plotting.save(fig, "test_fig", path, save_png=False, save_html=True)
    assert Path(f"tests/temp/test_fig.html").exists()
    shutil.rmtree("tests/temp/")


def test_save_svg_altair():
    """Test that that figures saved as svg exist."""
    fig = alt.Chart(pd.DataFrame()).mark_bar()
    path = "tests/temp/"
    plotting.save(fig, "test_fig", path, save_png=False, save_svg=True)
    assert Path(f"tests/temp/test_fig.svg").exists()
    shutil.rmtree("tests/temp/")


def test_save_altair_exception():
    """Test that function returns exception no format is selected."""
    fig = alt.Chart(pd.DataFrame()).mark_bar()
    path = "tests/temp/"
    with pytest.raises(Exception):
        plotting.save(
            fig, "test_fig", path, save_png=False, save_html=False, save_svg=False
        )


def test_nesta_theme_activation():
    """Test that the Nesta's theme is activates by checking the first color of
    the palette is Nesta's blue."""
    fig = alt.Chart(pd.DataFrame()).mark_bar()
    plotting.setup_theme()
    assert fig.to_dict()["config"]["range"]["category"][0] == "#0000FF"
