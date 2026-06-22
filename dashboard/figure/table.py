from dash import dash_table
import pandas as pd
from dash import html

def create_table_city(df,selected_city=None):

    # HEADER
    header = html.Div(
        [
            html.Div(col, style={
                "flex": 1,
                "fontWeight": "bold",
                "color": "white"
            })
            for col in df.columns
        ],
        style={
            "display": "flex",
            "padding": "10px",
            "borderBottom": "2px solid #333",
            "backgroundColor": "#1a1a1a"
        }
    )

    # ROWS
    rows = []
    for i in range(len(df)):
        city = str(df.iloc[i]["Departure_city"])

        bg_color = "#2a6df4" if city == selected_city else "#111111"

        row = html.Div(
            id={"type": "row", "city": city},
            n_clicks=0,
            children=[
                html.Div(str(df.iloc[i][col]), style={"flex": 1, "color": "white"})
                for col in df.columns
            ],
            style={
                "display": "flex",
                "padding": "10px",
                "borderBottom": "1px solid #222",
                "backgroundColor": bg_color,  # 🔥 ICI le highlight
                "cursor": "pointer"
            }
        )
        rows.append(row)

    return html.Div([header] + rows)
def create_trip_table(df):
    # HEADER
    header = html.Div(
        [
            html.Div(col, style={
                "flex": 1,
                "fontWeight": "bold",
                "color": "white"
            })
            for col in df.columns
        ],
        style={
            "display": "flex",
            "padding": "10px",
            "borderBottom": "2px solid #333",
            "backgroundColor": "#1a1a1a"
        }
    )

    # ROWS
    rows = []
    for i in range(len(df)):
        row = html.Div(
            id={"type": "row", "id": str(i)},  # 🔥 important pour les callbacks
            children=[
                html.Div(str(df.iloc[i][col]), style={"flex": 1, "color": "white"})
                for col in df.columns
            ],
            style={
                "display": "flex",
                "padding": "10px",
                "borderBottom": "1px solid #222",
                "backgroundColor": "#111111",
                "cursor": "pointer"
            }
        )
        rows.append(row)

    return html.Div([header] + rows)