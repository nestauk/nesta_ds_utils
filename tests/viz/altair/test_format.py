from nesta_ds_utils.viz.altair import formatting
import altair as alt
import pytest
import pandas as pd


def test_nesta_theme_activation():
    """Test that the Nesta's theme is activates by checking the first color of
    the palette is Nesta's blue."""
    alt.themes.enable("default")
    fig = alt.Chart(pd.DataFrame()).mark_bar()
    formatting.setup_theme()
    assert fig.to_dict()["config"]["range"]["category"][0] == "#0000FF"
