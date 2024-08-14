import os
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from utilities import init_curs
from club_util import VistaClubLookup
from user_util import verify_login

app = Flask(__name__)
CORS(app)

# Configuration
SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
print(SECRET_KEY)

@app.before_request
def before_request():
    init_curs()

@app.route("/api/login-google", methods=["POST"])
def login_google():
    data = request.json
    id_token = data.get("idToken")

    if not id_token:
        return jsonify({'error': 'ID token is required'}), 400
    
    return verify_login(id_token)


@app.route("/api/get-clubs-list", methods=['GET'])
def get_classes_list():
    club_list = VistaClubLookup()
    print(club_list.get_json_string())
    return jsonify(club_list.get_json_string())


@app.route("/api/get-clubs-by-tag", methods=['POST'])
def get_clubs_by_tags():

    tags = request.json.get("tags", [])
    print(request.json)
    print("Received tags:", tags)  # Debug: Print received tags

    if not tags:
        print("No tags received or empty list provided")
        return jsonify([])

    club_list = VistaClubLookup()
    clubs = club_list.get_clubs_by_tags(tags)
    
    print("Matching clubs:", clubs)  # Debug: Print matching clubs
    return jsonify(clubs)


@app.route("/api/get-all-tags", methods=["GET"])
def get_all_tags():
    club_list = VistaClubLookup()
    return jsonify(club_list.get_all_tags())

if __name__ == '__main__':
    app.run(debug=True, port=5000)