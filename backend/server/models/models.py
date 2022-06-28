from pyjackson import dumps, loads
from sqlalchemy import (Column, DateTime, 
                        ForeignKey, Integer,
                        String, Text, UniqueConstraint,
                        Float,CheckConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar
from abc import abstractmethod

from .views import (User)


SQL_OBJECT_FIELD = '_sqlalchemy_object'

Base = declarative_base()
Mem_Choices = ["ADMIN","TESTER","DEV"]
    


T = TypeVar('T')
S = TypeVar('S', bound='Attaching')


class Attaching:
    id = ...
    name = ...

    def attach(self, obj):
        setattr(obj, SQL_OBJECT_FIELD, self)
        return obj



    @classmethod
    @abstractmethod
    def get_kwargs(cls, obj: T) -> dict:
        pass  # pragma: no cover

    @abstractmethod
    def to_obj(self) -> T:
        pass  # pragma: no cover
    
class SUsers(Base,Attaching):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    mobile = Column(String(11), unique=False, nullable=False)
    password = Column(String(200), unique=False, nullable=False)
    email = Column(String(100), unique=False, nullable=False)
    
    creation_date = Column(DateTime, unique=False, nullable=False)
    

    def to_obj(self) -> User:
        user = User(id=self.id,
                    name=self.name,
                    mobile=self.mobile,
                    creation_date=self.creation_date,
                    password=self.password,
                    email=self.email
                   )
        return self.attach(user)