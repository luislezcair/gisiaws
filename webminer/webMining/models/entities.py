### Definir entidades y crear la base de datos en SQLite
from pony.orm import *

# db = Database("sqlite", "database.sqlite", create_db=True)
# db = Database("sqlite", "../../../gisiaws.sqlite3", create_db=True)
db = Database('mysql', host='localhost', user='root', passwd='motocross1' , db="gisiaws")
class Cloud(db.Entity):
    searchKey=PrimaryKey(str)
    structures=Required(str)

class WSRequest(db.Entity):
    _table_ = "searchkeyws_wsfilteredurlsrequest"
    id = PrimaryKey(int, auto=False)
    id_proyecto = Required(int)
    nombre_directorio = Required(str)
    urls = Set("Url")
    ws_request = Optional("WsRequestState")

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
    search_keys = Required("WSRequest")


db.generate_mapping(create_tables=True)
