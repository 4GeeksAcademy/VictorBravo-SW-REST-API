from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    climate = db.Column(db.String, unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    gravity = db.Column(db.String, unique=False, nullable=False)
    orbital_period = db.Column(db.Integer, unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    residents = db.Column(ARRAY(db.String), unique=False, nullable=True) # Array de residentes
    rotation_period = db.Column(db.Integer, unique=False, nullable=False)
    surface_water = db.Column(db.Integer, unique=False, nullable=False)
    created =db.Column(db.DateTime, nullable=False)
    edited = db.Column(db.DateTime, nullable=False)
    terrain = db.Column(db.String, unique=False, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Planetas(id={self.id}, name='{self.name}')>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter, 
            "gravity": self.gravity, 
            "orbital_period": self.orbital_period, 
            "population": self.population, 
            "residents": self.residents, 
            "rotation_period": self.rotation_period, 
            "surface_water": self.surface_water,
            "created": self.created.isoformat(), 
            "edited": self.edited.isoformat(),
            "terrain": self.terrain, 
            "url": self.url,
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    birth_year = db.Column(db.String, nullable=False)
    eye_color = db.Column(db.String, nullable=False)
    films = db.Column(ARRAY(db.String), nullable=True)  # Arrays de URLs de películas
    gender = db.Column(db.String, nullable=False)
    hair_color = db.Column(db.String, nullable=False)
    height = db.Column(db.String, nullable=False)
    homeworld = db.Column(db.String, nullable=False)  # URL del planeta natal
    mass = db.Column(db.String, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    skin_color = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    edited = db.Column(db.DateTime, nullable=False)
    species = db.Column(ARRAY(db.String), nullable=True)  # Arrays de URLs de especies
    starships = db.Column(ARRAY(db.String), nullable=True)  # Arrays de URLs de naves
    url = db.Column(db.String, unique=True, nullable=False)
    vehicles = db.Column(ARRAY(db.String), nullable=True)  # Arrays de URLs de vehículos

    def __repr__(self):
        return f"<People(id={self.id}, name='{self.name}')>"

    def serialize(self):
        return {
            "id": self.id,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "films": self.films,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "homeworld": self.homeworld,
            "mass": self.mass,
            "name": self.name,
            "skin_color": self.skin_color,
            "created": self.created.isoformat(),
            "edited": self.edited.isoformat(),
            "species": self.species,
            "starships": self.starships,
            "url": self.url,
            "vehicles": self.vehicles
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)

    # Clave única para evitar duplicados por usuario y tipo de favorito
    __table_args__ = (
        db.UniqueConstraint('user_id', 'planet_id', name='unique_favorite_planet'),
        db.UniqueConstraint('user_id', 'person_id', name='unique_favorite_person'),
    )

    def __repr__(self):
        return f"<Favorite(user_id={self.user_id}, planet_id={self.planet_id}, person_id={self.person_id})>"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "person_id": self.person_id,
        }

