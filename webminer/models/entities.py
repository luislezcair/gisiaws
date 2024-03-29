### Definir entidades y crear la base de datos en SQLite
from pony.orm import *
from config import *


config = config()
db = config.getDb()

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


class Searchkeys_searchkey(db.Entity):
    _table_ = "searchkeyws_searchkey"
    id = PrimaryKey(int)
    clave = Required(str)
    request_id = Required(int)


db.generate_mapping(create_tables=True)
