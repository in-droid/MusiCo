from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from data.models import *
from event.serializers import *
import data.DataBase.query as DataBase
from rest_framework.renderers import JSONRenderer
# Create your views here.


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def all_events(request, location):
    db = DataBase.QueryDatabase()
    location_id = db.get_location_id_by_city(location)
    if not location_id:
        return Response()
    events_in_location = db.get_all_events_for_location(location_id)
    response = EventSerializerList(events_in_location, many=True)
    return Response(response.data)



@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def event_detail(request, pk):
    db = DataBase.QueryDatabase()
    event = db.get_event(pk)
    event_serialized = EventSerializer(event)
    return Response(event_serialized.data)