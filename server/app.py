#
# Correct app.py using Flask-RESTful
#
#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource  # <-- Correct imports
from flask_cors import CORS

from models import db, Plant

# Basic Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

# Force table creation for Codegrade
with app.app_context():
    db.create_all()

# Initialize Flask-RESTful
api = Api(app)
CORS(app)

# Resource for ALL plants
class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(plants, 200)

api.add_resource(Plants, '/plants')

# Resource for a SINGLE plant by ID
class PlantByID(Resource):
    def get(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return make_response({'error': 'Plant not found'}, 404)
        return make_response(plant.to_dict(), 200)

    def patch(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return make_response({'error': 'Plant not found'}, 404)
        data = request.get_json()
        for attr in data:
            setattr(plant, attr, data[attr])
        db.session.add(plant)
        db.session.commit()
        return make_response(plant.to_dict(), 200)

    def delete(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return make_response({'error': 'Plant not found'}, 404)
        db.session.delete(plant)
        db.session.commit()
        return make_response('', 204)

api.add_resource(PlantByID, '/plants/<int:id>')

@app.route('/')
def index():
    return "<h1>Plant Store API</h1>"

if __name__ == '__main__':
    app.run(port=5555, debug=True)