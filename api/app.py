import os
from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
from utilities import init_curs
from club_util import VistaClubLookup
from user_util import verify_login
import download_video
import requests

app = Flask(__name__)
CORS(app)

DOWNLOAD_DIR = "videos"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

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

@app.route("/api/download-video", methods=["POST"])
def download_club_video():
    video_url = request.json.get("video_url")

    if not video_url:
        return jsonify({"error": "No video URL provided"}), 400

    file_id = download_video.extract_file_id(video_url)
    if not file_id:
        return jsonify({"error": "Invalid Google Drive URL"}), 400 
    
    file_id = download_video.extract_file_id(file_id)
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    destination_path = os.path.join(DOWNLOAD_DIR, f"{file_id}.mp4")

    if not os.path.exists(destination_path):
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            with open(destination_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        else:
            return jsonify({"error": f"Failed to download file. Status code: {response.status_code}"}), 500
        
    return send_file(destination_path, as_attachment=False)


if __name__ == '__main__':
    app.run(debug=True, port=5000)