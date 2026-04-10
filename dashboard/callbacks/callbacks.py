from dash import Input, Output,State
from dashboard.app_instance import app, city_repo, trip_repo

from dashboard.service.services import *
from dashboard.figure.map import create_france_map

@app.callback(
    Output('graph-1', 'figure'),
    Output('selected-city-display', 'children'),
    Input('table_id1', 'selected_rows'),
    State("data-store", "data")
)
def update_graph_and_city_text(selected_rows, data):
    df_city = pd.DataFrame(data)

    cities = get_all_cities()
    trips = get_all_trips()
    # --- Si aucune ville sélectionnée ---
    if not selected_rows or len(selected_rows) == 0:
        filtered_trips = trips  # afficher tous les trajets
        city_text = "Aucune ville sélectionnée"
    else:
        # Nom de la ville sélectionnée
        selected_city_name = df_city.iloc[selected_rows[0]]['cities']
        # Récupère les trajets depuis le repository
        filtered_trips = trip_repo.get_all_departure_trip_city(selected_city_name)
        city_text = f"Ville sélectionnée : {selected_city_name}"

    # Création de la figure
    fig = create_france_map(cities, filtered_trips)

    # Retour des deux outputs
    return fig, city_text

@app.callback(
    Output("table_id1", "selected_rows"),
    Input("table_id1", "active_cell"),
    State("table_id1", "selected_rows"),
    prevent_initial_call=True
)
def toggle_row(active, selected):
    if not active:
        return selected
    row = active["row"]
    return [] if row in selected else [row]

@app.callback(
    Output("table_id1", "style_data_conditional"),
    Input("table_id1", "selected_rows")
)
def style_selected_rows(selected_rows):
    base_style = [
        # lignes impaires
        {'if': {'row_index': 'odd'}, 'backgroundColor': '#f8f9fa'},

        # cellule hover / focus
        {
            'if': {'state': 'active'},
            'backgroundColor': '#3498db',   
            'border': '1px solid #3498db',
            'color': 'inherit'
        },

        # cellule selected natif
        {
            'if': {'state': 'selected'},
            'backgroundColor': 'inherit',   # garde la couleur de ton callback
            'border': 'none',
            'color': 'inherit'
        }
    ]
    
    # ligne sélectionnée en bleu
    if selected_rows:
        base_style.append({
            'if': {'row_index': selected_rows[0]},
            'backgroundColor': '#3498db',
            'color': 'white'
        })

    return base_style