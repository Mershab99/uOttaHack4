from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
#parser.add_argument('home_key', type=str, required=True)


class Settings(Resource):
    @staticmethod
    def get():
        data = parser.parse_args()
        #data["walkzone_start_x"]