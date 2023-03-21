import json
from flask import Flask, jsonify, request 
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from data import pets as pet_list
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


@server.route('/')
def home():
    return jsonify({"Welcome": 'Welcome to the petpal API'})

#route for all pets 
@server.route('/pets', methods=['GET'])
def pets():
    return pet_list

#routes for dogs

# @server.route('/pets/dogs')
# def dog():
#     return dogs.dog_data


def run_db():
    app = server
    with app.app_context():
        db.drop_all()
        db.create_all()
    return app

run_db()