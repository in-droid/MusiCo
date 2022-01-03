import json
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError
from django.http import response
from django.shortcuts import redirect
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user import serializers
from requests import Request, post
from .utils import *
from .credentials import *

@api_view(['GET'])
def index(request):
    response = {
        "token" : str(request.auth)
    }
    return Response(response)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_users(request):
    try:
        data = {}
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            account.is_active = True
            account.save()
            token = Token.objects.get_or_create(user=account)[0].key
            data["messange"] = "user registered successfully"
            data["username"] = account.username
            data["token"] = token
        else:
            data = serializer.errors

        return Response(data)
    except IntegrityError  as e:
        account=User.objects.get(username='')
        account.delete()
    raise ValidationError({"400": f'{str(e)}'})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    data = {}
    req_body = json.loads(request.body)
    username = req_body['username']
    password = req_body['password']
    try:
        user = User.objects.get(username=username)
    except BaseException as e:
        raise ValidationError({"400" : f'{str(e)}'})
    token = Token.objects.get_or_create(user=user)[0].key
    print(token)
    if not user.check_password(password):
        raise ValidationError({'message' : 'Incorrect username or password'})
    
    if user:
        if user.is_active:
            login(request, user)
            data["message"] = "user logged in"
            data["username"] = username

            res = {"data": data, "token": token}
            return Response(res)
        else:
            raise ValidationError({"400" : f'User {username} not active'})
        
    else:
        raise ValidationError({'message' : 'Incorrect username or password'})


@api_view(['GET'])
def spotify_auth(request, format=None):

    resp = request.auth
    scopes = 'user-top-read'

    url = Request('GET', 'https://accounts.spotify.com/authorize', params={
        'scope': scopes,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID
    }).prepare().url
    return Response({'url': url}, status=status.HTTP_200_OK)

@api_view(['GET'])
def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')


    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    update_or_create_user_tokens(
        str(request.auth), access_token, token_type, expires_in, refresh_token)

    return Response(str(request.auth))



@api_view(['GET'])
def is_spotify_auth(request):
    is_authenticated = is_spotify_authenticated(str(request.auth))
    update_user_music(request)
    return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


@api_view(['GET'])
def my_profile(request):
    response = update_user_music(request)
    return Response(response)
 

