from typing import Any, Dict, List, Optional, Tuple, Union

import altair as alt
import pandas as pd

from .utils import Chart


def lineplot(
    df,
    x: str,
    y: str,
    column: Optional[str] = None,
    column_title: str = "",
    column_label_orient: str = "top",
    column_title_orient: str = "bottom",
    aggregate: Optional[str] = "mean",
    points: bool = True,
    lines: bool = True,
    errorbars: bool = True,
    error_extent: str = "stdev",
    limits: Optional[List[float]] = None,
    independent_x: bool = True,
    spacing: int = 5,
    color: Optional[Union[str, alt.Color]] = None,
    height: Optional[int] = None,
    width: Optional[int] = None,
) -> Chart:
    """Produces lineplot with optional errorbars and facets

    Args:
        df: Dataframe
        x: Shorthand for x
        y: Shorthand for y
        column: Shorthand for columns (optional) which are faceted
        column_title: Title text for columns displayed 
        column_label_orient: Orientation of column labels
        column_title_orient: Orientation of column title
        aggregate: Aggregation function for y values
        points: Whether to show points
        lines: Whether to show lines
        errorbars: Whether to show errorbars
        error_extent: Extent of errorbars, e.g., stdev or stderr
        limits: Limits for y-axis
        independent_x: Whether x-axes are be independent
        spacing: Spacing between facets
        color: Colorscale
        height: Height of plot in facet
        width: Width of plot in facet

    Returns:
        Chart
    """
    if color is None:
        color_kwarg = {}
    else:
        color_kwarg = {"color": color}

    if limits is not None:
        y_scale = alt.Scale(zero=False, domain=limits)
    else:
        y_scale = alt.Scale(zero=False)

    lines_layer = (
        alt.Chart()
        .mark_line()
        .encode(
            x=alt.X(x, title=""),
            y=alt.Y(y, scale=y_scale, aggregate=aggregate),
            **color_kwarg
        )
    )

    points_layer = (
        alt.Chart()
        .mark_point(filled=True)
        .encode(
            x=alt.X(x, title=""),
            y=alt.Y(y, scale=y_scale, aggregate=aggregate),
            **color_kwarg
        )
    )

    errorbars_layer = (
        alt.Chart()
        .mark_errorbar(extent=error_extent)
        .encode(
            x=alt.X(x, title=""), y=alt.Y(y, scale=y_scale), **color_kwarg
        )
    )

    layers = []
    if lines:
        layers.append(lines_layer)
    if points:
        layers.append(points_layer)
    if errorbars:
        layers.append(errorbars_layer)

    chart = alt.layer(*layers, data=df)

    if height is not None:
        chart = chart.properties(height=height)

    if width is not None:
        chart = chart.properties(width=width)

    if column is not None:
        chart = chart.facet(
            column=alt.Column(
                column, title=column_title, header=alt.Header(labels=True)
            ),
            spacing=spacing,
        )
        chart = chart.configure_header(titleOrient=column_title_orient, labelOrient=column_label_orient)

        if independent_x:
            chart = chart.resolve_scale(x='independent')

    return chart
