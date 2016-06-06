from optparse import OptionParser
from models.entities import *


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-r", "--request", dest="request_id")

    (options, args) = parser.parse_args()
    request_id = options.request_id



    with db_session:
        estadoActual = WsRequestState.get(search_keys = request_id )
        estadoActual.stop = True    
        flush()
    #    estadoActual.estado = unicode(self.get_progress())
    #    commit()
