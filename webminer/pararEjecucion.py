from optparse import OptionParser
from models.entities import *


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-r", "--request", dest="request_id")

    (options, args) = parser.parse_args()
    request_id = options.request_id
#
#
#
#     with db_session:
#         estadoActual = WsRequestState.get(search_keys = request_id )
#         estadoActual.stop = True
#         flush()
#         print estadoActual.stop
#     #    estadoActual.estado = unicode(self.get_progress())
#     #    commit()

import MySQLdb

# connect
db = MySQLdb.connect(host="localhost", user="root", passwd="motocross1",db="gisiaws")

cursor = db.cursor()

# execute SQL select statement
cursor.execute("SELECT * FROM wsrequest_state WHERE search_keys ="+request_id)

# commit your changes
db.commit()

# get the number of rows in the resultset
numrows = int(cursor.rowcount)

# get and display one row at a time.
for x in range(0,numrows):
    row = cursor.fetchone()
    print row[0], "-->", row[1] , "-->" ,row[2]
