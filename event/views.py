from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from data.models import *
from event.serializers import *
import data.DataBase.query as DataBase
from Recommender import recommender
# Create your views here.


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def all_events(request):


    city = request.query_params.get('city', '')
    country = request.query_params.get('country', '')
    db = DataBase.QueryDatabase()
    location_id = db.get_location_id_by_city_country(city, country)
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
    if not event:
        return Response()
    event_serialized = EventSerializer(event)
    return Response(event_serialized.data)


@api_view(['GET'])
def recommended_events(request):
    user = request.user.id
    city = request.query_params.get('city', '')
    country = request.query_params.get('country', '')
    rec = recommender.Recommender(city, country, user)
    artists = rec.recommend()
   # print(artists)
    

    return Response({"msg" : "BUG IN THE RECOMMENDER"})