from flask import Flask
from flask_restful import Resource, Api
from hashids import Hashids
from flask_restful import reqparse
from flask_restful import reqparse, abort, Api, Resource
import hashlib


app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('xxxx')

class Entry(Resource):
    def post(self):


        args = parser.parse_args()

        xxxx = args['xxxx']
        print(xxxx)
        return 201, 'Created'

    def get(self):


        return {'test': '123'}, 200

class Test(Resource):
    def get(self):
        print('test')
"""

curl http://localhost:5000/api/v1/entries -X POST -d '{"xxxx":"2016,All Causes,All causes,Alabama,52466,920.40 "}' -H "Content-Type: application/json"
"""

api.add_resource(Entry, '/api/v1/entries')
api.add_resource(Test, '/')



if __name__ == '__main__':
    app.run(host='localhost', port=5000)