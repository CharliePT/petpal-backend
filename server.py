import json
from flask import Flask, jsonify, request 
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from data import pets as pet_list
from dotenv import load_dotenv
# from controllers import signup, signin, get_user_id, get_user_name, update_user_id, delete_user_id

load_dotenv()
# from controllers import dogs

#current list of pets (feel free to add as many as you want)
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Incorect credintials'}), 409
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username exists'}), 409
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Success'}), 200

def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(username)
    print(password)
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Unauthorized"}), 401
    print(user)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "login": True
    })

def get_user_id(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({"error": "User does not exist"}), 404
    else:
        return jsonify({"id": user.id, "username": user.username})
    
def get_user_name(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"id": user.id, "username": user.username})
    
def delete_user_id(id):
    user = User.query.get(id)

    if user is None:
        return jsonify({"error": "User not found"}), 404
    else:
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"})

def update_user_id(user_id, new_username):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404
    else:
        user.username = new_username
        db.session.commit()

        return jsonify({"id": user.id, "username": user.username})



server = Flask(__name__)
CORS(server)

server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(server)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(35), unique=True)
    password = db.Column(db.Text, nullable=False)

    def check_password(self, password):
        return self.password == password


@server.route('/')
def home():
    return jsonify({"Welcome": 'Welcome to the petpal API'})


@server.route('/register', methods=['POST'])
def register():
    return signup()

@server.route('/login', methods=['POST'])
def login():
    return signin()

# @server.route('/users', methods=['GET'])
# def get_uses():
#     return get_users()

@server.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    return get_user_id(id)

@server.route('/users/<string:username>', methods=['GET'])
def get_user_by_name(username):
    return get_user_name(username)

@server.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    return update_user_id(id)

@server.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    return delete_user_id(id)


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