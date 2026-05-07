
import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
from dashboard.figure.histograme import *
from dashboard.figure.table import *
from dashboard.figure.map import *

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
        dcc.Store(id="store-map"),
        dcc.Store(id="store-histo"),
        dcc.Store(id="store-table"),
        dcc.Store(id="store-cities"),
        dcc.Store(id="store-init", data = False),
        dcc.Store(id="store-state-time", data={
        "granularity": "week",
        
        "day": None,
        "hour": None
    }),
        dcc.Store(id="store_state_filtre", data = {
            "city": None,
            "metric": "price"


        }),
        # Carré 1
        html.Div(
        html.Iframe(
            id="map",
            style={
                "width": "100%",
                "height": "100%",
                "border": "none",
                "backgroundColor": "#111111",
                "border": "3px solid #000000",
                "borderRadius": "5px"
                }
            )
        ),

        

        # Carré 2
        html.Div(
                dcc.Graph(
                    id="histo",
                    
                    config={"displayModeBar": False}
                ),
                id="histo-container",
                n_clicks=0,
                style={
                    "backgroundColor": "#111111",
                    "border": "3px solid #000000",
                    "borderRadius": "5px"
                }
        ),
        html.Div(
            id="table-container",
            style={
                "backgroundColor": "#111111",
                "border": "3px solid #000000",
                "borderRadius": "5px"
            }
        )
                
    ]
)
# --- Import des callbacks après layout ---
from dashboard.callbacks import callbacks  

if __name__ == "__main__":
   
    app.run(debug=True)
  
   