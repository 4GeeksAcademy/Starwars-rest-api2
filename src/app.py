"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    all_users= list(map(lambda x: x.serialize(), all_users))
    return jsonify(all_users), 200
    #response =[]
    #for user in all_users:
        #response.append(user.serialize())
    #return jsonify(response), 200

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user= User(
        email= data.get("email"),
        password = data.get("password"),
        is_active = data.get("is_active")
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = Planets.query.all()
    all_planets= list(map(lambda x: x.serialize(), all_planets))
    return jsonify(all_planets), 200

@app.route('/planets', methods=['POST'])
def add_planet():
    data = request.get_json()
    new_planet= Planets(
        name = data.get("name"),
        terrain = data.get("terrain"),
        climate = data.get("climate")
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

@app.route('/characters', methods=['GET'])
def get_all_characters():
    all_characters = Characters.query.all()
    all_characters= list(map(lambda x: x.serialize(), all_characters))
    return jsonify(all_characters), 200

@app.route('/characters', methods=['POST'])
def add_character():
    data = request.get_json()
    new_character= Characters(
        name= data.get("name"),
        gender = data.get("gender"),
        height = data.get("height")
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    single_user = User.query.get(user_id)
    single_user = single_user.serialize()
    
    return jsonify(single_user), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    single_planet = Planets.query.get(planet_id)
    single_planet = single_planet.serialize()    
    return jsonify(single_planet), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_single_character(character_id):
    single_character = Characters.query.get(character_id)
    single_character = single_character.serialize()    
    return jsonify(single_character), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
