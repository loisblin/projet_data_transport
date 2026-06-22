import plotly.graph_objects as go
import numpy as np

import folium
import numpy as np
from folium.plugins import AntPath
def create_france_map( trips,cities_dict,metric):
    
    # 🌍 Carte
    m = folium.Map(
        location=[46.6, 2.4],
        zoom_start=6,
        tiles=None,
        width="100%",
        height="100%"
    )

    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png",
        attr="CartoDB",
        name="dark",
        control=False
    ).add_to(m)

    # ------------------
    # 🌆 VILLES
    # ------------------
    
    for city, values  in cities_dict.items():
        
        lat = values[0]
        lon = values[1]
        radius = 5
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color="#4cc9f0",
            fill=True,
            fill_opacity=0.9,
            tooltip=city
        ).add_to(m)

    # ------------------
    # ✈️ TRAJETS
    # ------------------
    for row in trips.itertuples():

        depart = row.departure_city
        arrive = row.arrival_city

        # coords
        lat1, lon1 = cities_dict[depart]
        lat2, lon2 = cities_dict[arrive]

        # épaisseur selon nb trips
        weight = max(1, row.Number_of_trips / 10)
        if metric == "delay":
            # couleur simple (retard)
            color = "green"
            if row.Average_delay > 7:
                color = "orange"
            if row.Average_delay > 9:
                color = "red"
        elif metric =="price" :
            color = "green"
            if row.Average_price > 70:
                color = "orange"
            if row.Average_price > 110:
                color = "red"
        else :
            raise KeyError
        # ligne
        folium.PolyLine(
            locations=[(lat1, lon1), (lat2, lon2)],
            weight=weight,
            color=color,
            opacity=0.7,
            tooltip=f"{depart} → {arrive} | trips: {row.Number_of_trips}"
        ).add_to(m)
        
    html_map = m.get_root().render()

    html_map = html_map.replace(
        'padding-bottom:60.0%;',
        'padding-bottom:0%; height:100%;'
    )

    return html_map