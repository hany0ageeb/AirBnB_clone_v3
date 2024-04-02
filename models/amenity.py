#!/usr/bin/python
""" holds class Amenity"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Representation of Amenity """
    if models.storage_t == 'db':
        from models.place import place_amenity
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship(
                'Place',
                secondary=place_amenity,
                back_populates='amenities')
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)

    def to_dict(self, add_password=False):
        """override to_dict"""
        return {
            key: value
            for key, value in super().to_dict(add_password).items()
            if key != 'place_amenities'}
