import os
from crate import client

CRATEDB_URI = os.environ['CRATE_HOST_PORT'] # CRATEDB_URI = 'http://crate-db:4200'

def dbConnection():
    try:
        db = client.connect(CRATEDB_URI)
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db