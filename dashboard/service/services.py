import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
from repositories.city_repository import CityRepository
from repositories.trip_repository import TripRepository

def make_df_city_count_departure(city_repo):
    cities = city_repo.get_all_cities()
    name=[]
    departure_number=[]
    for city in cities :
        name.append(city.name)
        departure_number.append(city_repo.get_count_departure_trip_by_city(city.name))
    df = pd.DataFrame({
    "cities": name,
    "departure_number": departure_number
        })
    return df
