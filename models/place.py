#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from os import environ
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """Representation of Place """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", backref="place")

    if environ['HBNB_TYPE_STORAGE'] == 'db':
        reviews = relationship('Review',
                               cascade='all, delete', backref='place')
        amenities = relationship('Amenity', backref='place_amenities',
                                 secondary='place_amenity',
                                 viewonly=False)

    else:
        @property
        def reviews(self):
            """ getter returns list of reviews """
            list_of_reviews = []
            all_reviews = models.strage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    list_of_reviews.append(review)
            return list_of_reviews

        @property
        def amenities(self):
            """ getter returns list of amenities """
            list_of_amenities = []
            all_amenities = models.storage.all(Amenity)
            for key, obj in all_amenities.items():
                if key in self.amentiy_ids:
                    list_of_amenities.append(obj)
            return list_of_amenities

        @amenities.setter
        def amenities(self, obj=None):
            """Set amenity_ids
            """
            if type(obj).__name__ == 'Amenity':
                new_amenity = 'Amenity' + '.' + obj.id
                self.amenity_ids.append(new_amenity)
