from dash import dash_table
import pandas as pd
from dash import html
def create_city_table(df,id):
    table = dash_table.DataTable(
        id=id,
        columns=[
        {
        "name": i,
        "id": i,
        "type": "numeric" if df[i].dtype != "object" else "text"
         }
        for i in df.columns
        ],
        data=df.to_dict('records'),
        selected_rows=[],  
        row_selectable="single",
        page_size=10,
        sort_action="native",
        filter_action="native",
        css=[
            {
                "selector": "td:focus",
                "rule": "outline: none; background-color: transparent !important;"
            },
            {
                "selector": "td:active",
                "rule": "background-color: transparent !important;"
            },
            {
                "selector": "td.cell--selected",
                "rule": "background-color: transparent !important;"
            }
        ],

        # style des cellules
        style_cell={
            'textAlign': 'center',
            'padding': '10px',
            'fontFamily': 'Arial',
            'fontSize': '14px'
        },

        # style header
        style_header={
            'backgroundColor': '#2c3e50',
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center'
        },

        # lignes alternées
        style_data_conditional=[
    {
    "if": {"state": "active"},
    "backgroundColor": "transparent",
    "border": "none",
},
{
    "if": {"state": "selected"},
    "backgroundColor": "transparent",
    "border": "none",
},
],

        # bordure du tableau
        style_table={
            'border': '1px solid #ddd',
            'borderRadius': '10px',
            'overflow': 'hidden',
            
        }
    )

    return table
def create_table_city(df):

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
            id={"type": "row", "city": str(df.iloc[i]["cities"])},  # 🔥 important pour les callbacks
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
def create_trip_table(trips_filtered,id):
    """
    Retourne un DataTable des trajets filtrés.
    """
    table = dash_table.DataTable(
        id=id,
        columns=[{"name": i, "id": i} for i in ["Départ","Arrivée","Heure","Durée"]],
        data=trips_filtered,
        style_cell={'textAlign': 'center'},
        style_header={'fontWeight': 'bold'}
    )
    return table