from flask import Flask
from flask_restful import Resource, Api
from hashids import Hashids
from flask_restful import reqparse
from flask_restful import reqparse, abort, Api, Resource
from utils import md5
import json
import pprint

app = Flask(__name__)
api = Api(app)


entries = {}

parser = reqparse.RequestParser()
parser.add_argument('xxxx')

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

class Entry(Resource):
    def post(self):

        args = parser.parse_args()

        xxxx = args['xxxx']
        key = md5(xxxx)

        entries[key] = xxxx
        return 201


    def get(self):

        content = {
                "num_entries" : len(entries),
                "entries" :
                [
                    entries
                ]
        }



        return content, 200

class Test(Resource):
    def get(self):
        return "Hello World"
"""

curl http://localhost:5000/api/v1/entries -X POST -d '{"xxxx":"2016,All Causes,All causes,Alabama,52466,920.40 "}' -H "Content-Type: application/json"
"""

api.add_resource(Entry, '/api/v1/entries')
api.add_resource(Test, '/')

"""
I think you get the key by using the hash function like key = hash("2016,All Causes,All Causes,Alabama,52466,920.40")
because that whole line is in quotation marks.
"""

if __name__ == '__main__':
    app.run(host='localhost', port=5000)