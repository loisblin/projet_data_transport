from dash import ALL, Input, Output,State
from dashboard.app_instance import app
import copy
from dash import callback_context, no_update

from dashboard.utils.filter_utils import prepare_map_dataframe ,prepare_histo_dataframe
from dashboard.components.filter import format_selection, toggle_class
from dashboard.components.filter import create_filters
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
    Input("store-state-filtre","data"),
    Input("store-state-time", "data"),
    State("store-histo", "data"),
    State("store-init","data"),
)
def update_histo(state_filter,state_time,histo_data ,init):
    if init :
        df = pd.DataFrame(histo_data)
        histo_df = prepare_histo_dataframe(df,state_filter["city"])
        if state_filter["histo_metric"] == "price":
            metric = "average_price"
        elif state_filter["histo_metric"] == "delay":
            metric = "average_delay"
        else:
            print('error')
        if state_time["hour"] is not None :
            return create_histogram(histo_df, 'period', metric,state_time["hour"])
        else:
            return create_histogram(histo_df, 'period', metric)
    else:
        pass
@app.callback(
    Output("table-container", "children"),
    Input("store-state-time", "data"),
    Input("store-state-filtre","data"),
    State("store-table", "data"),
    State("store-init","data")
)
def update_table(state_time,state_filter,table_data,init):
    if init :
        df = pd.DataFrame(table_data)
        if state_filter["city"] is not None:
            return create_table_city(df,state_filter["city"])
        else:
                return create_table_city(df)
    else :
        pass

@app.callback(
    Output("map","srcDoc"),
    Input("store-state-filtre","data"),
    Input("store-state-time", "data"),
    State("store-map","data"),
    State("store-cities","data"),
    State("store-init","data")
    )
def update_map(state_filter,state_time,map_data,city_dict,init):
    if init :
        
        df = pd.DataFrame(map_data)
        map_df= prepare_map_dataframe(df,state_filter["city"])
        return create_france_map(map_df,city_dict,state_filter["map_metric"])
    else :
        pass


@app.callback(
    Output("store-state-filtre", "data"),
    Output("filter-title", "children"),
    Output("histo-metric-toggle", "className"),
    Output("map-metric-toggle", "className"),
    Input({"type": "row", "city": ALL}, "n_clicks_timestamp"),
    Input("histo-metric-toggle", "n_clicks"),
    Input("map-metric-toggle", "n_clicks"),
    Input("store-state-time", "data"),
    State({"type": "row", "city": ALL}, "id"),
    State("store-state-filtre", "data"),
    prevent_initial_call=True
)
def update_filters(timestamps, histo_click, map_click, state_time, ids, state):

    state = state.copy()
    trigger = callback_context.triggered_id

    # =====================
    # CITY SELECTION
    # =====================
    if isinstance(trigger, dict) and trigger.get("type") == "row":

        if timestamps and any(t is not None for t in timestamps):
            max_timestamp = max(t for t in timestamps if t is not None)
            idx = timestamps.index(max_timestamp)
            city = ids[idx]["city"]

            state["city"] = None if state["city"] == city else city

    # =====================
    # HISTO TOGGLE
    # =====================
    elif trigger == "histo-metric-toggle":
        state["histo_metric"] = (
            "delay" if state["histo_metric"] == "price" else "price"
        )

    # =====================
    # MAP TOGGLE
    # =====================
    elif trigger == "map-metric-toggle":
        state["map_metric"] = (
            "delay" if state["map_metric"] == "price" else "price"
        )

    # trigger == "store-state-time" -> juste rafraîchir le titre, rien d'autre

    title = format_selection(state.get("city"), state_time.get("day"), state_time.get("hour"))

    return (
        state,
        title,
        toggle_class(state["histo_metric"]),
        toggle_class(state["map_metric"]),
    )