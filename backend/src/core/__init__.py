from flask import Flask, request, jsonify, make_response
from functools import wraps
from utils import get_file_path
import logging.config
import jwt
import os

os.makedirs('logs', exist_ok=True)
logging.config.fileConfig(fname=get_file_path('logger.conf'), disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logger.info('Web app initialization')

version = os.environ.get('PROFILE', 'development')


def create_app():
    application = Flask(__name__)
    application.config['SECRET_KEY'] = 'ThisIssASecret'

    with application.app_context():
        from core import routes
        from instagram.routes import routes
        # from facebook import *

        return application


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'authorization' in request.headers:
            token = request.headers['authorization'].split(' ')[1]
        elif 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response(jsonify({'message': 'Token is missing!'}), 401)

        try:
            from flask import current_app as application
            data = jwt.decode(token, application.config['SECRET_KEY'])
            logger.debug('correct JWT for user {}'.format(data['user']))
        except jwt.DecodeError:
            return make_response(jsonify({'message': 'Token is invalid!'}), 401)

        return f(*args, **kwargs)

    return decorated
