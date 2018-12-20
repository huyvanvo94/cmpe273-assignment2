from flask import Flask
from flask_restful import reqparse, Api, Resource
from utils import md5

app = Flask(__name__)
api = Api(app)

# Store Entry
entries = {}

parser = reqparse.RequestParser()
parser.add_argument('xxxx')

class Entry(Resource):
    def post(self):
        try:
            args = parser.parse_args()

            xxxx = str(args['xxxx'])
            try:
                # hash(Year:Cause Name:State) => xxxx
                values = xxxx.split(',')
                # hash(year, cause1, cause2, state)
                tobehashed = "{}:{}{}:{}".format(values[0], values[1], values[2], values[3])

                key = md5(tobehashed)
                entries[key] = xxxx
            except:
                print('split error')
                key = md5(xxxx)
                entries[key] = xxxx

        except:
            print('error')
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

if __name__ == '__main__':
    app.run(host='localhost', port=5000)