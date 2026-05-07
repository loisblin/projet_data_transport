from dash import ALL, Input, Output,State
from dashboard.app_instance import app
import copy
from dash import callback_context, no_update

from dashboard.utils.filter_utils import prepare_map_dataframe ,prepare_histo_dataframe


from dashboard.figure.map import create_france_map
from dashboard.figure.histograme import *
from dashboard.figure.table import create_table_city
from backend.container import *
@app.callback(
    Output("store-map", "data"),
    Output("store-histo", "data"),
    Output("store-table", "data"),
    Output("store-cities", "data"),
    Output("store-init", "data"),
    Output("store-state-time", "data"),
    Input("store-init", "data"),
    Input("histo", "clickData"),
    Input("histo-container", "n_clicks"), 
    State("store-state-time", "data"),
    State("store-cities", "data"),
)
def init(init, clickData, n_clicks, state_time, cities):
    new_state_time = copy.deepcopy(state_time)

    if clickData:
        value = clickData["points"][0]["x"]

        if state_time["granularity"] == "week":
            new_state_time["day"] = value
            new_state_time["granularity"] = "day"
            new_state_time["hour"] = None

        elif state_time["granularity"] == "day":
            if state_time.get("day") == value:  
                new_state_time["day"] = None
                new_state_time["granularity"] = "week"
                new_state_time["hour"] = None
            else:
                new_state_time["granularity"] = "hour"
                new_state_time["hour"] = value

        elif state_time["granularity"] == "hour":
            if state_time["hour"] == value:  # double clic heure → reset
                new_state_time["day"] = None
                new_state_time["granularity"] = "week"
                new_state_time["hour"] = None
            else:
                new_state_time["hour"] = value

    map_df = map_service.get_trips_map_data(
        new_state_time["granularity"], new_state_time["day"], new_state_time["hour"]
    )
    
    histo_df = histo_service.get_histo_data(
        new_state_time["granularity"], new_state_time["day"]
    )
    table_df = table_service.get_table_data(new_state_time["granularity"], new_state_time["day"], new_state_time["hour"])

    map_df= prepare_map_dataframe(map_df,None)
    histo_df = prepare_histo_dataframe(histo_df,None)
    if init == False:
        cities = map_service.get_cities_coords_dict()
    else:
        cities = cities
    return (
        map_df.to_dict("records"),
        histo_df.to_dict("records"),
        table_df.to_dict("records"),
        cities,
        True,
        new_state_time
    )


@app.callback(
    Output("histo", "figure"),
    
    Input("store-state-time", "data"),
    State("store-histo", "data"),
    State("store-init","data"),
)
def update_histo(state_time,histo_data ,init):
    if init :
        df = pd.DataFrame(histo_data)
        if state_time["hour"] is not None :
            return create_histogram(df, 'period', "average_price",state_time["hour"])
        else:
            return create_histogram(df, 'period', "average_price")
    else:
        pass
@app.callback(
    Output("table-container", "children"),
    Input("store-state-time", "data"),
    State("store-table", "data"),
    State("store-init","data")
)
def update_table(state_time,table_data,init):
    if init :
        df = pd.DataFrame(table_data)

        return create_table_city(df)
    else :
        pass

@app.callback(
    Output("map","srcDoc"),
    Input("store-state-time", "data"),
    State("store-map","data"),
    State("store-cities","data"),
    State("store-state-time","data"),
    State("store-init","data")
    )
def update_map(state_time,map_data,city_dict,state,init):
    if init :
        df = pd.DataFrame(map_data)
        return create_france_map(df,city_dict)
    else :
        pass



# @app.callback(
#     Output("store-state", "data"),
#     Output("store-map", "data"),
#     Output("store-histo", "data"),
#     Output("store-table", "data"),
#     Input("histo", "clickData"),
#     Input({"type": "row", "city": ALL}, "n_clicks"),
#     State("data-store", "data"),
#     State("drill-state", "data"),
# )

# def update_state(clickData,n_clicks, data, state):

#     if state is None:
#         state = {
#             "level": "day",
#             "city": None,
#             "day": None,
#             "hour": None
#         }

#     ctx = callback_context
#     trigger = ctx.triggered[0]["prop_id"].split(".")[0]
    
