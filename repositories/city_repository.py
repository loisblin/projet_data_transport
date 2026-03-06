


from operator import or_
from sqlalchemy import func
from database import SessionLocal
from models import City
from models import Trip


class CityRepository:

    def __init__(self,session = None):
        if session == None:
            session = SessionLocal()
        self.session = session 
    
    def get_city_by_name(self, name):
        return self.session.query(City).filter_by(name=name).one()

    def get_all_cities(self):
       
        return  self.session.query(City).all()
    
    def get_cities_order_departure_count(self):
        
        return (
        self.session.query(City)
        .join(Trip, Trip.departure_city_id == City.id)
        .group_by(City.id)
        .order_by(func.count(Trip.id).desc())
        .all()
         )
    def get_cities_order_arrival_count(self):
        return (
        self.session.query(
            Trip.arrival_city_id,
            func.count(Trip.id).label("nb_arrival")
        )
        .group_by(Trip.arrival_city_id)
        .order_by(func.count(Trip.id).desc())
        .all()
    )
    def get_cities_order_trips(self):
        return self 