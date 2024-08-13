from time import time
from firebase_admin import db, credentials

from flask import jsonify

class User(object):
    def __init__(self, data):
        self.icon = data['photoURL']
        self.username = data['displayName']
        self.email = data['email']
        self._uid = data['uid']
        self.regdate = time()

    # Registers User in Realtime Database using their permanent UID as key
    # Will store portfolio information
    def reg_user(self):
        ref = db.reference('users')
        try:
            if not ref.child(self._uid).get():

                # Create new user object in database
                ref.child(self._uid).set({
                    "photoURL": self.icon,
                    "username": self.username,
                    "email": self.email,
                    'regdate': self.regdate,
                })
                return True, 201 # Tell frontend we need to prompt for more personalization info
            return True, 200
        except Exception as e:
            print(f"Exception: {e}")
            return False, 400  # Something crazy happened, server error please debug if this happens.
        
    def get_header_data(self):
        return jsonify({'photoURL': self.icon, 'username': self.username, "email": self.email})