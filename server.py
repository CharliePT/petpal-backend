import json
from flask import Flask, jsonify, request 
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from controllers import dogcat_api


load_dotenv()
# from controllers import dogs

#current list of pets (feel free to add as many as you want)


server = Flask(__name__)
CORS(server)

server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(server)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True)
    username = db.Column(db.String(35), unique=True)
    password = db.Column(db.Text, nullable=False)

pets_list = {
    "animals": [
        "Bird",
        "Cat",
        "Dog",
        "Fish",
        "Guinea Pig",
        "Hamster",
        "Iguana",
        "Jararaca",
        "Lizard",
        "Mouse",
        "Newt",
        "Owl",
        "Parakeet",
        "Rabbit",
        "Salamander",
        "Turtle",
        "Uromastyx lizard",
        "Vole",
        "Weasel",
        "Xolo Dog",
        "Yak",
        "Zebra Finch"
    ]
}

@server.route('/')
def home():
    return jsonify({"Welcome": 'Welcome to the petpal API'})
    

#route for all pets 
@server.route('/pets', methods=['GET'])
def pets():
    return pets_list

#routes for dogs

@server.route('/pets/dogs')
def dog():
    access_token = os.environ.get('DOG_KEY')
    api = dogcat_api("https://api.thedogapi.com/v1", access_token)
    data = api.get_data('breeds')
    return data



def run_db():
    app = server
    with app.app_context():
        db.drop_all()
        db.create_all()
    return app

run_db()