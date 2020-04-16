import requests
from flask import request, Blueprint, jsonify, abort

user = Blueprint('user', __name__)
