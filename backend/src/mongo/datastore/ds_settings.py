from src.mongo.datastore.datastore import Datastore


class SettingsManagerDatastore(Datastore):
    def __init__(self):
        super().__init__('settings')

    def save_setting(self, data):
        setting = self.collection.insert_one(data)
        return setting is not None
