from flask_restful import Resource, reqparse
from src.mongo.datastore import DataLake as dl

parser = reqparse.RequestParser()
#parser.add_argument('home_key', type=str, required=True)


class Settings(Resource):
    @staticmethod
    def get():
        data = parser.parse_args()
        x = 1
        #data["walkzone_start_x"]

    @staticmethod
    def post():
        data = parser.parse_args()
        test = check_setting_store()
        x = 1



def check_setting_store():
    try:
        setting = dl.find_by_key('setting')
        return setting
    except KeyError:
        return False
