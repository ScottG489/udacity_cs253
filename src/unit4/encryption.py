import random
import string
import hashlib
from google.appengine.ext import db


class Encryption(object):
    @staticmethod
    def make_salt():
        return ''.join(random.sample(string.letters,  5))

    @staticmethod
    def make_user_id_hash(user_id):
        secret = 'secret string'
        user_id = str(user_id)
        hash_value = hashlib.sha256(user_id + secret).hexdigest()
        return hash_value

    @staticmethod
    def is_valid_cookie(user_id, user_id_hash):
        return user_id_hash == Encryption.make_user_id_hash(user_id)

    @staticmethod
    def make_password_hash(username, password, salt = None):
        if not salt:
            salt = Encryption.make_salt()
        value_hash = hashlib.sha256(username + password + salt).hexdigest()
        return '%s,%s' % (value_hash, salt)

    @staticmethod
    def is_valid_password(username, password, password_hash):
        salt = password_hash.split(',')[1]
        return password_hash == Encryption.make_password_hash(username, password, salt)

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
