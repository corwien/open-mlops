#from pyjackson.decorators import make_string, type_field
import datetime
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class User:
    name:str
    mobile:str = None
    password:str= None
    email:str = None
    id: int = None
    creation_date: datetime.datetime = None
