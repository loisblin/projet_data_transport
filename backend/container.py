from backend.repositories.city_repository import CityRepository
from backend.repositories.trip_repository import TripRepository
from backend.services.map_service import Map_service
from backend.services.histo_service import Histo_service
from backend.services.table_service import Table_service


trip_repo = TripRepository()
city_repo = CityRepository()

map_service =Map_service(trip_repo,city_repo)
histo_service= Histo_service(trip_repo)
table_service = Table_service(trip_repo)
