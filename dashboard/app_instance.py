# dashboard/app_instance.py
import dash
from backend.repositories.city_repository import CityRepository
from backend.repositories.trip_repository import TripRepository

app = dash.Dash(__name__)