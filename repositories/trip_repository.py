
from operator import or_, and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from database import SessionLocal
from models import City
from models import Trip


class TripRepository:

    def __init__(self,session = None):
        if session == None:
            session = SessionLocal()
        self.session = session  
    def get_city_by_name(self, name):
        try:
            return self.session.query(City).filter_by(name=name).one()
        except (NoResultFound, MultipleResultsFound):
            return None
    def get_trips(self):
        trips = self.session.query(Trip).all()
        return trips 
    def get_all_trip_city(self,city_name):

        city = self.get_city_by_name(city_name)

        if not city:
            return []

        return (
            self.session.query(Trip)
            .filter(
                or_(
                    Trip.departure_city_id == city.id,
                    Trip.arrival_city_id == city.id
                )
            )
            .all()
        )
    def get_all_arrival_trip_city(self, city_name):
        city = self.get_city_by_name(city_name)

        return self.session.query(Trip).filter(Trip.arrival_city_id == city.id).all()
    
    def get_all_departure_trip_city(self, city_name):
        city = self.get_city_by_name(city_name)

        return self.session.query(Trip).filter(Trip.departure_city_id == city.id).all()
    
    def get_same_trip(self,departure_city_name,arrival_city_name):
        departure_city = self.get_city_by_name(departure_city_name)
        arrival_city = self.get_city_by_name(arrival_city_name)
        return self.session.query(Trip).filter(
            Trip.departure_city_id ==departure_city.id,
            Trip.arrival_city_id==arrival_city.id
                          ).all()
    def get_trip_2_cities(self,city_1_name,city_2_name):
        city1= self.get_city_by_name(city_1_name)
        city2= self.get_city_by_name(city_2_name)
        return self.session.query(Trip).filter(
        or_(
            and_(
                Trip.departure_city_id == city1.id,
                Trip.arrival_city_id == city2.id
            ),
            and_(
                Trip.departure_city_id == city2.id,
                Trip.arrival_city_id == city1.id
            )
        )
        ).all()

        
