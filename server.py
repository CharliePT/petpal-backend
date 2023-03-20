from flask import Flask, jsonify, request 
from flask_cors import CORS


server = Flask(__name__)

@server.route('/')
def home():
    return "Flask backend"


