from flask import Flask
from flask_restful import Resource, Api
import requests
import json

app = Flask(__name__)
api = Api(app)

class Status(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(Status, '/status')

if __name__ == '__main__':
    app.run(debug=True)