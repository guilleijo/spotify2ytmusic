import logging
import os

import spotipy
from dotenv import load_dotenv
from spotipy import SpotifyOAuth
from ytmusicapi import YTMusic

load_dotenv()


CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

# config logger
format = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(format)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def main():
    # spotify
    scope = "playlist-read-private"
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
        )
    )

    playlists = sp.current_user_playlists()
    playlists = playlists.get("items")

    playlists_to_create = {}

    for p in playlists:
        playlist_id = p["id"]
        playlist_name = p["name"]
        playlist_description = p["description"]

        offset_mul = 0
        track_names = []
        while True:
            tracks = sp.playlist_items(playlist_id, offset=100 * offset_mul)
            next = tracks["next"]

            tracks = tracks["items"]
            for track in tracks:
                track_name = track["track"]["name"]
                track_artist = track["track"]["artists"][0]["name"]
                full_name = f"{track_name} - {track_artist}"
                track_names.append(full_name)

            p_data = {
                "id": playlist_id,
                "name": playlist_name,
                "description": playlist_description,
                "tracks": track_names,
            }
            playlists_to_create[playlist_name] = p_data

            if next is None:
                break

            offset_mul += 1

    # ytmusic
    ytmusic = YTMusic("headers_auth.json")

    for data in playlists_to_create.values():
        playlist_name = data["name"]

        yt_track_ids = []
        logger.info(f"Getting track list for playlist: {playlist_name}")
        for sp_track_name in data["tracks"]:
            search_results = ytmusic.search(sp_track_name)
            try:
                yt_track_id = search_results[0]["videoId"]
                yt_track_ids.append(yt_track_id)
            except Exception as e:
                logger.error(f"Song not found: {sp_track_name}. Error: {e}")

        logger.info(f"Creating '{playlist_name}'")
        yt_playlist_id = ytmusic.create_playlist(playlist_name, data["description"])

        logger.info(f"Adding tracks to '{playlist_name}'")
        ytmusic.add_playlist_items(yt_playlist_id, yt_track_ids)


if __name__ == "__main__":
    logger.info("Starting...")
    main()
