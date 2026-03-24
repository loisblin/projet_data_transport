import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
from repositories.city_repository import CityRepository
from repositories.trip_repository import TripRepository
from dashboard.app_instance import trip_repo, city_repo
def make_df_city_count_departure():
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

def get_all_cities():
    return city_repo.get_all_cities()

def get_trips_from_city(city_name):
    """Retourne les trajets dont la ville de départ est `city_name`"""
    return trip_repo.get_all_departure_trip_city(city_name)

def get_all_trips():
    """retourne tous les trajet"""
    return trip_repo.get_trips()