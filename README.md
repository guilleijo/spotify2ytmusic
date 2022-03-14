# spotify2ytmusic
Migrate your playlists from your spotify account to your youtube music account

## Using
- [spotipy](https://github.com/plamere/spotipy)
- [ytmusicapi](https://github.com/sigma67/ytmusicapi)

## Spotify auth
- Create a developer account: https://developer.spotify.com/
- Create a new app
- Get credentials
- Set `redirect_uri` to a valid value (e.g.: "http://localhost:8080")
- Create `.env` file following `.env.sample` structure and add those values

## Youtube music auth
- Follow [Copy authentication headers](https://ytmusicapi.readthedocs.io/en/latest/setup.html#copy-authentication-headers) from `ytmusicapi` docs.
- Create a `headers_auth.json` following `headers_auth.sample.json` structure
- Replace `cookie` and other necessary values from the data in your browser

## Run script
- Install dependencies: ```$ pipenv install```
- Activate environment: ```$ pipenv shell```
- Run script: ```$ python main.py```
