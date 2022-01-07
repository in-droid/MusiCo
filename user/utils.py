from requests.api import request
from data.models import Artist, Artist_Genre, SpotifyToken, User_Artist, User_Genre, Genre
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, put, get


BASE_URL = "https://api.spotify.com/v1/me/"

BASE_URL_ARTISTS = "https://api.spotify.com/v1/artists/"

def get_user_tokens(rest_token):
    user_tokens = SpotifyToken.objects.filter(user=rest_token)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


def update_or_create_user_tokens(rest_token, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(rest_token)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token',
                                   'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(user=rest_token, access_token=access_token,
                              refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()


def is_spotify_authenticated(rest_token):
    tokens = get_user_tokens(rest_token)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(rest_token)

        return True

    return False


def refresh_spotify_token(rest_token):
    refresh_token = get_user_tokens(rest_token).refresh_token
    print(refresh_token)

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    #refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(
        rest_token, access_token, token_type, expires_in, refresh_token)

def execute_spotify_api_request(rest_token, endpoint, post_=False, put_=False):
    tokens = get_user_tokens(rest_token)
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + tokens.access_token}

    if post_:
        post(BASE_URL + endpoint, headers=headers)
    if put_:
        put(BASE_URL + endpoint, headers=headers)

    response = get(BASE_URL + endpoint, {}, headers=headers)
    try:
        return response.json()
    except:
        return {'Error': 'Issue with request'}


def create_update_user_genres(genre, user):
    try:
        new_genre = Genre.objects.get(name=genre)
    except Genre.DoesNotExist:
            new_genre = Genre(name=genre)
            new_genre.save()
    try:
        User_Genre.objects.get(uid=user, gid=new_genre)
        return
    except User_Genre.DoesNotExist:    
        new_user_genre = User_Genre(uid=user, gid=new_genre)
        new_user_genre.save()


def create_update_user_artists(artist, img, user):
    try:
        artist_ = Artist.objects.filter(name=artist)
        if artist_ and artist_[0]:

            new_input = User_Artist(user=user, artist=artist_[0])
        else:
                new_artist = Artist(name=artist, img_link=img)
                new_artist.save()
                new_input = User_Artist(user=user, artist=new_artist)
        new_input.save()
    except:
        pass

def create_update_artist_genres(artist_name, genre_name):
    artist = Artist.objects.get(name=artist_name)
    genre = Genre.objects.get(name=genre_name)
    try:
        Artist_Genre.objects.get(aid=artist, gid=genre)
    except Artist_Genre.DoesNotExist:
        new_input = Artist_Genre(aid=artist, gid=genre)
        new_input.save()

def update_user_music(request):
    endpoint = 'top/artists?time_range=short_term&limit=10&offset=1'
    response = execute_spotify_api_request(str(request.auth), endpoint, post_=False, put_=False)
    if response.get('error'):
        return response
    
    for item in response['items']:
        create_update_user_artists(item['name'], item['images'][0]['url'] ,request.user)
        for genre in item['genres']:
            create_update_user_genres(genre, request.user)
            create_update_artist_genres(item['name'], genre)
    
    return response