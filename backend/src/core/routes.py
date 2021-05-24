from utils import get_default_user_password_hash
import jwt
from passlib.context import CryptContext
import datetime
from flask import current_app as application
from flask import jsonify, make_response, request


@application.route('/api/login', methods=['POST'])
def login():
    auth = request.authorization
    if auth and auth.username and auth.password:
        password_hash = get_default_user_password_hash(auth.username)
        crypt_context = CryptContext(schemes=['bcrypt_sha256'])
        if password_hash is None or not crypt_context.verify(auth.password, password_hash):
            return make_response('Incorrect credentials!', 401)
        expires = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        token = jwt.encode({'user': auth.username, 'exp': expires}, application.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})
    return make_response('Login required!', 401)
