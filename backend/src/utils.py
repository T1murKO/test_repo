import os

__location__ = os.path.abspath(os.path.dirname(__file__))

from passlib.context import CryptContext


def get_file_path(filename: str) -> str:
    return os.path.join(__location__, filename)


def get_default_user_password_hash(username: str):
    if username == 'user':
        return CryptContext(schemes=['bcrypt_sha256']).hash('$ecREt')
    return None
