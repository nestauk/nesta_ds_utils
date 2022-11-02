import shutil
from pathlib import Path
from nesta_ds_utils import plotting
import pandas as pd
import altair as alt
import pytest


def test_save__png_altair():
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
