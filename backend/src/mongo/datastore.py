import os
from datetime import datetime

from pymongo import MongoClient


class Datastore:
    def __init__(self, collection):
        self.db = MongoClient(
            host=os.environ['MONGO_HOST'], port=int(os.environ.get('MONGO_PORT', 27017)),
            username=os.environ.get('MONGO_USERNAME', ""), password=os.environ.get('MONGO_PASSWORD', "")
        ).get_database(os.environ['MONGO_DB'])
        self.collection = self.db.get_collection(collection)


class DataLake(Datastore):
    def __init__(self):
        super().__init__('data_lake')

    def flow_in(self, key, data):
        flow = {
            'key': key,
            'data': data,
            'insert_time': datetime.now().__str__()
        }

        if self.collection.find_one({'key': key}) is None:
            self.collection.insert_one(flow)
        else:
            self.collection.replace_one({'key': key}, flow)
        return flow

    def find_by_key(self, key):
        obj = self.collection.find_one({
            'key': key
        })
        if obj is None:
            raise KeyError("No object found for key:{}".format(key))
        obj.pop('_id')
        return obj


LAKE_INSTANCE = DataLake()
