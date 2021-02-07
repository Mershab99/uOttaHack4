from flask_restful import Resource


class Status(Resource):
    @staticmethod
    def get():
        return {
            'status': 'alive'
        }
