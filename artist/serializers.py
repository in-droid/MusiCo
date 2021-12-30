from data.models import *
from rest_framework import serializers
import data.DataBase.query as DataBase

class ArtistSerializerList(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=255)
    img_link = serializers.CharField(required=False, allow_blank=True, max_length=255)
    genres = serializers.SerializerMethodField()

    def get_genres(self, obj):
        db = DataBase.QueryDatabase()
        return db.get_all_genres_for_artist(obj.id)


class ArtistSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=255)
    info = serializers.CharField(required=False, allow_blank=True, max_length=255)
    img_link = serializers.CharField(required=False, allow_blank=True, max_length=255)
    genres = serializers.SerializerMethodField()


    def get_genres(self, obj):
        db = DataBase.QueryDatabase()
        return db.get_all_genres_for_artist(obj.id)

