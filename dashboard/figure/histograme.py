from dash import dash_table
import pandas as pd
import plotly.express as px
from dash import dcc
import plotly.express as px

def create_histogram(df, x, y, selected_x=None):

    fig = px.bar(df, x=x, y=y)

    # couleur par défaut
    colors = ["#3FA2FF"] * len(df)  # bleu

    # highlight sélection
    if selected_x is not None:
        colors = [
            "#FF8C00" if val == selected_x else "#3FA2FF"
            for val in df[x]
        ]

    fig.update_traces(marker_color=colors)

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        margin=dict(l=10, r=10, t=10, b=10),
    )

    return fig