import plotly.graph_objects as go
import numpy as np

import folium
import numpy as np

def create_france_map(cities_set, trips,selected_city=None):

    import folium
    import numpy as np
    from folium.plugins import AntPath

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
    for city in cities_set:

        # 👉 prêt pour évolution (ex: city.volume)
        radius = 4

        folium.CircleMarker(
            location=[city.latitude, city.longitude],
            radius=radius,
            color="#4cc9f0",
            fill=True,
            fill_opacity=0.9,
            tooltip=city.name
        ).add_to(m)

    # ------------------
    # ✈️ TRAJETS
    # ------------------
    for trip in trips:

        lon_start = trip.departure_city.longitude
        lon_end = trip.arrival_city.longitude

        lat_start = trip.departure_city.latitude
        lat_end = trip.arrival_city.latitude

        # courbe
        lons = np.linspace(lon_start, lon_end, 50)
        lats = (
            np.linspace(lat_start, lat_end, 50)
            + np.sin(np.linspace(0, np.pi, 50)) * 0.5
        )

        coords = list(zip(lats, lons))

        # ------------------
        # 🎯 PARAMS SCALABLE
        # ------------------

        # 👉 futur: remplacer par trip.volume / price
        weight = 2
        color = "#ff4d6d"

        # ------------------
        # 🌫️ GLOW (fond)
        # ------------------
        folium.PolyLine(
            locations=coords,
            color=color,
            weight=6,
            opacity=0.1
        ).add_to(m)

        # ------------------
        # 🔥 LIGNE PRINCIPALE
        # ------------------
        folium.PolyLine(
            locations=coords,
            color=color,
            weight=weight,
            opacity=0.8,
            tooltip=f"{trip.departure_city.name} ↔ {trip.arrival_city.name}"
        ).add_to(m)
        
        # ------------------
        # ⚡ ANIMATION
        # ------------------
        if selected_city == True:
            AntPath(
                locations=coords,
                color=color,
                weight=2,
                delay=900,
                opacity=0.6
            ).add_to(m)

    html_map = m.get_root().render()

    html_map = html_map.replace(
        'padding-bottom:60.0%;',
        'padding-bottom:0%; height:100%;'
    )

    return html_map