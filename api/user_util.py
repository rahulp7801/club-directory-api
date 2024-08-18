# from time import time
# from firebase_admin import initialize_app
# from firebase_admin.credentials import Certificate
# from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError, verify_id_token
# from dotenv import load_dotenv

# from flask import jsonify

# cred = Certificate("api/creds.json")
# initialize_app(cred)


# from flask import jsonify

# def verify_login(id_token):
#     try:
#         decoded_token = verify_id_token(id_token)
#         uid = decoded_token['uid']
#         print("User authenticated")
        
#         return jsonify({'message': 'User authenticated', 'uid': uid}), 200

#     except InvalidIdTokenError:
#         return jsonify({'error': 'Invalid token'}), 401
#     except ExpiredIdTokenError:
#         return jsonify({'error': 'Token expired'}), 401
#     except Exception as e:
#         print(f'Error verifying token: {e}')
#         return jsonify({'error': 'Token verification failed'}), 401