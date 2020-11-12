import os
from flask_cors import CORS
from flask import Flask, jsonify
from flask_restful import reqparse

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from src import routes

