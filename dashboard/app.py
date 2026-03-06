import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from repositories.city_repository import CityRepository
from repositories.trip_repository import TripRepository
import plotly.graph_objects as go
app = dash.Dash(__name__)

city_repo = CityRepository()
trip_repo = TripRepository()

cities = city_repo.get_all_cities()
trips= trip_repo.get_trips()
data = []
fig = go.Figure()
for city in cities:
    data.append({
        "city": city.name,
        "lat": city.latitude,
        "lon": city.longitude
    })

df = pd.DataFrame(data)
# tracer les villes
for trip in trips:
    fig.add_trace(go.Scattergeo(
        lon=[trip.departure_city.longitude, trip.arrival_city.longitude],
        lat=[trip.departure_city.latitude, trip.arrival_city.latitude],
        mode='lines',
        line=dict(width=2, color='blue'),
        opacity=0.6,
    ))

# tracer les villes comme points
cities_set = {trip.departure_city for trip in trips}.union(
    {trip.arrival_city for trip in trips}
)

for city in cities_set:
    fig.add_trace(go.Scattergeo(
        lon=[city.longitude],
        lat=[city.latitude],
        mode='markers+text',
        marker=dict(size=8, color='red'),
        text=[city.name],
        textposition="top center"
    ))

# zoom sur la France
fig.update_geos(
    center={"lat":46.5, "lon":2.5},
    lataxis_range=[41, 51],
    lonaxis_range=[-5, 10],
    showcountries=True,
    showland=True,
    landcolor="rgb(240,240,240)"
)

fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
app.layout = html.Div([
    html.H1("Carte des villes"),
    dcc.Graph(figure=fig)
])


if __name__ == "__main__":
    app.run(debug=True)