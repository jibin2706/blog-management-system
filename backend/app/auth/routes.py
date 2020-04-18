from flask import Blueprint, jsonify, request, abort
from app.auth.func import get_token_auth_header, verify_token
from app.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login_user():
    token = get_token_auth_header()
    idinfo = verify_token(token)

    # check if the email is present in db
    user = User.query.filter(User.email == idinfo['email']).all()

    if user == []:
        new_user = User(idinfo['name'], idinfo['email'], idinfo['picture'])
        new_user.insert()

    return jsonify({
        'success': True,
        'token': token,
        'userInfo': {
            'name': idinfo['name'],
            'email': idinfo['email'],
            'picture': idinfo['picture']
        }
    })
