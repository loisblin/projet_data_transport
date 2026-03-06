from repositories.city_repository import CityRepository
from repositories.trip_repository import TripRepository
from database import SessionLocal

session= SessionLocal()
city =CityRepository(session)
trip = TripRepository(session)
# print(trip.get_trip_2_cities("Marseille","Paris"))
city2=(city.get_cities_order_departure_count())
for c in city2:
    print(c.name,len(trip.get_all_departure_trip_city(c.name)))
    