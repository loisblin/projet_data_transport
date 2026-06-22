
import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
from dashboard.figure.histograme import *
from dashboard.figure.table import *
from dashboard.figure.map import *

from dashboard.app_instance import app
from dashboard.components.filter import create_filters





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
init_state_filter = {
    "city": None,
    "histo_metric": "price",
    "map_metric": "price"
}

init_state_time = {
    "granularity": "week",
    "day": None,
    "hour": None
}


app.layout = html.Div(

    style={
        "display": "grid",
        "gridTemplateColumns": "1.4fr 1fr",
        "gap": "10px",
        "height": "100vh",
        "backgroundColor": "#0b0b0b",
        "margin": 0,
        "padding": "15px",
        "boxSizing": "border-box",
        "overflow": "hidden"
    },

    children=[

        # =========================
        # STORES
        # =========================

        dcc.Store(id="store-map"),
        dcc.Store(id="store-histo"),
        dcc.Store(id="store-table"),
        dcc.Store(id="store-cities"),

        dcc.Store(id="store-init", data=False),

        dcc.Store(
            id="store-state-time",
            data= init_state_time
        ),

        dcc.Store(
            id="store-state-filtre",
            data= init_state_filter
        ),

        # ==================================================
        # LEFT COLUMN (MAP + FILTERS)
        # ==================================================

        html.Div(

            style={
                "display": "grid",
                "gridTemplateRows": "4fr 1fr",
                "gap": "10px",
                "height": "100%",
                "minHeight": 0
            },

            children=[

                # MAP
                html.Div(

                    html.Iframe(
                        id="map",
                        style={
                            "width": "100%",
                            "height": "100%",
                            "border": "none"
                        }
                    ),

                    style={
                        "backgroundColor": "#111111",
                        "border": "3px solid #000000",
                        "borderRadius": "5px",
                        "overflow": "hidden",
                        "minHeight": 0
                    }
                ),



                # FILTERS
                html.Div(
                      
                    id="filter",
                    children=create_filters(init_state_filter, init_state_time),
                    style={
                        "backgroundColor": "#111111",
                        "border": "3px solid #000000",
                        "borderRadius": "5px",
                        "padding": "15px",
                        "height": "100%",
                        "boxSizing": "border-box",
                        "overflow": "hidden"
                    }
                ),
            ]
        ),

        # ==================================================
        # RIGHT COLUMN (HISTO + TABLE)
        # ==================================================

        html.Div(

            style={
                "display": "grid",
                "gridTemplateRows": "1fr 1fr",
                "gap": "10px",
                "height": "100%",
                "minHeight": 0
            },

            children=[

                # HISTO
                html.Div(

                    dcc.Graph(
                        id="histo",
                        config={"displayModeBar": False},
                        style={"height": "100%"}
                    ),

                    id="histo-container",

                    style={
                        "backgroundColor": "#111111",
                        "border": "3px solid #000000",
                        "borderRadius": "5px",
                        "minHeight": 0
                    }
                ),

                # TABLE
                html.Div(

                    id="table-container",

                    style={
                        "backgroundColor": "#111111",
                        "border": "3px solid #000000",
                        "borderRadius": "5px",
                        "overflowY": "auto",
                        "minHeight": 0
                    }
                ),
            ]
        ),
    ]
)
# --- Import des callbacks après layout ---
from dashboard.callbacks import callbacks  

if __name__ == "__main__":
   
    app.run(debug=True)
  
   