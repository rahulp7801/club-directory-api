from time import time
import firebase_admin
from firebase_admin import db, credentials, auth
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