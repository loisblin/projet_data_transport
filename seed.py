import random

from database import SessionLocal
from models import City, Trip
from datetime import datetime, timedelta

session = SessionLocal()

# 1️⃣ Supprimer tout (trips d'abord)
session.query(Trip).delete()
session.query(City).delete()
session.commit()

# 2️⃣ Créer les villes
cities = [
    City(name="Paris", latitude=48.8566, longitude=2.3522),
    City(name="Lyon", latitude=45.7640, longitude=4.8357),
    City(name="Marseille", latitude=43.2965, longitude=5.3698),
    City(name="Lille", latitude=50.6292, longitude=3.0573),
    City(name="Bordeaux", latitude=44.8378, longitude=-0.5792),
    City(name="Toulouse", latitude=43.6047, longitude=1.4442),
    City(name="Nantes", latitude=47.2184, longitude=1.5536),
    City(name="Strasbourg", latitude=47.2184, longitude=7.7521),
    City(name="Montpellier", latitude=43.6108, longitude=3.8767)


]
session.add_all(cities)
session.commit()  # IDs générés

# 3️⃣ Créer les trips
paris = session.query(City).filter_by(name="Paris").one()
lyon = session.query(City).filter_by(name="Lyon").one()
marseille = session.query(City).filter_by(name="Marseille").one()
lille= session.query(City).filter_by(name="Lille").one()
bordeaux= session.query(City).filter_by(name="Bordeaux").one()
toulouse = session.query(City).filter_by(name="Toulouse").one()
nantes = session.query(City).filter_by(name="Nantes").one()
strasbourg = session.query(City).filter_by(name="Strasbourg").one()
montpellier = session.query(City).filter_by(name="Montpellier").one()
cities= [paris,lyon,marseille,lille,bordeaux,toulouse,nantes,strasbourg,montpellier]


trips=[]
for k in range (0,50):
    cities_to_choose = cities.copy()
    
    departure_city= random.choice(cities_to_choose)
    cities_to_choose.remove(departure_city)
    arrival_city= random.choice(cities_to_choose)

    # Plage horaire de départ
    start_day = datetime(2024, 3, 4, 6, 0)
    end_day = datetime(2024, 3, 4, 22, 0)
    # Départ aléatoire
    delta_minutes = int((end_day - start_day).total_seconds() / 60)
    departure_time = start_day + timedelta(minutes=random.randint(0, delta_minutes))

    # Durée aléatoire (1h à 5h)
    duration = random.randint(60, 300)  # en minutes
    arrival_time = departure_time + timedelta(minutes=duration)
    trips.append( Trip(departure_city=departure_city, arrival_city=arrival_city, departure_time=departure_time,
         arrival_time=arrival_time, duration_minutes=duration))


session.add_all(trips)
session.commit()
session.close()
print("seeds ok ")