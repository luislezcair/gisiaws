# db = Database("sqlite", "database.sqlite", create_db=True)
# db = Database("sqlite", "../../../gisiaws.sqlite3", create_db=True)
def getDb():
    db = Database('mysql', host='localhost', user='root', passwd='motocross1' , db="gisiaws")
    return db
