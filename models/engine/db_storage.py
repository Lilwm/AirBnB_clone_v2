#!/usr/bin/python3
"""SQL db engine class"""
import json
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

all_classes = {'User': User,'State': State, 
               'City': City, 'Amenity': Amenity,
               'Place': Place, 'Review': Review}

class DBStorage:
    """SQL db class"""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiation"""
        self.__engine = create_engine(
                "mysql+mysqldb://{}:{}@{}:3306/{}".format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB"),
            ),
            pool_pre_ping=True,
        )
        # drop tables if test environment
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query and return all objects by class/generally
        Return: dictionary (<class-name>.<object-id>: <obj>)
        """
        obj_dict = {}

        if cls:
            for row in self.__session.query(cls).all():
                # populate dict with objects from storage
                obj_dict.update({'{}.{}'.
                                format(type(cls).__name__, row.id,): row})
        else:
            for key, val in all_classes.items():
                for row in self.__session.query(val):
                    obj_dict.update({'{}.{}'.
                                    format(type(row).__name__, row.id,): row})
        return obj_dict

    def new(self, obj):
        """Add object to current database session"""
        self.__session.add(obj)

    def save(self):
        """Save"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from database session
        """
        if obj:
            # determine class from obj
            cls_name = all_classes[type(obj).__name__]

            # query class table and delete
            self.__session.query(cls_name).\
                filter(cls_name.id == obj.id).delete()

    def reload(self):
        """Create database session
        """
        # create session from current engine
        Base.metadata.create_all(self.__engine)
        # create db tables
        session = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        # previously:
        # Session = scoped_session(session)
        self.__session = scoped_session(session)

    def close(self):
        """calls session close"""
        self.__session.remove()
