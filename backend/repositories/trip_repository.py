
from operator import or_, and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import func,extract
from sqlalchemy.orm import aliased
from backend.database import SessionLocal
from backend.models import City
from backend.models import Trip


class TripRepository:

    def __init__(self,session = None):
        if session is None:
            session = SessionLocal()
        self.session = session  
    
    def _get_base_map(self):
        departure_city = aliased(City)
        arrival_city = aliased(City)

        query = (
            self.session.query(
                departure_city.name.label("departure_city"),
                arrival_city.name.label("arrival_city"),
                func.count(Trip.id).label("Number_of_trips"),
                func.avg(Trip.price).label("Average_price"),
                func.avg(Trip.delay).label("Average_delay"),
            )
            .join(departure_city, Trip.departure_city_id == departure_city.id)
            .join(arrival_city, Trip.arrival_city_id == arrival_city.id)
            .group_by(departure_city.id, arrival_city.id)
        )

        return query
    def _get_base_table(self):
        departure_city = aliased(City)
        query = (self.session.query(
            departure_city.name.label("Departure_city"),
            func.count(Trip.id).label("Number_of_departure"),
            func.avg(Trip.price).label("Average_price"),
            func.avg(Trip.delay).label("Average_delay")

        )
        .join(departure_city,Trip.departure_city_id == departure_city.id)
        .group_by(departure_city.id)
        )
        return query
    def _filtre_time(self,query,time_granularity,day,hour):
        if time_granularity == "week":
            pass
        elif time_granularity == "day":
            query = query.filter(func.date(Trip.departure_time) == day)
        elif time_granularity =="hour":
            query = (
            query
            .filter(func.date(Trip.departure_time) == day)
            .filter(extract('hour', Trip.departure_time) == hour)
            )
        else:
            raise ValueError("wrong time granularity")
        return query


    def get_trips_map_data(self,time_granularity,day,hour):
        query = self._get_base_map()
        query = self._filtre_time(query,time_granularity,day,hour )
        return query.all()
    
    def get_table_data(self,time_granularity,day,hour):
        query = self._get_base_table()
        query = self._filtre_time(query,time_granularity,day,hour )
        return query.all()
    
    def get_histo_data(self, granularity, day):

        departure_city = aliased(City)

        query = (
            self.session.query(
                departure_city.name.label("departure_city"),
                func.avg(Trip.price).label("average_price"),
                func.avg(Trip.delay).label("average_delay"),
            )
            .join(departure_city, Trip.departure_city_id == departure_city.id)
        )

        if granularity == "week":
            query = query.add_columns(
                func.date(Trip.departure_time).label("period")
            ).group_by(departure_city.name, func.date(Trip.departure_time))

        elif granularity == "day" or granularity == "hour":
            query = (
                query
                .filter(func.date(Trip.departure_time) == day)
                .add_columns(
                    extract('hour', Trip.departure_time).label("period")
                )
                .group_by(departure_city.name, extract('hour', Trip.departure_time))
            )

        return query.all()



            
    def get_city_by_name(self, name):
        try:
            return self.session.query(City).filter_by(name=name).one()
        except (NoResultFound, MultipleResultsFound):
            return None
    def get_hourly_trips_map(self,day,hour):
        _, _, query = self._base_map_query()
        query = (
            query
            .filter(func.date(Trip.departure_time) == day)
            .filter(extract('hour', Trip.departure_time) == hour)
        )

        return query.all()
    
    
    
    def get_trips(self,city=None,day=None,hour=None):
        query = self.session.query(Trip)
        if city:
            query = query.filter(Trip.departure_city.has(name=city))

        if day is not None:
            query = query.filter(func.date(Trip.departure_time) == day)

        if hour is not None:
            query = query.filter(extract('hour', Trip.departure_time) == hour)
        return query.all()
    
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

    def count_trip_by_hour_for_day(self, day=None, city=None, hour=None):

        query = self.session.query(
            extract('hour', Trip.departure_time).label("hour"),
            func.count().label("count")
        )

        if city:
            query = query.filter(Trip.departure_city.has(name=city))

        if day is not None:
            query = query.filter(func.date(Trip.departure_time) == day)

        if hour is not None:
            query = query.filter(extract('hour', Trip.departure_time) == hour)

        return query.group_by("hour").order_by("hour").all()
    def count_trip_by_day(self,city=None):
        query = self.session.query(
                func.date(Trip.departure_time).label("day"),
                func.count().label("count")
            )
        if city:
            query = query.filter(Trip.departure_city.has(name=city))
        return (
            query
            .group_by("day")
            .order_by("day")
            .all()
        )
    def get_count_departures_by_city(self, day=None, hour=None):
        query = (
        self.session.query(
            City.name,
            func.count(Trip.id)
        )
        .join(City, City.id == Trip.departure_city_id)
        )

        # ------------------
        # FILTER DAY
        # ------------------
        if day is not None:
            query = query.filter(func.date(Trip.departure_time) == day)

        # ------------------
        # FILTER HOUR
        # ------------------
        if hour is not None:
            query = query.filter(extract('hour', Trip.departure_time) == hour)

        # ------------------
        # GROUP BY
        # ------------------
        query = query.group_by(City.name)

        return query.all()