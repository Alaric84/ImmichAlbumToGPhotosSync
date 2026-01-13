
import os
import subprocess
import requests

# --- Configuration (Passed via Env Vars) ---
IMMICH_URL = os.getenv("IMMICH_URL") # e.g., "https://immich.local/api"
API_KEY = os.getenv("IMMICH_API_KEY")
ALBUM_NAME = os.getenv("ALBUM_NAME", "Photo Frame")
LOCAL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photo_frame")
os.makedirs(LOCAL_DIR, exist_ok=True)
RCLONE_REMOTE = os.getenv("RCLONE_REMOTE", "gphotos:album/Photo Frame")

def get_album_id():
    headers = {"x-api-key": API_KEY}
    r = requests.get(f"{IMMICH_URL}/albums", headers=headers)
    albums = r.json()
    for a in albums:
        if a['albumName'] == ALBUM_NAME:
            return a['id']
    return None

def download_album(album_id):
    headers = {"x-api-key": API_KEY}
    r = requests.get(f"{IMMICH_URL}/albums/{album_id}", headers=headers)
    assets = r.json().get('assets', [])
    
    os.makedirs(LOCAL_DIR, exist_ok=True)
    
    for asset in assets:
        filename = f"{asset['id']}.jpg" # Simplified naming
        filepath = os.path.join(LOCAL_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"Downloading {filename}...")
            url = f"{IMMICH_URL}/assets/{asset['id']}/original"
            with requests.get(url, headers=headers, stream=True) as res:
                with open(filepath, 'wb') as f:
                    for chunk in res.iter_content(chunk_size=8192):
                        f.write(chunk)

def sync_to_google():
    print("Starting Rclone Sync...")
    # Use local config/rclone.conf for rclone config
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "rclone.conf")
    subprocess.run(["rclone", "--config", config_path, "sync", LOCAL_DIR, RCLONE_REMOTE, "--progress"])

if __name__ == "__main__":
    aid = get_album_id()
    if aid:
        download_album(aid)
        sync_to_google()
    else:
        print(f"Album '{ALBUM_NAME}' not found.")
