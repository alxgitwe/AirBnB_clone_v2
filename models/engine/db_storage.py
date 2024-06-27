#!/usr/bin/python3
"""Database Storage"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class DBStorage:
    """Database Storage class"""

    def __init__(self):
        """Initialize the database connection"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{password}@{host}/{database}',
            pool_pre_ping=True
        )

        if env == "test":
            Base.metadata.drop_all(self.__engine)

        Session = sessionmaker(bind=self.__engine)
        self.__session = scoped_session(Session)

    def all(self, cls=None):
        """Return a dictionary of all objects"""
        obj_dict = {}
        if cls is None:
            for model in [State, City, User, Place, Amenity, Review]:
                for obj in self.__session.query(model).all():
                    key = f"{model.__name__}.{obj.id}"
                    obj_dict[key] = obj
        else:
            for obj in self.__session.query(cls).all():
                key = f"{cls.__name__}.{obj.id}"
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add a new object to the database"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the database"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)

    def close(self):
        """Close the database session"""
        self.__session.remove()

