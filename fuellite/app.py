from fuelparse import prices

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class FuelPrice(Resource):
    def get(self):
        return {'fuelprice': 'not implimented'}


api.add_resource(FuelPrice, '/')

if __name__ == '__main__':
    app.run(debug=True)
