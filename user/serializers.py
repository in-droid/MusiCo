from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db.models.fields import IntegerField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_username(self, username):
        if len(username) < 4 or len(username) > 15:
            raise ValidationError('Username must be between 4 and 15 characters long')
        return username

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


class GenreSerializer(serializers.Serializer):
    #id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=True)