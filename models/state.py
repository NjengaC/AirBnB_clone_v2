#!/usr/bin/python3
""" State Module for HBNB project """
import models
from sqlalchemy.orm import declarative_base, relationship
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
import shlex
from models.city import City


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", cascade='all, delete,\
                              delete-orphan', backref="state")
    else:
        @property
        def cities(self):
            """
            Get a list of City instances with
            state_id equals to the current State.id.
            """
            curr = models.storage.all()
            lists = []
            res = []
            for key in curr:
                city = key.replace('.', ' ')
                city = shlex.split(city)
                if (city[0] == 'City'):
                    lists.append(curr[key])
            for lis in lists:
                if (lis.state_id == self.id):
                    res.append(lis)
            return (res)
