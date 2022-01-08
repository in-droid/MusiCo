from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from data.models import *
from event.serializers import *
import data.DataBase.query as DataBase
from rest_framework.renderers import JSONRenderer
from .serializers import *
# Create your views here.

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def all_venues(request):
    
    db = DataBase.QueryDatabase()
    venues = db.get_all_venues()
    if not venues:
        return Response()
    
    response = VenueSerializer(venues, many=True)
    return Response(response.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def venue_detail(request, pk):
    db = DataBase.QueryDatabase()
    venue = db.get_venue_obj(pk)
    if not venue:
        return Response()
    
    response = VenueDetailSerializer(venue)
    return Response(response.data)
