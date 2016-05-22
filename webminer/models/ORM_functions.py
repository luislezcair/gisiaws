from entities import *

def save(sk,structs):
    with db_session:
        Cloud(searchKey=sk,structures=structs)

def get(sk):
    with db_session:
        search=Cloud.get(searchKey=sk)
        return search

def drop():db.drop_all_tables(with_all_data=True)
    #with db_session:
    #    db.drop_all_tables(with_all_data=True)
