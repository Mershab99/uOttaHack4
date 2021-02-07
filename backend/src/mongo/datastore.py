import os
from datetime import datetime
from pymongo import MongoClient


class Datastore:
    def __init__(self, collection):
        self.db = MongoClient(
            host=os.environ['MONGO_HOST'], port=int(os.environ['MONGO_PORT']),
            username=os.environ['MONGO_USERNAME'], password=os.environ['MONGO_PASSWORD']
        ).get_database(os.environ['MONGO_DB'])
        self.collection = self.db.get_collection(collection)


class DataLake(Datastore):
    def __init__(self):
        super().__init__('lake_sani')

    def flow_in(self, key, data):
        self.collection.insert_one(
            {
                'key': key,
                'data': data,
                'insert_time': datetime.now()
            }
        )

    def find_by_key(self, key):
        obj = self.collection.find_one({
            'key': key
        })
        if obj is None:
            raise KeyError("No object found for key:{}".format(key))
        obj.pop('_id')
        return obj


LAKE_INSTANCE = DataLake()
