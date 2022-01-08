from data.models import *
from rest_framework import serializers




class ArtistSerializerForEvent(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.SerializerMethodField()
    img_link = serializers.SerializerMethodField()


    def get_name(self, obj):
        return obj.name


    def get_img_link(self, obj):
        return obj.img_link


class VenueSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    info = serializers.CharField()
    img_link = serializers.CharField()


class VenueDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    info = serializers.CharField()
    img_link = serializers.CharField()
    events = serializers.SerializerMethodField()


    def get_events(self, obj):
        return Event.objects.filter(vid=object.id)

class VenueSerializerForEvent(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    


    def get_info(self, obj):
        return obj.info

    def get_name(self, obj):
        return obj.name


class EventSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    artist = ArtistSerializerForEvent(source="aid")
    date = serializers.DateField()
    venue = VenueSerializerForEvent(source="vid")
    lineup = serializers.CharField(required=False, allow_blank=True, max_length=255)
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    additional_info = serializers.CharField(required=False, allow_blank=True, max_length=255)
    tickets = serializers.CharField(required=False, allow_blank=True, max_length=255)

    class Meta:
        model = Event


    def get_city(self, obj):
        return obj.lid.city

    
    def get_country(self, obj):
        return obj.lid.country
    

class EventSerializerList(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    artist = ArtistSerializerForEvent(source="aid")
    date = serializers.DateField()
    venue = VenueSerializerForEvent(source="vid")
    additional_info = serializers.CharField(required=False, allow_blank=True, max_length=255)