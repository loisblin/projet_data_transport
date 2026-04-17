from dash import ALL, Input, Output,State
from dashboard.app_instance import app, city_repo, trip_repo

from dash import callback_context, no_update
import json

from dashboard.service.services import *
from dashboard.figure.map import create_france_map
from dashboard.figure.histograme import *

@app.callback(
    Output("drill-state", "data"),
    Input("histo_day", "clickData"),
    Input({"type": "row", "city": ALL}, "n_clicks"),
    State("data-store", "data"),
    State("drill-state", "data"),
)
def update_state(clickData,n_clicks, data, state):

    if state is None:
        state = {
            "level": "day",
            "city": None,
            "day": None,
            "hour": None
        }

    ctx = callback_context
    trigger = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if not ctx.triggered:
        return state
    df_city = pd.DataFrame(data)

    # ------------------
    # CITY CLICK
    # ------------------
    try:
        trigger_data = json.loads(trigger)
    except:
        trigger_data = {}
    if trigger_data.get("type") == "row":
        
        clicked_city = trigger_data["city"]
        # 🔥 toggle
        if state.get("city") == clicked_city:
            # reset
            state["city"] = None
            state["day"] = None
            state["hour"] = None
            state["level"] = "day"
        else:
            # nouvelle ville
            state["city"] = clicked_city
            state["day"] = None
            state["hour"] = None
            state["level"] = "day"
    # ------------------
    # HISTO CLICK
    # ------------------
    elif trigger == "histo_day" and clickData:

        value = clickData["points"][0]["x"]

        if state["level"] == "day":
            state["day"] = value
            state["level"] = "hour"
            state["hour"] = None
        else:
            if state["hour"] == value:
                state["hour"] = None
                state["day"] = None
                state["level"] = "day"
            else:
                state["hour"] = value

    return state
@app.callback(
    Output("histo_day", "figure"),
    Input("drill-state", "data"),
    State("data-store", "data")
)
def update_histo(state, data):

    city = state.get("city")
    day = state.get("day")
    hour = state.get("hour")
    level = state.get("level")


    level = state.get("level")

    # =========================
    # MODE DAY
    # =========================
    if level == "day":

        df = make_df_trip_date(city=city)
        return create_histogram(df, "day", "count")

    # =========================
    # MODE HOUR
    # =========================
    if level == "hour":

        df = make_df_trip_date_by_hour(day, city=city)

        return create_histogram(df, "hour", "count", hour)
@app.callback(
    Output("table-container", "children"),
    Input("drill-state", "data"),
    State("data-store", "data")
)
def update_table(state, data):

    df = pd.DataFrame(data)

    city = state.get("city")
    day = state.get("day")
    hour = state.get("hour")
    level = state.get("level")

    # ------------------
    # FILTRAGE DATA
    # ------------------

    if level == "day":
        df = make_df_city_trip_depart()

    elif level == "hour":
        df = make_df_city_trip_depart(day)

    if hour:
        df = make_df_city_trip_depart(day, hour)

    # ------------------
    # BUILD TABLE
    # ------------------

    header = html.Div(
        [
            html.Div(col, style={"flex": 1, "fontWeight": "bold", "color": "white"})
            for col in df.columns
        ],
        style={
            "display": "flex",
            "padding": "10px",
            "borderBottom": "2px solid #333",
            "backgroundColor": "#1a1a1a"
        }
    )

    rows = []

    for i in range(len(df)):
        print(df.columns)
        row_city = df.iloc[i]["cities"]

        # 🔥 STYLE DYNAMIQUE
        bg = "#111111"
        if city == row_city:
            bg = "#1f6feb"  # bleu sélection

        row = html.Div(
            id={
                "type": "row",
                "city": row_city
            },
            children=[
                html.Div(str(df.iloc[i][col]), style={"flex": 1})
                for col in df.columns
            ],
            style={
                "display": "flex",
                "padding": "10px",
                "cursor": "pointer",
                "backgroundColor": bg,
                "color": "white",
                "borderBottom": "1px solid #222",
                "transition": "background-color 0.2s"
            }
        )

        rows.append(row)

    return html.Div([header] + rows)
# @app.callback(
#     Output("table_id1", "style_data_conditional"),
#     Input("table_id1", "selected_rows"),
# )
# def update_style(selected_rows):

#     base = [
#         {
#             "if": {"row_index": "odd"},
#             "backgroundColor": "#161616",
#             "color": "white",
#         },
#     ]

#     if selected_rows:
#         base.append({
#             "if": {"row_index": selected_rows[0]},
#             "backgroundColor": "#1f6feb",
#             "color": "white",
#             "fontWeight": "bold",
#         })

#     return base
# @app.callback(
#     Output("histo_day", "figure"),
#     Input("drill-state", "data"),
#     State("data-store", "data")
# )
# def update_table(state, data):
#     pass
# @app.callback(
#     Output('graph-1', 'figure'),
#     Output('selected-city-display', 'children'),
#     Input('table_id1', 'selected_rows'),
#     State("data-store", "data")
# )
# def update_graph_and_city_text(selected_rows, data):
#     df_city = pd.DataFrame(data)

#     cities = get_all_cities()
#     trips = get_all_trips()
#     # --- Si aucune ville sélectionnée ---
#     if not selected_rows or len(selected_rows) == 0:
#         filtered_trips = trips  # afficher tous les trajets
#         city_text = "Aucune ville sélectionnée"
#     else:
#         # Nom de la ville sélectionnée
#         selected_city_name = df_city.iloc[selected_rows[0]]['cities']
#         # Récupère les trajets depuis le repository
#         filtered_trips = trip_repo.get_all_departure_trip_city(selected_city_name)
#         city_text = f"Ville sélectionnée : {selected_city_name}"

#     # Création de la figure
#     fig = create_france_map(cities, filtered_trips)

#     # Retour des deux outputs
#     return fig, city_text

# @app.callback(
#     Output("table_id1", "selected_rows"),
#     Input("table_id1", "active_cell"),
#     State("table_id1", "selected_rows"),
#     prevent_initial_call=True
# )
# def toggle_row(active, selected):
#     if not active:
#         return selected
#     row = active["row"]
#     return [] if row in selected else [row]

# @app.callback(
#     Output("table_id1", "style_data_conditional"),
#     Input("table_id1", "selected_rows")
# )
# def style_selected_rows(selected_rows):
#     base_style = [
#         # lignes impaires
#         {'if': {'row_index': 'odd'}, 'backgroundColor': '#f8f9fa'},

#         # cellule hover / focus
#         {
#             'if': {'state': 'active'},
#             'backgroundColor': '#3498db',   
#             'border': '1px solid #3498db',
#             'color': 'inherit'
#         },

#         # cellule selected natif
#         {
#             'if': {'state': 'selected'},
#             'backgroundColor': 'inherit',   # garde la couleur de ton callback
#             'border': 'none',
#             'color': 'inherit'
#         }
#     ]
    
#     # ligne sélectionnée en bleu
#     if selected_rows:
#         base_style.append({
#             'if': {'row_index': selected_rows[0]},
#             'backgroundColor': '#3498db',
#             'color': 'white'
#         })

#     return base_style
