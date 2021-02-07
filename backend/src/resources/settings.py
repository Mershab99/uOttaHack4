from flask_restful import Resource, reqparse

from src.mongo.datastore import LAKE_INSTANCE

parser = reqparse.RequestParser()
parser.add_argument('data', type=dict, required=True)


class SettingsGet(Resource):
    @staticmethod
    def get():
        try:
            current_settings = LAKE_INSTANCE.find_by_key('settings')['data']
        except KeyError:
            return {
                'failure': "No current settings for system"
            }
        return {
            'current_settings': current_settings
        }


# WATCH INSERTIONS FOR NESTED 'data' OBJECTS
class SettingsUpdate(Resource):
    @staticmethod
    def post():
        data = parser.parse_args()
        old_settings = None
        try:
            #TEST
            old_settings = LAKE_INSTANCE.find_by_key('settings')
            old_settings = old_settings['data']
        finally:
            LAKE_INSTANCE.flow_in('settings', data)
            return {
                'old_settings': old_settings,
                'new_settings': data
            }
