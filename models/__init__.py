#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv
from models.city import City
from models.place import Place
from models.base_model import BaseModel
from models.user import User
from models.review import Review
from models.state import State
from models.amenity import Amenity


storage_type = getenv("HBNB_TYPE_STORAGE")

if storage_type == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()

else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
