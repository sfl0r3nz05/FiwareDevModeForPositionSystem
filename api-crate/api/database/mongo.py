import os
from pymongo.mongo_client import MongoClient

MONGO_URI = os.environ['MONGODB_URI'] #MONGO_URI = 'mongodb://mongo-db'

def dbConnection(org):
    try:
        client = MongoClient(MONGO_URI)
        collection = "orion-"+org
        db = client[collection]
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db