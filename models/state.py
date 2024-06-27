#!/usr/bin/python3
""" State Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv

class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cities = []

    def save(self):
        for city in self.cities:
            city.save()
        super().save()

    def delete(self):
        for city in self.cities:
            city.delete()
        super().delete()

    def to_dict(self):
        state_dict = super().to_dict()
        state_dict['cities'] = [city.to_dict() for city in self.cities]
        return state_dict

