import shutil
from pathlib import Path
from nesta_ds_utils import plotting
import pandas as pd
import altair as alt
import pytest


def test_save_altair():
    """Test that that figures saved exist."""
    fig = alt.Chart(pd.DataFrame()).mark_bar()
    path = "tests/temp/"
    plotting.save(fig, "test_fig", path)
    assert all(
        [
            Path(f"tests/temp/png/test_fig.png").exists(),
            Path(f"tests/temp/svg/test_fig.svg").exists(),
            Path(f"tests/temp/html/test_fig.html").exists(),
        ]
    )
    shutil.rmtree("tests/temp/")


def test_save_altair():
    """Test that that figures saved exist."""
    fig = alt.Chart(pd.DataFrame()).mark_bar()
    path = "tests/temp/"
    plotting.save(fig, "test_fig", path, filetypes="html")
    assert Path(f"tests/temp/html/test_fig.html").exists()
    shutil.rmtree("tests/temp/")


def test_save_altair_exception():
    """Test that function returns exception for unsupported formats."""
    fig = alt.Chart(pd.DataFrame()).mark_bar()
    path = "tests/temp/"
    with pytest.raises(Exception):
        plotting.save(fig, "test_fig", path, filetypes="")
