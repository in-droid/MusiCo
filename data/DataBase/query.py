import sys

# sys.path.append('../../')

from data.models import *


# Use this class to get data from the database

class QueryDatabase:
    def __init__(self):
        pass
    
    # Get a dictionary for all artist with KEY = artist.id and VALUE = artist.name
    def get_all_artists(self):
        return [artist for artist in Artist.objects.all()]

    # Get a dictionary for all venues with KEY = venue.id and VALUE = venue.name
    def get_all_venues(self):
        return {venue.id: venue.name for venue in Venue.objects.all()}

    # Get a dictionary for all genres with KEY = genre.id and VALUE = genre.name
    def get_all_genres(self):
        return {genre.id: genre.name for genre in Genre.objects.all()}

    # Get all genres for specific artist by artist ID
    def get_all_genres_for_artist(self, aid):
        try:
            genres = []
            for artist_genre in Artist_Genre.objects.filter(aid=aid):
                genre = Genre.objects.get(id=artist_genre.gid.id)
                genres.append(genre.name)
            return genres
        except:
            return None

    def get_artist(self, id):
        try:
            return Artist.objects.get(id=id)
        except:
            return None
     # Get artist NAME by ID
    def get_artist_name(self, id):
        try:
            return Artist.objects.get(id=id).name
        except:
            # Can be changed to anything...
            return None

    # Get artist ID by NAME
    def get_artist_id(self, name):
        try:
            return Artist.objects.get(name=name).id
        except:
            # Can be changed to anything...
            return None
        
    # Get artist INFO by ID
    def get_artist_info(self, id):
        try:
            return Artist.objects.get(id=id).info
        except:
            return None

    # Get artist IMG_LINK by ID
    def get_artist_imgLink(self, id):
        try:
            return Artist.objects.get(id=id).img_link
        except:
            return None

    # Get a list of artists for that genre
    def get_artist_by_genre(self, genre):
        try:
            artists = []
            genre_id = Genre.objects.get(name=genre)
            for artist_genre in Artist_Genre.objects.filter(gid=genre_id):
                artist = artist_genre.aid.name
                artists.append(artist)
            return artists
        except:
            # Can be changed to anything...
            return None

    # Get all events with all fields
    def get_all_events(self):
        return [(event.id, event.vid.id, event.aid.id, event.lid.id, event.date, event.lineup, event.additional_info, event.tickets) for event in Event.objects.all()]
    
    # Get event IDs for given artist ID 
    def get_event_ids_for_artist(self, aid):
        try:
            return [event.id for event in Event.objects.filter(aid=aid)]
        except:
            return None


    def get_event(self, eid):
        try:
            return Event.objects.get(id=eid)
        except:
            return None

    # Get LINEUP for event by event ID
    def get_event_lineup(self, eid):
        try:
            return Event.objects.get(id=eid).lineup
        except:
            return None

    # Get TICKETS for event by event ID
    def get_event_tickets(self, eid):
        try:
            return Event.objects.get(id=eid).tickets
        except:
            return None

    # Get DATE for event by event ID
    def get_event_date(self, eid):
        try:
            return Event.objects.get(id=eid).date
        except:
            return None

    # Get ADDITIONAL INFO for event by event ID
    def get_event_additionalInfo(self, eid):
        try:
            return Event.objects.get(id=eid).additional_info
        except:
            return None
    
    # Get venue ID for event by event ID
    def get_venueID_for_event(self, eid):
        try:
            return Event.objects.get(id=eid).vid.id
        except:
            return None

    # Get artist ID for event by event ID
    def get_artistID_for_event(self, eid):
        try:
            return Event.objects.get(id=eid).aid.id
        except:
            return None

    # Get artist NAME for event by event ID
    def get_artist_name_for_event(self, eid):
        try:
            return Event.objects.get(id=eid).aid.name
        except:
            return None

    # Get a list ov all venues (id, name, info) for artist by artist ID
    def get_all_venus_for_artist(self, aid):
        try:
            venue_id = Event.objects.get(aid=aid).vid.id
            return [(venue.id, venue.name, venue.info) for venue in Venue.objects.filter(id=venue_id)]
        except:
            return None

    # Get venue ID by NAME of venue
    def get_venue_id(self, name):
        try:
            return Venue.objects.get(name=name).id
        except:
            return None

    # Get venue NAME by venue ID
    def get_venue_name(self, vid):
        try:
            return Venue.objects.get(id=vid).name
        except:
            return None

    # Get venue INFO by venue ID
    def get_venue_info(self, vid):
        try:
            return Venue.objects.get(id=vid).info
        except:
            return None

    # Get venue ADDITIONAL_INFO by venue ID
    def get_venue_additionalInfo(self, vid):
        try:
            return Venue.objects.get(id=vid).additional_info
        except:
            return None

    # Get venue IMG_LINK by venue ID
    def get_venue_imgLink(self, vid):
        try:
            return Venue.objects.get(id=vid).img_link
        except:
            return None

    # Get a list of all locations (id, city, country)
    def get_all_locations(self):
        return [(location.id, location.city, location.country) for location in Location.objects.all()]

    # Get location ID by CITY and COUNTRY
    def get_location_id(self, city, country):
        try:
            return Location.objects.filter(country=country).get(city=city).id
        except:
            return None

    def get_location_id_by_city(self, city):
        try:
            return Location.objects.get(city=city).id
        except:
            return None

    def get_location_id_by_city_country(self, city, country):
        try:
            return Location.objects.get(city=city, country=country).id
        except:
            return None

    # Get location CITY by location ID
    def get_location_city(self, id):
        try:
            return Location.objects.get(id=id).city
        except:
            return None

    # Get location COUNTRY by location ID
    def get_location_country(self, id):
        try:
            return Location.objects.get(id=id).country
        except:
            return None

    # Get location (city, country) by location ID
    def get_location(self, id):
        try:
            location = Location.objects.get(id=id)
            return (location.city, location.country)
        except:
            return None

    # Get a list of event IDs for events in location by location ID
    def get_eventIDs_for_location(self, lid):
        try:
            return [event.id for event in Event.objects.filter(lid=lid)]
        except:
            return None

    def get_all_events_for_location(self, lid):
        try:
            return [event for event in Event.objects.all().filter(lid=lid)]
        except:
            return None

    # Get location ID for event by event ID  
    def get_event_location(self, eid):
        try:
            return Event.objects.get(id=eid).lid.id
        except:
            return None


    def get_user_artists(self, username):
        try:
            return [artist.artist.name for artist in User_Artist.objects.filter(user=User.objects.get(username=username).id)]
        except:
            return None


    def get_user_artists_obj(self, username):
        try:
            return [user_artist.artist for user_artist in User_Artist.objects.filter(user=User.objects.get(username=username).id)]
        except:
            return None

    def get_user_gernes(self, username):
        try:
            return [genre.gid.name for genre in User_Genre.objects.filter(uid=User.objects.get(username=username).id)]
        except:
            return None


    def get_location_country_by_city(self, city):
        try:
            return Location.objects.get(city=city).country
        except:
            return None 
        

    def get_artist_spotify(self, artist):
        try:
            return Artist_SpotifyID.objects.get(artist=artist).spotify_id
        except:
            return None