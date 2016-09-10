from pony.orm import *
import MySQLdb

class config(object):
    """docstring for config."""
    typedb = ""
    db = ""
    host = ""
    user = ""
    password = ""
    pathLog = ""
    repositoryPath = ""



    def __init__(self):
        super(config, self).__init__()

    def getDb(self):
        db = Database(self.typedb, host=self.host, user=self.user, passwd=self.password, db=self.db)
        return db

    def getDbProgress(self):
        db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db)
        return db