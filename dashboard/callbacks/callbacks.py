from dash import Input, Output
from dashboard.app_instance import app, city_repo, trip_repo

from dashboard.service.services import *
from dashboard.figure.map import create_france_map
cities = get_all_cities()  # récupère la liste des villes à chaque callback
trips = get_all_trips() 
df_city= make_df_city_count_departure()
@app.callback(
    Output('graph-1', 'figure'),
    Output('selected-city-display', 'children'),
    Input('table_id1', 'selected_rows')
)
def update_graph_and_city_text(selected_rows):
    
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