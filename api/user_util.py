from time import time
import firebase_admin
from firebase_admin import db, credentials, auth
import os
from dotenv import load_dotenv

from flask import jsonify

cred = credentials.Certificate("api/creds.json")
firebase_admin.initialize_app(cred)


from flask import jsonify
from firebase_admin import auth

def verify_login(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        print("User authenticated")
        
        return jsonify({'message': 'User authenticated', 'uid': uid}), 200

    except auth.InvalidIdTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except auth.ExpiredIdTokenError:
        return jsonify({'error': 'Token expired'}), 401
    except Exception as e:
        print(f'Error verifying token: {e}')
        return jsonify({'error': 'Token verification failed'}), 401

# class User(object):
#     def __init__(self, data):
#         self.icon = data['photoURL']
#         self.username = data['displayName']
#         self.email = data['email']
#         self._uid = data['uid']
#         self.regdate = time()

#     # Registers User in Realtime Database using their permanent UID as key
#     # Will store portfolio information
#     def reg_user(self):
#         ref = db.reference('users')
#         try:
#             if not ref.child(self._uid).get():

#                 # Create new user object in database
#                 ref.child(self._uid).set({
#                     "photoURL": self.icon,
#                     "username": self.username,
#                     "email": self.email,
#                     'regdate': self.regdate,
#                 })
#                 return True, 201 # Tell frontend we need to prompt for more personalization info
#             return True, 200
#         except Exception as e:
#             print(f"Exception: {e}")
#             return False, 400  # Something crazy happened, server error please debug if this happens.
        
#     def get_header_data(self):
#         return jsonify({'photoURL': self.icon, 'username': self.username, "email": self.email})