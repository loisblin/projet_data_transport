import random

from backend.database import SessionLocal
from backend.models import City, Trip
from datetime import datetime, timedelta
import math


def haversine(lat1, lon1, lat2, lon2):
    """return  distance between 2 point """
    R = 6371  
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def get_city_neighbors(cities,n):
    """ return 2 dict, 
    - 'closest': for each city, a list of the n nearest cities
    - 'farthest': for each city, a list of the n farthest cities"""
    closest = {}
    farthest = {}
    
    for city in cities:
        others = [c for c in cities if c != city]
        others_sorted = sorted(others, key=lambda c: haversine(city.latitude, city.longitude, c.latitude, c.longitude))
        closest[city.name] = [c.name for c in others_sorted[:n]]
        farthest[city.name] = [c.name for c in others_sorted[-n:]]
        
    return closest, farthest
def generate_seed_data(n):
    """function which generate n data """
    session = SessionLocal()
    try :
        # 1️⃣ deleat all Trips and cities
        session.query(Trip).delete()
        session.query(City).delete()
        session.commit()

        # 2️⃣ Created cities
        cities = [
            City(name="Paris", latitude=48.8566, longitude=2.3522),
            City(name="Lyon", latitude=45.7640, longitude=4.8357),
            City(name="Marseille", latitude=43.2965, longitude=5.3698),
            City(name="Lille", latitude=50.6292, longitude=3.0573),
            City(name="Bordeaux", latitude=44.8378, longitude=-0.5792),
            City(name="Toulouse", latitude=43.6047, longitude=1.4442),
            City(name="Nantes", latitude=47.2184, longitude=-1.5536),
            City(name="Strasbourg", latitude=48.5734, longitude=7.7521),
            City(name="Montpellier", latitude=43.6108, longitude=3.8767)


        ]
        session.add_all(cities)
        session.commit()  # IDs generated

        city_map = {city.name: city.id for city in cities}
        #put more weights to city which are more likely to be choose in trip
        cities_weights = {
            "Paris": 5,
            "Lyon": 4,
            "Marseille": 3,
            "Lille": 2,
            "Bordeaux": 2,
            "Toulouse": 2,
            "Nantes": 2,
            "Strasbourg": 2,
            "Montpellier": 2
        }
        #make dict to 3 closest and farthest cities to each city 
        dict_closest,dict_farthest= get_city_neighbors(cities,3)

        # generate n Trips 
        trips=[]
        for k in range (0,n):
            

            # choose departure city
            departure_city_name = random.choices(
                list(cities_weights.keys()),      
                weights=list(cities_weights.values()), 
                k=1)[0]

            #choose arrival city
            cities_to_arrive = cities_weights.copy()
            cities_to_arrive.pop(departure_city_name)

            #update weights for distance 
            for city in dict_closest[departure_city_name]:
                cities_to_arrive[city]+=1 
            for city in dict_farthest[departure_city_name]:
                cities_to_arrive[city]-=1 
            arrival_city_name= random.choices(
                list(cities_to_arrive.keys()),      
                weights=list(cities_to_arrive.values()),  
                k=1)[0]
            
            
            # choose day and hour of departure in one week and between 6h-22h
            day_choose= random.randint(1,7)
            hour_choose=random.randint(6,22)
            date_departure= datetime(2026,5,day_choose,hour_choose,0)
            # make randome price and duration between 4 - 6 hour and 40 -120 € that is likely a real trip
            duration = random.randint(240, 360)
            price = random.randint(40,120)
            # update duration  and price compared with distance 
            if arrival_city_name in dict_closest[departure_city_name]:
                duration-=90
                price-=20
            if arrival_city_name in dict_farthest[departure_city_name]:
                duration+=90
                price+=20

            date_arrival = date_departure +  timedelta(minutes=duration)
            
            # generate a possibility of delay 
            delay_category = random.choices(["no","low", "medium", "high", "very_high"],weights=[35,25, 20, 15, 5])[0]
            if delay_category == "no" :
                delay = 0
            elif delay_category == "low":
                delay = random.randint(1, 5)

            elif delay_category == "medium":
                delay = random.randint(5, 10)

            elif delay_category == "high":
                delay = random.randint(10, 20)

            else:
                delay = random.randint(20, 60)



            trips.append(
            Trip(
                departure_city_id=city_map[departure_city_name],
                arrival_city_id=city_map[arrival_city_name],
                departure_time=date_departure,
                arrival_time=date_arrival,
                delay=delay,
                price=price
            )
        )


        session.add_all(trips)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

    finally:    
        session.close()
