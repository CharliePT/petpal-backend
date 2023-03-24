from models import User
from flask import jsonify, request
from server import db

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
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({
        "id": user.id,
        "username": user.username
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