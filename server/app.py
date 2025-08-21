# server/app.py
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Plant

app = Flask(__name__)

# SQLite DB file in server directory
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Optional helpers for local testing and UI
@app.get("/plants")
def list_plants():
    plants = Plant.query.order_by(Plant.id.asc()).all()
    return jsonify([p.to_dict() for p in plants]), 200

@app.get("/plants/<int:id>")
def get_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404
    return jsonify(plant.to_dict()), 200

# REQUIRED BY README
@app.patch("/plants/<int:id>")
def update_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    data = request.get_json() or {}
    if "is_in_stock" not in data:
        return jsonify({"error": "Request must include is_in_stock"}), 400

    value = data["is_in_stock"]
    if not isinstance(value, bool):
        return jsonify({"error": "is_in_stock must be a boolean"}), 400

    plant.is_in_stock = value
    db.session.commit()
    return jsonify(plant.to_dict()), 200

# REQUIRED BY README
@app.delete("/plants/<int:id>")
def delete_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    db.session.delete(plant)
    db.session.commit()
    return "", 204

if __name__ == "__main__":
    app.run(port=5555, debug=True)