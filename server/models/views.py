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

@dataclass
class AbExpCase:
    name: str
    data_campaign_id:int=None
    description: str = None
    id: int = None
    app_type: str = None
    user_id: int = None
    creation_date: datetime.datetime = None

@dataclass    
class AbExpOps:
    name: str
    alt_name:str
    exposure_ratio: str = None,
    id: int = None
    model_id:int=None
    model_name: str = None
    description:str=None
    ab_id: int = None
    creation_date: datetime.datetime = None

@dataclass 
class DataCampaign:
    name: str
    author:str
    description: str = None
    data_campaign_type:str = None
    id: int = None
    campaign_status:int=None
    online_date: datetime.datetime = None
    expire_date: datetime.datetime = None
    creation_date: datetime.datetime = None