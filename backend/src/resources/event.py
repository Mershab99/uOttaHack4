from flask_restful import Resource, reqparse

from src.mongo.datastore import LAKE_INSTANCE

parser = reqparse.RequestParser()
parser.add_argument('data', type=dict, required=True)


class GCloudEventPost(Resource):
    @staticmethod
    def post():
        data = parser.parse_args()
        flow = LAKE_INSTANCE.flow_in('gcloud', data)
        return flow


# WATCH INSERTIONS FOR NESTED 'data' OBJECTS
class SanitizationEventPost(Resource):
    @staticmethod
    def post():
        data = parser.parse_args()
        flow = LAKE_INSTANCE.flow_in('sanitizer', data['data'])
        return flow
