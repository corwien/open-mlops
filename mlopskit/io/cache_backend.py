from pathlib import Path
from contextlib import contextmanager
from typing import Any, Iterator, List, Optional
import shutil

import diskcache as dc


@contextmanager
def database_connection(dbpath=None) -> Iterator[Any]:
    if dbpath is None:
        database_path = Path(Path("./").parent, "cache")
    else:
        database_path = dbpath
    cache = dc.Cache(database_path)
    try:
        with cache.transact():
            yield cache
    finally:
        cache.close()

def get_data_by_cache(key,db_path=None):
    with database_connection(dbpath=db_path) as db:
        data = db.get(key)
        
    return data

def set_data_by_cache(key,value,db_path=None):
    with database_connection(dbpath=db_path) as db:
        db[key]=value        
    return True
