import sys
from models.config import *
from models.entities import *

def main():
    print sys.argv
    if len(sys.argv) == 3 and sys.argv[1] == "-r":
       stopRequest(sys.argv[2])
    else:
        print "Argumento invalido"

def stopRequest(idRequest):
    with db_session:
        unRequest = WsRequestState.get(search_keys = idRequest)
        unRequest.stop = True
    print "Request Detenido"


if __name__ == "__main__":
    main()