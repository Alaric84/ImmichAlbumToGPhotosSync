# Docker Usage

## 1. Prepare your .env file

Create a `.env` file in the project root with the following content (update values as needed):

```
IMMICH_URL=http://your-immich-server/api
IMMICH_API_KEY=your_immich_api_key
ALBUM_NAME=PhotoFrame
LOCAL_DIR=photo_frame
RCLONE_REMOTE=gphotos:album/PhotoFrame
```

## 2. Build the Docker image

Run this command in the project directory:

```bash
docker build -t immich-gphotos-sync .
```

## 3. Start the container


## 3. Start the container

Map the config file and pass the .env file:

```bash
docker run --env-file .env -v $(pwd)/config/rclone.conf:/config/rclone.conf immich-gphotos-sync
```

This will start the sync process using your configuration and environment variables, with the config file mapped directly from the host.
# Google Photos Rclone Access Setup

To sync with Google Photos using rclone, you need to set up rclone with access to your Google account:


1. **Install rclone v1.72 or newer** (older versions may not work reliably with Google Photos):
	```bash
	curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip
	unzip rclone-current-linux-amd64.zip
	cd rclone-*-linux-amd64
	sudo cp rclone /usr/bin/
	rclone version
	```


2. **Configure rclone for Google Photos:**
	 ```bash
	 rclone config
	 ```
	 - Choose `n` for a new remote.
	 - Name it `gphotos` (or any name you like, but match it in your config and script).
	 - For storage, select `google photos`.
	 - **If your browser says the Google OAuth app is blocked:**
		 1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
		 2. Create a new project (or select an existing one).
		 3. Go to "APIs & Services" > "Credentials".
		 4. Click "Create Credentials" > "OAuth client ID".
		 5. Set application type to "Desktop app".
		 6. Download the `client_id.json` file.
		 7. When running `rclone config`, enter your own `client_id` and `client_secret` from the file when prompted.
		 8. Authenticate again with rclone; this time, the app is owned by you and will not be blocked.
	 - When finished, rclone will save the required `token` and config in your rclone config file.

3. **Copy the config:**
	- Copy the `[gphotos]` section from your default rclone config (usually at `~/.config/rclone/rclone.conf`) into `config/rclone.conf` in this project.
	- Make sure the `token` line is present and up to date.

4. **Troubleshooting:**
	- If you need to re-authenticate, run `rclone config reconnect gphotos:`.
	- For more details, see the [rclone Google Photos documentation](https://rclone.org/googlephotos/).

**Note:** Never share your `rclone.conf` with others, as it contains access tokens for your Google account.
# ImmichAlbumToGPhotosSync
Cyclically sync a local immich album to google photos to display the images on a chromecast device
