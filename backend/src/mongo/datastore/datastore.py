import os

from pymongo import MongoClient


class Datastore:
    def __init__(self, collection):
        self.db = MongoClient(
            host=os.environ['MONGO_HOST'], port=int(os.environ['MONGO_PORT']),
            username=os.environ['MONGO_USERNAME'], password=os.environ['MONGO_PASSWORD']
        ).get_database(os.environ['MONGO_DB'])
        self.collection = self.db.get_collection(collection)
