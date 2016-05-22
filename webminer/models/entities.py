### Definir entidades y crear la base de datos en SQLite
from pony.orm import *
from db_local import *


db = getDb()
# crear archivo db_local con el siguiente codigo
# def getDb():
#     db = Database('mysql', host='', user='', passwd='' , db="") -> para mysql
#     db = Database("sqlite", "database.sqlite", create_db=True) -> para sqlite
#     return db

class Cloud(db.Entity):
    searchKey=PrimaryKey(str)
    structures=Required(str)

class WSRequest(db.Entity):
    _table_ = "searchkeyws_wsfilteredurlsrequest"
    id = PrimaryKey(int, auto=False)
    id_proyecto = Required(int)
    nombre_directorio = Required(str)
    request_id = Required(int)
    urls = Set("Url")

class Url(db.Entity):
    _table_ = "searchkeyws_filteredurl"
    id = PrimaryKey(int, auto=False)
    orden = Required(int)
    url = Required(str)
    request_id = Required(WSRequest)

class WsRequestState(db.Entity):
    _table_ = "wsrequest_state"
    id = PrimaryKey(int, auto=True)
    estado = Required(str)
    stop = Required(bool)
    search_keys = Required("Searchkeys_wsrequest")

class Searchkeys_wsrequest(db.Entity):
    _table_ = "searchkeyws_wsrequest"
    id = PrimaryKey(int)
    id_proyecto = Required(int)
    nombre_directorio = Required(str)
    ws_request = Optional("WsRequestState")

db.generate_mapping(create_tables=True)
