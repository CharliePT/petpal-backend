import json
from flask import Flask, jsonify, request 
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
# from data.pets import pets as pet_list
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
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(35), unique=True)
    password = db.Column(db.Text, nullable=False)

class Services(db.Model):
    # __tablename__ = "service_providers"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(35), unique=True)
    email = db.Column(db.String(35), unique=True)
    password = db.Column(db.Text, nullable=False)
    profile = db.relationship('ServiceProfile', backref='service', lazy='dynamic')

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'password' : self.password
        }

class ServiceProfile(db.Model):
    # __tablename__ = "service_profile"
    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35))
    address = db.Column(db.String(50))
    city = db.Column(db.String(35))
    postcode = db.Column(db.String(15))
    phone = db.Column(db.String(35))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    dog =  db.Column(db.Boolean, default=False)
    cat = db.Column(db.Boolean, default=False)
    rabbit = db.Column(db.Boolean, default=False)
    bird = db.Column(db.Boolean, default=False)
    reptile = db.Column(db.Boolean, default=False)
    daily_care = db.Column(db.Boolean, default=False)
    boarding_hotel = db.Column(db.Boolean, default=False)
    pet_sitter = db.Column(db.Boolean, default=False)
    dog_walker = db.Column(db.Boolean, default=False)
    vet = db.Column(db.Boolean, default=False)
    grooming = db.Column(db.Boolean, default=False)
    trainer = db.Column(db.Boolean, default=False)
    s_id = db.Column(db.Integer, db.ForeignKey('services.id'))

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'address' : self.address,
            'city' : self.city,
            'postcode' : self.postcode,
            'phone' : self.phone,
            'latitude' : self.latitude, 
            'longitude' : self.longitude,
            'dog' :  self.longitude,
            'cat' : self.cat,
            'rabbit' : self.rabbit,
            'bird' : self.bird,
            'reptile' : self.reptile,
            'daily_care' : self.daily_care,
            'boarding_hotel' :self.boarding_hotel,
            'pet_sitter' : self.pet_sitter,
            'dog_walker' : self.dog_walker,
            'vet' : self.vet,
            'grooming' : self.grooming,
            'trainer' : self.trainer,
            's_id' : self.s_id
        }





@server.route('/')
def home():
    return jsonify({"Welcome": 'Welcome to the petpal API'})
    

#routes to add service provider
@server.route('/service-register', methods=['POST'])
def create_service_provider():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]
    service = Services(username = username, email = email, password= password)
    db.session.add(service)
    db.session.commit()
    return {'token' : service.id, "username": service.username }, 201

#route to create service provider profile

@server.route('/service-profile', methods=['POST'])
def create_service_provider_profile():
    data = request.get_json()
    s = Services.query.get(data["sp_id"])
    profile = ServiceProfile(name = data["name"],
    address = data["address"],
    city = data["city"],
    postcode = data["post_code"],
    phone = data["phone"],
    latitude = data["latitude"],
    longitude = data["longitude"],
    dog =  data["dog"],
    cat = data["cat"],
    rabbit = data["rabbit"],
    bird = data["bird"],
    reptile = data["reptile"],
    daily_care = data["daily_care"],
    boarding_hotel = data["boarding_hotel"],
    pet_sitter = data["pet_sitter"],
    dog_walker = data["dog_walker"],
    vet = data["vet"],
    grooming = data["grooming"],
    trainer = data["trainer"],
    service = s)
    db.session.add(profile)
    db.session.commit()
    return {'p_id' : profile.id}

#retrieve all service provider profiles

@server.route('/services', methods=['GET'])
def get_all_services():
    services = ServiceProfile.query.all()
    return jsonify(services=[i.serialize for i in services])

#get service provider profile by id
@server.route('/services/<int:id>', methods=['GET'])
def get_services_by_id(id):
    service = ServiceProfile.query.get_or_404(int(id))
    return jsonify(service.serialize)


#get service provider account by id

@server.route('/services/providers/<int:id>', methods=['GET'])
def get_providers_by_id(id):
    service = Services.query.get_or_404(int(id))
    return jsonify(service.serialize)

#delete service provider and profile
@server.route('/services/providers/delete/<int:id>', methods=['GET'])
def delete_provider(id):
    provider = Services.query.get(int(id))
    profile = ServiceProfile.query.filter_by(s_id = id).first()
    if provider:
        if profile:
            db.session.delete(profile)
        db.session.delete(provider)
        db.session.commit()
        return {"response":"Provider successfully deleted"}, 201
    else:
        return {"Error":"Provider does not exist"}, 404

    



#route for all pets 
@server.route('/pets', methods=['GET'])
def pets():
    return pets
#routes for dogs

@server.route('/pets/dogs')
def dog():
    access_token = os.environ.get('DOG_KEY')
    api = dogcat_api("https://api.thedogapi.com/v1", access_token)
    data = api.get_data('breeds')
    return data

@server.route('/pets/cats')
def cat():
    access_token = os.environ.get('DOG_KEY')
    api = dogcat_api("https://api.thecatapi.com/v1", access_token)
    data = api.get_data('breeds')
    return data



def run_db():
    app = server
    with app.app_context():
        # db.drop_all()
        db.create_all()
    return app

run_db()

pets={
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
