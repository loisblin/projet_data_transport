from repositories.city_repository import CityRepository
from repositories.trip_repository import TripRepository
from database import SessionLocal
from service.services import make_df_city_count_departure

session= SessionLocal()
city =CityRepository(session)
trip = TripRepository(session)
# print(trip.get_trip_2_cities("Marseille","Paris"))
# city2=(city.get_cities_order_departure())

# print(trip.get_trips())
# print(city.get_cities_order_arrival_count())
# print(trip.get_city_by_name("lille"))

df = make_df_city_count_departure(city)
print(df)