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

if not os.path.exists("videos/movie.mp4"):
        response = requests.get("https://drive.google.com/uc?export=download&id=1XhIEzAigmOTBoHtqh7XNF-fLHi8qqDkN", stream=True)
        if response.status_code == 200:
            with open("videos/movie.mp4", 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
    
print(extract_file_id("https://drive.google.com/uc?export=download&id=1XhIEzAigmOTBoHtqh7XNF-fLHi8qqDkN"))
