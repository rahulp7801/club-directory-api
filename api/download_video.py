from flask import send_file, jsonify
import os
import re
import requests

DOWNLOAD_DIR = "videos"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def extract_file_id(url):
    """
    Extract file_id from Google Drive URL.
    """
    # Match file ID in different URL formats
    patterns = [
        r"https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)",  # format: /file/d/FILE_ID/
        r"https://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)",  # format: /open?id=FILE_ID
        r"https://drive\.google\.com/uc\?export=download&id=([a-zA-Z0-9_-]+)"  # format: /uc?export=download&id=FILE_ID
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None
    

