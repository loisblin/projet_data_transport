
import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
from dashboard.figure.table import *
from repositories.city_repository import CityRepository
from repositories.trip_repository import TripRepository
from dashboard.figure.map import *
from dashboard.service.services import *
from dashboard.app_instance import app


app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                background-color: #0b0b0b;
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


cities = get_all_cities()
trips = get_all_trips()

df_city= make_df_city_count_departure()

app.layout = html.Div(
    
    style={
        "display": "grid",
        "gridTemplateColumns": "1.2fr 1.8fr",
        "gridTemplateRows": "2fr 1fr",
        "gap": "10px",
        "height": "100vh",
        "backgroundColor": "#0b0b0b",
        "margin": 0,
        "padding": "15px",
        "boxSizing": "border-box"  # ← IMPORTANT
    },
    children=[
        # STORE GLOBAL
        dcc.Store(
    id="data-store",
    data=df_city.to_dict("records")
    ),
        # Carré 1
        html.Div(
            dcc.Graph(
                id="graph-1",
                figure=create_france_map(cities, trips),
                style={"height": "100%", "width": "100%"},
                config={"displayModeBar": False},
            ),
            style={
                "backgroundColor": "#111111",
                "border": "3px solid #000000",  # bord noir autour
                "borderRadius": "5px"           # coins arrondis optionnels
            }
        ),

        # Carré 2
        html.Div(
            create_city_table(df_city,"table_id1"),
            style={
                "backgroundColor": "#111111",
                "border": "3px solid #000000",
                "borderRadius": "5px"
            }
        ),

        # Carré 3
        html.Div(
            create_city_table(df_city,"table_id2"),
            style={
                "backgroundColor": "#111111",
                "border": "3px solid #000000",
                "borderRadius": "5px"
            }
        ),

        # Carré 4
       html.Div(
    id="selected-city-display",
    children="Aucune ville sélectionnée",
    style={
        "backgroundColor": "#111111",
        "border": "3px solid #000000",
        "borderRadius": "5px",
        "color": "white",
        "fontSize": "30px",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "fontWeight": "bold"
    }
),
    ]
)
# --- Import des callbacks après layout ---
from dashboard.callbacks import callbacks  
if __name__ == "__main__":
    app.run(debug=True)