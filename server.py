import json
from flask import Flask, jsonify, request, session
from flask_session import Session
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from dotenv import load_dotenv
from controllers import dogcat_api
from uuid import uuid4
import cloudinary
import cloudinary.uploader

load_dotenv()
# from controllers import dogs

#current list of pets (feel free to add as many as you want)
def signup():
    data = request.get_json()
    username = data.get('userName')
    password = data.get('password')
    # if not username or not password:
    #     return jsonify({'error': 'Incorect credintials'}), 409
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username exists'})
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "username": user.username,
    }), 200

def signin():
    data = request.get_json()
    username = data.get('userName')
    password = data.get('password')
    print(username)
    print(password)
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Unauthorized"}), 401
    print(user)
    session["id"] = user.id
    return jsonify({
        "id": user.id,
        "username": username,
    })

# def get_users():
#     user_id = session.get("id")

#     if not user_id:
#         return jsonify({"error": "Unauthorised"}), 401

#     user = User.query.filter_by(id=user_id).first()
#     return jsonify({
#         "id": user.id,
#         "username": user.username
#     })

def get_users():
    user_id = session.get("id")

    if not user_id:
        return jsonify({"error": "Unauthorised"}), 401
    
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify({
            "id": user.id,
            "username": user.username
        })

    service = Services.query.filter_by(id=user_id).first()
    if service:
        return jsonify({
            "id": service.id,
            "username": service.username
        })

    return jsonify({"error": "User or Service not found"}), 404

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

def update_password_id(user_id, new_password):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404
    else:
        user.password = new_password
        db.session.commit()

        return jsonify({"id": user.id, "password": user.password})


server = Flask(__name__)
CORS(server, supports_credentials=True)
#### Added to make tests work
server.config['SESSION_TYPE'] = 'filesystem'
####
server.config['SECRET_KEY'] = 'supersecret'
SESSION_PERMANENT = False
SESSION_TYPE = 'sqlalchemy'
Session(server)

server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(server)

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(35), unique=True)
    password = db.Column(db.Text, nullable=False)
    pets = db.relationship('Pet', backref='owner', lazy=True)

    def check_password(self, password):
        return self.password == password

class Pet(db.Model):
    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    animal_type = db.Column(db.String(50), nullable=False)
    animal_age= db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
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
    sender_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    sender_service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=True)
    content = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "sender_user_id": self.sender_user_id,
            "sender_service_id": self.sender_service_id,
            "content": self.content,
            "conversation_id": self.conversation_id
        }


class Services(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(35), unique=True)
    email = db.Column(db.String(35), unique=True)
    password = db.Column(db.Text, nullable=False)
    profile = db.relationship('ServiceProfile', backref='service', lazy='dynamic')

    def check_password(self, password):
        return self.password == password

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'password' : self.password
        }

class ServiceProfile(db.Model):
    __tablename__ = "service_profile"
    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35))
    address = db.Column(db.String(50))
    city = db.Column(db.String(35))
    icon = db.Column(db.String(100))
    picture = db.Column(db.String(100))
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
            'icon': self.icon,
            'picture': self.picture,
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
# @server.route('/service-register', methods=['POST'])
# def create_service_provider():
#     data = request.get_json()
#     username = data["username"]
#     email = data["email"]
#     password = data["password"]
#     service = Services(username = username, email = email, password= password)
#     db.session.add(service)
#     db.session.commit()
#     return {'token' : service.id, "username": service.username }, 201

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
    # icon = data["icon"],
    # picture = data["picture"],
    service = s)
    db.session.add(profile)
    db.session.commit()
    return {'p_id' : profile.id},201


#add profile picture  for service provider
@server.route('/service/add-picture/<int:id>', methods=['POST'])
def create_service_provider_pictures(id):
   
    data= request.get_json()
    picture = data["picture"]
    s_profile = ServiceProfile.query.filter_by(s_id = id).first()
    s_profile.picture = picture
    db.session.commit()
    return {'s_id':id}

    #add profile  icon for service provider
