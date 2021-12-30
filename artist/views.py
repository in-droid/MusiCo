from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from data.models import *
from artist.serializers import *
import data.DataBase.query as DataBase
from rest_framework.renderers import JSONRenderer

# Create your views here.


@api_view(['GET'])
@authentication_classes([])
#@permission_classes([IsAuthenticated])
@permission_classes([])
def all_artists(request):
    
    db = DataBase.QueryDatabase()
    artists = db.get_all_artists()
    print(request.user)
    if not artists:
        return Response()
    
    response = ArtistSerializerList(artists, many=True)
    return Response(response.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def artist_detail(request, pk):
    db = DataBase.QueryDatabase()
    artist = db.get_artist(pk)
    if not artist:
        return Response()
    artist_serialized = ArtistSerializer(artist)
    return Response(artist_serialized.data)