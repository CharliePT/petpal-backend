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
    
class Conversation(db.Model):
    __tablename__ = "conversations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    messages = db.relationship("Message", backref="conversation", lazy=True)

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "content": self.content,
            "conversation_id": self.conversation_id
        }

    
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


class ServiceCalendar(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    sp_id = db.Column(db.Integer)
    calendar = db.Column(db.Boolean, default=False)
    events = db.Column(db.String(10000))       
    
    @property
    def serialize(self):
        return {
            'sp_id' : self.sp_id,
            'calendar': self.calendar,
            'events':self.events
        }
    # conversation = Conversation.query.filter_by(id=conversation_id).join(Services).first()
    # service_username = conversation.service.username
@server.route('/')
def home():
    return jsonify({"Welcome": 'Welcome to the petpal API'})



#############################Service-providers###########################################

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

#route to add calendar to service provider profile
@server.route('/service/add-calendar', methods=['POST'])
def create_service_provider_calendar():
    data= request.get_json()
    sp_id = data["sp_id"]
    calendar = data["calendar"]
    is_calendar = ServiceCalendar.query.filter_by(sp_id =sp_id).first()
    if is_calendar:
        is_calendar.calendar = calendar
        db.session.commit()
        return {'sp_id': is_calendar.sp_id, 'calendar': is_calendar.calendar}, 201
    else:
        s_calendar = ServiceCalendar(sp_id = sp_id, calendar= calendar)
        db.session.add(s_calendar)
        db.session.commit()
        return {'id': s_calendar.id}, 200

#route to check if service provider has initialized calendar
@server.route('/service/calendar/<int:id>', methods=['GET'])
def get_service_provider_calendar(id):
    sp_id = id
    s_calendar = ServiceCalendar.query.filter_by(sp_id =sp_id).first()
    if s_calendar:
        return {'sp_id': s_calendar.sp_id, 'calendar': s_calendar.calendar}, 201
    else:
        return {'error': 'User calendar was not initialized'}, 404

#route to add events to service provider calendar
@server.route('/service/add-events/<int:id>', methods=['POST'])
def create_service_provider_calendar_events(id):
   
    data= request.get_json()
    print(data)
   
    events = data["events"]
    s_calendar = ServiceCalendar.query.filter_by(sp_id = id).first()
    s_calendar.events = events
    db.session.commit()
    return {'sp_id':s_calendar.sp_id, 'events': s_calendar.events}

#route to get all events of service provider
@server.route('/service/get-events/<int:id>', methods=['GET'])
def get_service_provider_calendar_events(id):
    sp_id = id
    s_calendar = ServiceCalendar.query.filter_by(sp_id =sp_id).first()
    return {'sp_id': s_calendar.sp_id, 'events': s_calendar.events }, 201


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
    return {'p_id' : profile.id},201

#retrieve all service provider profiles

@server.route('/services', methods=['GET'])
def get_all_services():
    services = ServiceProfile.query.all()
    return jsonify(services=[i.serialize for i in services])

#get service provider profile by profile id
@server.route('/services/<int:id>', methods=['GET'])
def get_services_by_id(id):
    service = ServiceProfile.query.get_or_404(int(id))
    return jsonify(service.serialize)

#get service provider profile by provider id
@server.route('/services/profile/<int:id>', methods=['GET'])
def get_services_by_provider_id(id):
    prof = ServiceProfile.query.filter_by(s_id = id).first()
    return jsonify(prof.serialize)

#get service provider account by id

@server.route('/services/providers/<int:id>', methods=['GET'])
def get_providers_by_id(id):
    service = Services.query.get_or_404(int(id))
    return jsonify(service.serialize)

#service provider log in

@server.route('/services/service-login', methods=['POST'])
def provider_login():
    data = request.get_json()
    user = Services.query.filter_by(username = data["username"]).first()
    user_email = Services.query.filter_by(email = data["username"]).first()
    if user or user_email:
        if user.password == data["password"]:
            return jsonify(token = user.id), 200
        else:
            return jsonify(error="wrong password"), 401
    else:
        return jsonify(error="username does not exist"), 402



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

    

################################# USERS  #################################################


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


####################  Messaging   #######################################################


@server.route("/conversations", methods=["POST"])
def create_conversation():
    # Get the user and service IDs from the request data
    user_id = request.json.get("user_id")
    service_id = request.json.get("service_id")

    # Check if the user and service exist
    user = User.query.get(user_id)
    service = Services.query.get(service_id)
    if not user or not service:
        return({"error": "User or service not found"})

    # Create a new conversation between the user and service
    conversation = Conversation(user_id=user_id, service_id=service_id)
    db.session.add(conversation)
    db.session.commit()

    return jsonify({"message": "Conversation created successfully"}), 201

@server.route("/conversations/<int:conversation_id>/messages", methods=["POST"])
def add_message(conversation_id):
    # Get the sender ID and message content from the request data
    sender_id = request.json.get("sender_id")
    content = request.json.get("content")

    # Check if the conversation exists
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return({"error": "Conversation not found"})

    # Check if the sender is a participant in the conversation
    if sender_id not in [conversation.user_id]:
        print(conversation.user_id)
        return({"error": "Sender is not a participant in the conversation"})

    # Create a new message in the conversation
    message = Message(sender_id=sender_id, content=content, conversation_id=conversation_id)
    db.session.add(message)
    db.session.commit()

    return jsonify({"message": "Message added successfully"}), 201

@server.route("/conversations", methods=["GET"])
def get_conversation():
    # Get the conversation ID from the request data
    conversation_id = request.args.get("conversation_id")

    # Check if the conversation exists
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return({"error": "Conversation not found"})

    # Get the user and service objects for the participants
    user = User.query.get(conversation.user_id)
    service = Services.query.get(conversation.service_id)

    # Serialize the conversation and participant objects to JSON format
    conversation_json = {
        "id": conversation.id,
        "user_id": conversation.user_id,
        "service_id": conversation.service_id
    }
    user_json = {
        "id": user.id,
        "username": user.username
    }
    service_json = {
        "id": service.id,
        "username": service.username
    }

    # Return the conversation and participant objects as a response
    return jsonify({
        "conversation": conversation_json,
        "user": user_json,
        "service": service_json
    }), 200



###################### external API    ###################################################


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
