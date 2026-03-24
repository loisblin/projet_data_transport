# dashboard/app_instance.py
import dash
from repositories.city_repository import CityRepository
from repositories.trip_repository import TripRepository
app = dash.Dash(__name__)
city_repo = CityRepository()
trip_repo = TripRepository()