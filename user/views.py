import json

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user import serializers


@api_view(['GET'])
def index(request):
    response = {
        "message" : "You are Loged in! All paths accept and return only json",
        "user/login/" : "username, password",
        "user/register/": "{username, password, password2}"
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
            print(token)
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
            print(request.user)
            login(request, user)
            data["message"] = "user logged in"
            data["username"] = username

            res = {"data": data, "token": token}
            return Response(res)
        else:
            raise ValidationError({"400" : f'User {username} not active'})
        
    else:
        raise ValidationError({'message' : 'Incorrect username or password'})