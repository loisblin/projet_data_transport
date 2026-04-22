from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    departures = relationship("Trip", foreign_keys="Trip.departure_city_id", back_populates="departure_city")
    arrivals = relationship("Trip", foreign_keys="Trip.arrival_city_id", back_populates="arrival_city")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)

    departure_city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    arrival_city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)

    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)

    delay = Column(Integer, nullable=True) 

    price = Column(Float, nullable=True) 

    departure_city = relationship("City", foreign_keys=[departure_city_id], back_populates="departures")
    arrival_city = relationship("City", foreign_keys=[arrival_city_id], back_populates="arrivals")