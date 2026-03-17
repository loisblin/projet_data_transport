from dash import Input, Output
from dashboard.app_instance import app
from dashboard.app import df_city, trips, cities  # juste les données
from dashboard.figure.map import create_france_map

@app.callback(
    Output("selected-city-display", "children"),
    Input("table_id2", "selected_rows")
)
def display_selected_city(selected_rows):
    if not selected_rows:
        return "Aucune ville sélectionnée"

    print("feur")
    print(df_city.iloc[selected_rows[0]]["cities"])
    print("feur2")
    # Récupère le nom de la ville sélectionnée
    selected_city_name = df_city.iloc[selected_rows[0]]['cities']
    return f"Ville sélectionnée : {selected_city_name}"