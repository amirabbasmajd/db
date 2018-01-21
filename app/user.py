from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)


class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return '<User: {0} >'.format(self.username)

    def get_id(self):
        return self.username

    @staticmethod
    def verify_password(password_hash, password):
        return check_password_hash(password_hash, password)

    @staticmethod
    def generate_hash(password):
        return generate_password_hash(password, method='pbkdf2:sha256')
