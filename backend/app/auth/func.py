import requests
from functools import wraps
from flask import jsonify, request, abort
from google.oauth2 import id_token
from google.auth.transport import requests
from app.models import User

CLIENT_ID = '828759278900-8mqop912snst4l66v0auh6c958tn1shf.apps.googleusercontent.com'


def requires_auth():
    # decorator for checking authentication & permission
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            idinfo = verify_token(token)
            user = getUser(idinfo['email'])
            return f(user, *args, **kwargs)
        return wrapper
    return requires_auth_decorator


def get_token_auth_header():
    token = request.headers.get('Authorization')
    if token is None:
        return abort(401)
    return token


def verify_token(token):
    try:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        return idinfo

    except Exception as e:
        print(e)
        return abort(401)


def getUser(email):
    user = User.query.filter(User.email == email).first()
    return user