@server.route('/service/add-icon/<int:id>', methods=['POST'])
def create_service_provider_icons(id):
    data= request.get_json()
    icon = data["icon"]
    s_profile = ServiceProfile.query.filter_by(s_id = id).first()
    s_profile.icon = icon
    db.session.commit()
    return {'s_id':id}

#retrieve all service provider profiles

@server.route('/services', methods=['GET'])
def get_all_services():
    services = ServiceProfile.query.all()
    return jsonify(services=[i.serialize for i in services])

#get service provider profile by profile id
@server.route('/services/<int:id>', methods=['GET'])
def get_services_by_id(id):
    service = Services.query.get_or_404(int(id))
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

# @server.route('/services/service-login', methods=['POST'])
# def provider_login():
#     data = request.get_json()
#     user = Services.query.filter_by(username = data["username"]).first()
#     user_email = Services.query.filter_by(email = data["userEmail"]).first()
#     if user or user_email:
#         if user.password == data["password"]:
#             return jsonify(token = user.id), 200
#         else:
#             return jsonify(error="wrong password"), 401
#     else:
#         return jsonify(error="username does not exist"), 402

@server.route('/services/service-login', methods=['POST'])
def provider_login():
    data = request.get_json()
    print(data)
    username = data['serviceName']
    print(username)
    email = data['serviceEmail']
    password = data['servicePassword']
    service = Services.query.filter_by(username=username).first()
     
    
    if service and service.password == password:
        session["id"] = service.id
        return jsonify({
            "id": service.id,
            "serviceName": service.username,
            "email": service.email
        })
    else:
        return jsonify({"error": "Unauthorized"}), 401   
   



#delete service provider and profile
@server.route('/services/providers/<int:id>', methods=['DELETE'])
def delete_provider(id):
    provider = Services.query.get(int(id))
    profile = ServiceProfile.query.filter_by(s_id = id).first()
    if provider:
        if profile:
            db.session.delete(profile)
        db.session.delete(provider)
        db.session.commit()
        return {"response":"Provider successfully deleted"}, 202
    else:
        return {"Error":"Provider does not exist"}, 404



@server.route('/register', methods=['POST'])
def register():
    return signup()

@server.route('/login', methods=['POST'])
def login():
    return signin()

@server.route('/user', methods=['GET'])
def get_uses():
    return get_users()

@server.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    return get_user_id(id)

@server.route('/users/<string:username>', methods=['GET'])
def get_user_by_name(username):
    return get_user_name(username)

@server.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    name = request.json.get('new_username')
    return update_user_id(id, name)

@server.route('/users/<int:id>', methods=['PUT'])
def update_password(id):
    return update_password_id(id)

@server.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    return delete_user_id(id)


####################  Messaging   #######################################################


@server.route("/conversations", methods=["POST"])
def create_conversation():

    user_id = request.json.get("user_id")
    service_id = request.json.get("service_id")

    user = User.query.get(user_id)
    service = Services.query.get(service_id)
    if not user or not service:
        return({"error": "User or service not found"}), 404

    conversation = Conversation(user_id=user_id, service_id=service_id)
    db.session.add(conversation)
    db.session.commit()

    return jsonify({"message": "Conversation created successfully"}), 201

@server.route("/conversations/<int:conversation_id>/messages", methods=["POST"])
def add_message(conversation_id):
    sender_id = int(request.json.get("sender_id"))
    content = request.json.get("content")

    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return {"error": "Conversation not found"}, 404

    if sender_id not in [conversation.user_id, conversation.service_id]:
        return {"error": "Sender is not a participant in the conversation"}, 404

    if sender_id == conversation.user_id:
        sender_user_id = sender_id
        sender_service_id = None
    else:
        sender_user_id = None
        sender_service_id = sender_id

    message = Message(sender_user_id=sender_user_id, sender_service_id=sender_service_id, content=content, conversation_id=conversation_id)
    db.session.add(message)
    db.session.commit()

    return jsonify({"message": "Message added successfully"}), 201

