#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import hashlib
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        __password = Column('password', String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")

        @hybrid_property
        def password(self):
            return self.__password

        @password.setter
        def password(self, pwd):
            self.__password = hashlib.md5(pwd.encode()).hexdigest()

    else:
        email = ""
        __password = ""
        first_name = ""
        last_name = ""

        @property
        def password(self):
            return self.__password

        @password.setter
        def password(self, pwd):
            self.__password = hashlib.md5(pwd.encode()).hexdigest()

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def to_dict(self, add_password=False):
        """overriding to_dict method"""
        return {
            key: value
            for key, value in super().to_dict(add_password).items()
            if key not in ('places', 'reviews')}
