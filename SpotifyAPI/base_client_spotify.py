import os
from requests.api import head
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import base64
import datetime
from urllib.parse import urlencode


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    client_id = None
    client_secret = None
    client_creds = None
    has_expired = True

    redirect_url = "http://localhost:8888/callback"
    token_url = "https://accounts.spotify.com/api/token"
    api_url = "https://api.spotify.com/v1"

    def __init__(self):
        super().__init__()

        # set environment variables for spotipy
        os.environ["SPOTIPY_CLIENT_ID"] = "b41f9e008ac94cf586a7825f224ba261"
        os.environ["SPOTIPY_CLIENT_SECRET"] = "28f67abb8a4448fc800b6cfe7d3e6ce6"
        os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8888/callback"

        self.client_id = "b41f9e008ac94cf586a7825f224ba261"
        self.client_secret = "28f67abb8a4448fc800b6cfe7d3e6ce6"

    def generate_credentials(self):
        if self.client_id is None or self.client_secret is None:
            raise Exception("Client ID and/or secret not set!")

        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds = base64.b64encode(client_creds.encode())
        return client_creds.decode()

    def generate_token_headers(self):
        return {
            "Authorization": f"Basic {self.generate_credentials()}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def generate_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def authenticate(self):
        r = requests.post(self.token_url, self.generate_token_data(),
                          headers=self.generate_token_headers())

        # check HTTP status code
        if r.status_code not in range(200, 300):
            raise Exception("Could not authenticate client.")

        data = r.json()
        now = datetime.datetime.now()
        access_token = data["access_token"]
        expires_in = data["expires_in"]
        expires = now + datetime.timedelta(seconds=expires_in)

        self.access_token = access_token
        self.access_token_expires = expires
        self.has_expired = expires < now

        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()

        # return get access token of newly generated token
        # the beauty of recursion <3
        if expires < now:
            self.authenticate()
            return self.get_access_token
        elif token is None:
            self.authenticate()
            return self.get_access_token()

        return token

    def generate_headers(self):
        token = self.get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            'Content-Type': 'application/json'
        }

    def search(self, q, q_type):
        access_token = self.get_access_token()
        header = self.generate_headers()

        # adds parameters to GET request
        data = urlencode({"q": q, "type": q_type})
        lookup_url = f"{self.api_url}/search?{data}"
        r = requests.get(lookup_url, headers=header)

        if r.status_code not in range(200, 300):
            print(r.status_code)
            return {}
        return r.json()

    def verify_artist(self, name):
        try:
            result = self.search(
                "artist:" + name, "artist")["artists"]["items"][0]["name"]
        except IndexError:
            raise Exception(
                f"No artist named ~{name}~ was found! Please check spelling")

        not_equal = result.lower().replace(" ", "") != name.lower().replace(" ", "")
        no_result = len(self.search("artist:" + name, "artist")
                        ["artists"]["items"]) == 0

        if no_result or not_equal:
            raise Exception(
                f"No artist named ~{name}~ was found! Please check spelling")

    def get_artists_genres(self, name):
        self.verify_artist(name)

        artist_id = self.get_artist_id(name)
        lookup_url = f"https://api.spotify.com/v1/artists/{artist_id}"
        header = self.generate_headers()

        r = requests.get(lookup_url, headers=header)
        data = r.json()

        return data["genres"]

    def auth_curr_user(self, scope):
        """ https://github.com/plamere/spotipy """

        return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # get user's recently played tracks
    def get_recently_played(self, limit=15):
        sp = self.auth_curr_user("user-read-recently-played")
        items = []

        # dict_keys(['track', 'played_at', 'context'])
        data = sp.current_user_recently_played(limit=limit)["items"]
        for track in data:
            item = {
                "name": track["track"]["name"].encode("utf-8"),
                "artist": track["track"]["artists"][0]["name"].encode("utf-8"),
                "id": track["track"]["id"]
            }
            items.append(item)

        return items

    # get user's top tracks
    # values for range: short_term, medium_term, long_term
    def get_top_tracks(self, range="medium_term", limit=15):
        sp = self.auth_curr_user("user-top-read")
        items = []

        data = sp.current_user_top_tracks(
            limit=limit, time_range=range)["items"]

        for track in data:
            item = {
                "name": track["name"].encode("utf-8"),
                "artist": track["artists"][0]["name"].encode("utf-8"),
                "id": track["id"]
            }
            items.append(item)

        return items

    # get user's top artists
    # values for range: short_term, medium_term, long_term
    def get_top_artists(self, range="medium_term", limit=15):
        sp = self.auth_curr_user("user-top-read")
        items = []

        data = sp.current_user_top_artists(
            limit=limit, time_range=range)["items"]

        for artist in data:
            item = {
                "name": artist["name"],
                "popularity": artist["popularity"],
                "genres": artist["genres"]
            }
            items.append(item)

        return items

    ############################## FRONT END ##############################
    # might not work, back end needs to check if the render works (img is the url to the image of the artist)
    def get_artist_image(self, name):
        self.verify_artist(name)

        return self.search(
            "artist:" + name, "artist")["artists"]["items"][0]["images"][0]["url"]

    ############################## ZA KIRIL ##############################

    def get_artist_id(self, name):
        return self.search(
            "artist:" + name, "artist")["artists"]["items"][0]["id"]

    def get_artists_albums(self, name):
        self.verify_artist(name)

        artist_id = self.get_artist_id(name)
        lookup_url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
        header = self.generate_headers()

        r = requests.get(lookup_url, headers=header)
        data = r.json()
        albums = []

        # has other attributes such as release date, total tracks etc
        for album in data["items"]:
            albums.append(album["name"])

        return albums
