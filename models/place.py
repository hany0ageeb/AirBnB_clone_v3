#!/usr/bin/python
""" holds class Place"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

if models.storage_t == 'db':
    place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column(
            'place_id',
            ForeignKey('places.id'),
            primary_key=True,
            nullable=False),
        Column(
            'amenity_id',
            ForeignKey('amenities.id'),
            primary_key=True,
            nullable=False)
        )


class Place(BaseModel, Base):
    """Representation of Place """
    if models.storage_t == 'db':
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
        amenities = relationship(
                "Amenity",
                secondary=place_amenity,
                back_populates='place_amenities',
                viewonly=False)

        @property
        def amenity_ids(self):
            """amenity_ids property getter"""
            return [amenity.id for amenity in self.amenities]

        def remove_amenity(self, amenity):
            """remove amenity"""
            first_or_default = next(
                    (a for a in self.amenities if a.id == amenity.id),
                    None)
            if first_or_default:
                self.amenities.remove(first_or_default)
                return True
            return False

        def add_amenity(self, amenity):
            """add amenity to place"""
            if amenity not in self.amenities:
                self.amenities.append(amenity)
                return True
            return False

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """reviews property getter"""
            from models.review import Review
            all_reviews = models.storage.all(Review).values()
            return [
                    review for review in all_reviews
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """amenities property getter"""
            from models.amenity import Amenity
            amenities = set(
                    [
                        models.storage.get(Amenity, amenity_id)
                        for amenity_id in self.amenity_ids])
            amenities.reduce(None)
            return list(amenities)

        def remove_amenity(self, amenity):
            """remove amenity id"""
            try:
                self.amenity_ids.remove(amenity.id)
                return True
            except ValueError:
                return False

        def add_amenity(self, amenity):
            if amenity.id not in self.amenity_ids:
                self.amenity_ids.append(amenity.id)
                return True
            return False

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)

    def to_dict(self, add_password=False):
        """Override the BaseModel to_dict"""
        dictionary = super().to_dict(add_password)
        if 'amenities' in dictionary:
            del dictionary['amenities']
        if 'reviews' in dictionary:
            del dictionary['reviews']
        return dictionary
