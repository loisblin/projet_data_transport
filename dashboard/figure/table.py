from dash import dash_table
import pandas as pd

def create_city_table(df,id):
    table = dash_table.DataTable(
        id=id,
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        row_selectable="single",
        selected_rows=[],  
        page_size=10,
        sort_action="native",
        filter_action="native",

        # style des cellules
        style_cell={
            'textAlign': 'center',
            'padding': '10px',
            'fontFamily': 'Arial',
            'fontSize': '14px'
        },

        # style header
        style_header={
            'backgroundColor': '#2c3e50',
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center'
        },

        # lignes alternées
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f8f9fa'
            },

            # ligne sélectionnée
            {
                'if': {'state': 'selected'},
                'backgroundColor': '#3498db',
                'color': 'white',
                'border': '1px solid #3498db'
            },

            # hover
            {
                'if': {'state': 'active'},
                'backgroundColor': '#eaf2f8',
                'border': '1px solid #3498db'
            }
        ],

        # bordure du tableau
        style_table={
            'border': '1px solid #ddd',
            'borderRadius': '10px',
            'overflow': 'hidden',
            
        }
    )

    return table

def create_trip_table(trips_filtered,id):
    """
    Retourne un DataTable des trajets filtrés.
    """
    table = dash_table.DataTable(
        id=id,
        columns=[{"name": i, "id": i} for i in ["Départ","Arrivée","Heure","Durée"]],
        data=trips_filtered,
        style_cell={'textAlign': 'center'},
        style_header={'fontWeight': 'bold'}
    )
    return table