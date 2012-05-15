from encryption import Encryption

from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty()

class UserDataHandler(object):
    @staticmethod
    def get_by_id(user_id):
        "Returns a user object given a user id"
        # TODO: Why can't to_dict() be called on PageEntry.get_by_id()?
        user = User.get_by_id(user_id)
        return user
        #return {'username': user.username, 'password': user.password, 'email':
        #        user.email}

    @staticmethod
    def get_by_username(username):
        "Returns a list of user objects given a username"
        user = db.GqlQuery("SELECT * FROM User WHERE username = '%s'" %
                username)
        return user.fetch(1)
        #return {'username': user.username, 'password': user.password, 'email': user.email}

    @staticmethod
    def put(username, password, email = ''):
        password_hash = Encryption.make_password_hash(username, password)
        return User(username = username, password = password_hash, email =
                email).put().id()

    @staticmethod
    def get_all():
        "Returns all page entries as user objects in a list"
        users = db.GqlQuery('SELECT * FROM User')
        return users
        #return [{'username': user.username, 'password': user.password, 'email': user.email}
        #        for user in users]
