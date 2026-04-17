import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
from repositories.city_repository import CityRepository
from repositories.trip_repository import TripRepository
from dashboard.app_instance import trip_repo, city_repo

def get_all_cities():
    return city_repo.get_all_cities()

def get_trips_from_city(city_name):
    """Retourne les trajets dont la ville de départ est `city_name`"""
    return trip_repo.get_all_departure_trip_city(city_name)

def get_all_trips():
    """retourne tous les trajet"""
    return trip_repo.get_trips()

def make_df_trip_date(city= None ):
    "make df count nomber trip per day"

    data=trip_repo.count_trip_by_day(city)

    df = pd.DataFrame(data, columns=["day", "count"])

    return df
def make_df_trip_date_by_hour(day,city=None):
    "make df count nomber trip per hour with the day in arg"
    data=trip_repo.count_trip_by_hour_for_day(day,city)
    df = pd.DataFrame(data, columns=["hour", "count"])
    return df
def make_df_trip_for_hour(day, hour=None, city=None):

    data = trip_repo.count_trip_by_hour_for_day(day, city, hour)

    if not data:
        return pd.DataFrame(columns=["hour", "count"])

    return pd.DataFrame(data, columns=["hour", "count"])
def make_df_city_trip_depart(day=None,hour=None):
    data= trip_repo.get_count_departures_by_city(day,hour)
    if not data:
        return pd.DataFrame(columns=["cities", "count"])

    return pd.DataFrame(data, columns=["cities", "count"])