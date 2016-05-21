### Definir entidades y crear la base de datos en SQLite
from pony.orm import *

db = Database("sqlite", "database.sqlite", create_db=True)

class Cloud(db.Entity):
    searchKey=PrimaryKey(str)
    structures=Required(str)

db.generate_mapping(create_tables=True)


