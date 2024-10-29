"""
This module takes care of starting the API Server, loading the DB, and adding the endpoints.
"""
import os
from MySQLdb import IntegrityError
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People, Favorites
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.url_map.strict_slashes = False

# Database configuration
db_url = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://") if db_url else "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.errorhandler(SQLAlchemyError)
def handle_database_error(error):
    return jsonify({"error": "Database error occurred", "message": str(error)}), 500


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# [GET] /user
@app.route('/user', methods=['GET'])
def handle_hello():
    return jsonify({"msg": "Hello, this is your GET /user response"}), 200

# People endpoints
@app.route('/people', methods=['GET', 'POST'])
def manage_people():
    if request.method == 'GET':
        return get_all_people()
    else:
        return create_people()

def get_all_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200

def create_people():
    data = request.json
    try:
        new_person = People(**data)  # Unpack data directly
        db.session.add(new_person)
        db.session.commit()
        return jsonify(new_person.serialize()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_database_error(e)

@app.route('/people/<int:people_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_person(people_id):
    if request.method == 'GET':
        return get_people_by_id(people_id)
    elif request.method == 'PUT':
        return update_people(people_id)
    else:
        return delete_people(people_id)

def get_people_by_id(people_id):
    person = People.query.get(people_id)
    return jsonify(person.serialize()) if person else ({"error": "Person not found"}, 404)

def update_people(people_id):
    data = request.json
    person = People.query.get(people_id)
    if not person:
        return jsonify({"error": "Person not found"}), 404

    for key, value in data.items():
        setattr(person, key, value)  # Update attributes dynamically

    try:
        db.session.commit()
        return jsonify(person.serialize()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_database_error(e)

def delete_people(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"error": "Person not found"}), 404

    try:
        db.session.delete(person)
        db.session.commit()
        return jsonify({"message": "Person deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_database_error(e)

# Planets endpoints
@app.route('/planets', methods=['GET', 'POST'])
def manage_planets():
    if request.method == 'GET':
        return get_all_planets()
    else:
        return create_planet()

def get_all_planets():
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

def create_planet():
    data = request.json
    try:
        new_planet = Planets(**data)  # Unpack data directly
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(new_planet.serialize()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_database_error(e)

@app.route('/planets/<int:planet_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_planet(planet_id):
    if request.method == 'GET':
        return get_planet_by_id(planet_id)
    elif request.method == 'PUT':
        return update_planet(planet_id)
    else:
        return delete_planet(planet_id)

def get_planet_by_id(planet_id):
    planet = Planets.query.get(planet_id)
    return jsonify(planet.serialize()) if planet else ({"error": "Planet not found"}, 404)

def update_planet(planet_id):
    data = request.json
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    for key, value in data.items():
        setattr(planet, key, value)  # Update attributes dynamically

    try:
        db.session.commit()
        return jsonify(planet.serialize()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_database_error(e)

def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    try:
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"message": "Planet deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_database_error(e)

# Users endpoints
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

# User favorites endpoints
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    favorites = Favorites.query.filter_by(user_id=user_id).all()
    return jsonify([fav.serialize() for fav in favorites]), 200

# Favorite endpoints
@app.route('/favorites/<string:fav_type>/<int:fav_id>', methods=['POST', 'DELETE'])
def manage_favorites(fav_type, fav_id):
    user_id = request.json.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    if request.method == 'POST':
        if fav_type == "planet":
            new_favorite = Favorites(user_id=user_id, planet_id=fav_id)
        elif fav_type == "person":
            new_favorite = Favorites(user_id=user_id, person_id=fav_id)
        else:
            return jsonify({"error": "Invalid favorite type"}), 400

        try:
            db.session.add(new_favorite)
            db.session.commit()
            return jsonify(new_favorite.serialize()), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Favorite already exists"}), 409

    elif request.method == 'DELETE':
        if fav_type == "planet":
            favorite = Favorites.query.filter_by(user_id=user_id, planet_id=fav_id).first()
        elif fav_type == "person":
            favorite = Favorites.query.filter_by(user_id=user_id, person_id=fav_id).first()
        else:
            return jsonify({"error": "Invalid favorite type"}), 400

        if not favorite:
            return jsonify({"error": "Favorite not found"}), 404

        try:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({"message": "Favorite deleted successfully"}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