#     if not ctx.triggered:
#         return state
#     df_city = pd.DataFrame(data)

#     # ------------------
#     # CITY CLICK
#     # ------------------
#     try:
#         trigger_data = json.loads(trigger)
#     except:
#         trigger_data = {}
#     if trigger_data.get("type") == "row":
        
#         clicked_city = trigger_data["city"]
#         # 🔥 toggle
#         if state.get("city") == clicked_city:
#             # reset
#             state["city"] = None
#             state["day"] = None
#             state["hour"] = None
#             state["level"] = "day"
#         else:
#             # nouvelle ville
#             state["city"] = clicked_city
#             state["day"] = None
#             state["hour"] = None
#             state["level"] = "day"
#     # ------------------
#     # HISTO CLICK
#     # ------------------
#     elif trigger == "histo_day" and clickData:

#         value = clickData["points"][0]["x"]

#         if state["level"] == "day":
#             state["day"] = value
#             state["level"] = "hour"
#             state["hour"] = None
#         else:
#             if state["hour"] == value:
#                 state["hour"] = None
#                 state["day"] = None
#                 state["level"] = "day"
#             else:
#                 state["hour"] = value

#     return state
# @app.callback(
#     Output("histo_day", "figure"),
#     Input("drill-state", "data"),
#     State("data-store", "data")
# )
# def update_histo(state, data):

#     city = state.get("city")
#     day = state.get("day")
#     hour = state.get("hour")
#     level = state.get("level")


#     level = state.get("level")

#     # =========================
#     # MODE DAY
#     # =========================
#     if level == "day":

#         df = make_df_trip_date(city=city)
#         return create_histogram(df, "day", "number of departures")

#     # =========================
#     # MODE HOUR
#     # =========================
#     if level == "hour":

#         df = make_df_trip_date_by_hour(day, city=city)

#         return create_histogram(df, "hour", "number of departures", hour)
# @app.callback(
#     Output("table-container", "children"),
#     Input("drill-state", "data"),
#     State("data-store", "data")
# )
# def update_table(state, data):

#     df = pd.DataFrame(data)

#     city = state.get("city")
#     day = state.get("day")
#     hour = state.get("hour")
#     level = state.get("level")

#     # ------------------
#     # FILTRAGE DATA
#     # ------------------

#     if level == "day":
#         df = make_df_city_trip_depart()

#     elif level == "hour":
#         df = make_df_city_trip_depart(day)

#     if hour:
#         df = make_df_city_trip_depart(day, hour)

#     # ------------------
#     # BUILD TABLE
#     # ------------------

#     header = html.Div(
#         [
#             html.Div(col, style={"flex": 1, "fontWeight": "bold", "color": "white"})
#             for col in df.columns
#         ],
#         style={
#             "display": "flex",
#             "padding": "10px",
#             "borderBottom": "2px solid #333",
#             "backgroundColor": "#1a1a1a"
#         }
#     )

#     rows = []

#     for i in range(len(df)):

#         row_city = df.iloc[i]["cities"]

#         # 🔥 STYLE DYNAMIQUE
#         bg = "#111111"
#         if city == row_city:
#             bg = "#1f6feb"  # bleu sélection

#         row = html.Div(
#             id={
#                 "type": "row",
#                 "city": row_city
#             },
#             children=[
#                 html.Div(str(df.iloc[i][col]), style={"flex": 1})
#                 for col in df.columns
#             ],
#             style={
#                 "display": "flex",
#                 "padding": "10px",
#                 "cursor": "pointer",
#                 "backgroundColor": bg,
#                 "color": "white",
#                 "borderBottom": "1px solid #222",
#                 "transition": "background-color 0.2s"
#             }
#         )

#         rows.append(row)

#     return html.Div([header] + rows)
# @app.callback(
#     Output("map","srcDoc"),
#     Input("drill-state", "data"),
#     State("data-store", "data")
# )
# def update_map(state,data):
#     city = state.get("city")
#     day = state.get("day")
#     hour = state.get("hour")
#     level = state.get("level")
#     selected_city = None
#     if city is not None:
#         selected_city= True

#     trips= make_df_map_filtre(city,day,hour)
#     cities= get_all_cities()
#     return create_france_map(cities,trips,selected_city) 












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
