
import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
from dashboard.figure.histograme import *
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

df_city= make_df_city_trip_depart()
df_trip_time = make_df_trip_date()

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
    dcc.Store(id="drill-state", data={
        "level": "day",
        "city": None,
        "day": None,
        "hour": None
    }),
        # Carré 1
        html.Div(
            html.Iframe(
        id="map",
        srcDoc=create_france_map(cities, trips),
        style={"width": "100%", "height": "100%", "border": "none","backgroundColor": "#111111",
                "border": "3px solid #000000",
                "borderRadius": "5px"}
        )
        ),

        

        # Carré 2
        html.Div(
            dcc.Graph(
        id="histo_day",
        figure=create_histogram(df_trip_time, "day", "number of departures"),
        config={"displayModeBar": False}
    ),
            style={
                "backgroundColor": "#111111",
                "border": "3px solid #000000",
                "borderRadius": "5px"
            }
        ),
        # Carré 3
        html.Div(
        id="table-container",  # 🔥 ICI
        children=create_table_city(df_city),
        style={
        "backgroundColor": "#111111",
        "border": "3px solid #000000",
        "borderRadius": "5px"
        }
        ),
        # Carré 4
        html.Div(
        id="trip-container",  # 🔥 ICI
        children=create_trip_table(make_df_trip_filtre()),
        style={
        "backgroundColor": "#111111",
        "border": "3px solid #000000",
        "borderRadius": "5px"
        }
        ),
    ]
)
# --- Import des callbacks après layout ---
from dashboard.callbacks import callbacks  
if __name__ == "__main__":
    print(cities)
    app.run(debug=True)
    