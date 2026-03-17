import plotly.graph_objects as go
import numpy as np

def create_france_map(cities_set, trips):
    fig = go.Figure()

    # 🌆 Villes
    for city in cities_set:
        fig.add_trace(go.Scattermapbox(
            lon=[city.longitude],
            lat=[city.latitude],
            mode='markers',
            marker=dict(size=8, color='#4cc9f0', opacity=0.9),
            hoverinfo='skip',
            showlegend=False
        ))

    # ✈️ Trajets
    for trip in trips:
        lon_start, lon_end = trip.departure_city.longitude, trip.arrival_city.longitude
        lat_start, lat_end = trip.departure_city.latitude, trip.arrival_city.latitude
        lons = np.linspace(lon_start, lon_end, 50)
        lats = np.linspace(lat_start, lat_end, 50) + np.sin(np.linspace(0, np.pi, 50))*0.3

        fig.add_trace(go.Scattermapbox(
            lon=lons,
            lat=lats,
            mode='lines',
            line=dict(width=2, color='#ff4d6d'),
            opacity=0.8,
            hoverinfo='skip',
            showlegend=False
        ))

    fig.update_layout(
        mapbox=dict(
            style="open-street-map",  # style gratuit, sombre mais pas noir total
            center=dict(lat=46.6, lon=2.4),
            zoom=5,
            layers=[]
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#0b0b0b",
        plot_bgcolor="#0b0b0b"
    )

    return fig