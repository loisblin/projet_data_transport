from repositories.city_repository import CityRepository
from repositories.trip_repository import TripRepository
from backend.database import SessionLocal

session= SessionLocal()
city =CityRepository(session)
trip = TripRepository(session)
# print(trip.get_trip_2_cities("Marseille","Paris"))
# city2=(city.get_cities_order_departure())

# print(trip.get_trips())
# print(city.get_cities_order_arrival_count())
# print(trip.get_city_by_name("lille"))

p=trip.count_trip_by_day()
day = p[0][0]
d=trip.count_trip_by_hour_for_day(day)
print(d)