@server.route("/conversations", methods=["GET"])
def get_conversations_by_user():
    user_id = request.args.get("user_id")

    conversations = Conversation.query.filter(
        or_(Conversation.user_id == user_id, Conversation.service_id == user_id)
    ).all()

    conversation_list = []
    for conversation in conversations:
        user = User.query.get(conversation.user_id)
        service = Services.query.get(conversation.service_id)

        conversation_dict = {
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

        conversation_list.append({
            "conversation": conversation_dict,
            "user": user_json,
            "service": service_json
        })

    return jsonify({"conversations": conversation_list}), 200

@server.route("/conversations/<int:conversation_id>/messages", methods=["GET"])
def get_messages(conversation_id):

    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return {"error": "Conversation not found"}

    messages = Message.query.filter_by(conversation_id=conversation_id).all()

    message_list = []
    for message in messages:
        sender_id = message.sender_user_id or message.sender_service_id
        sender = User.query.get(sender_id) if message.sender_user_id else Services.query.get(sender_id)
        message_dict = {
            "id": message.id,
            "sender": sender.username,
            "content": message.content
        }
        message_list.append(message_dict)

    return jsonify({"messages": message_list}), 200

@server.route('/service-register', methods=['POST'])
def create_service_provider():
    data = request.get_json()
    username = data["serviceName"]
    email = data["serviceEmail"]
    password = data["servicePassword"]
    service = Services(username = username, email = email, password= password)
    db.session.add(service)
    db.session.commit()
    return {'id' : service.id, "username": service.username }, 201


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


@server.route('/pets/upload', methods=['POST'])
def upload():
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")
    secure = os.getenv("CLOUDINARY_SECURE") == "True"

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=secure
    )

    url = None
    if request.method == 'POST':
        file_to_upload = (request.files['image'])
        server.logger.info('%s file_to_upload', file_to_upload)
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload, public_id=file_to_upload.filename)
            server.logger.info(upload_result)
            url = upload_result.get('url')
            #user_id = get_user_id() 
            # user_profile = UserProfile.query.filter_by(user_id=user_id).first() 
            # user_profile.image_url = url
            # db.session.commit()


    return jsonify({'url': url})

@server.route('/users/<int:user_id>/pets', methods=['GET'])
def get_user_pets(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    pets = [pet.__dict__ for pet in user.pets]
    for pet in pets:
        pet.pop('_sa_instance_state')

    return jsonify(pets)

@server.route('/users/<int:user_id>/pets', methods=['POST'])
def create_pet(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    # Get pet data from request
    data = request.get_json()
    name = data.get('name')
    animal_type = data.get('animal_type')
    animal_age = data.get('animal_age')
    comment = data.get('comment')

    # Create new pet
    pet = Pet(
        name=name,
        animal_type=animal_type,
        animal_age=animal_age,
        comment=comment,
        owner=user
    )

    # Add and commit pet to database
    db.session.add(pet)
    db.session.commit()

    # Return new pet ID as response
    return jsonify({'id': pet.id})



# class Pet(db.Model):
#     id = db.Column(db.String(50), primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     age = db.Column(db.Integer, nullable=True)
#     species = db.Column(db.String(50), nullable=False)
#     instructions = db.Column(db.Text)

#     def __repr__(self):
#         return f'<Pet {self.id}>'

# @server.route('/upload/pet-profile', methods=['POST'])
# def add_pet():
#     data = request.json
#     pet = Pet(id=data['id'], name=data['name'], age=data['age'], species=data['species'], instructions=data.get('instructions'))
#     db.session.add(pet)
#     db.session.commit()
#     return jsonify({'message': 'Pet Profile added successfully'})

# @server.route('/upload/pet-profile/<id>', methods=['GET'])
# def get_pet(id):
#     pet = Pet.query.get(id)
#     if pet:
#         return jsonify({'id': pet.id, 'name': pet.name, 'age': pet.age, 'species': pet.species, 'instructions': pet.instructions})
#     else:
#         return jsonify({'message': 'Pet Profile not found'})


def run_db():
    app = server
    with app.app_context():
        # db.drop_all()
        db.create_all()
    return app
    
run_db()

