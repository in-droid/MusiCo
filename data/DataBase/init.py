
from datetime import datetime
import sys
from data.models import *

sys.path.append('../')

from Scrapers import SongKickScraper, WikipediaScraper
from SpotifyAPI import base_client



class InitDatabase:
    def __init__(self, city, country):
        if not city or not country:
            return 'Error: Must enter "city" and "country" !!'
        self.city = city
        self.country = country
        try:
            self.all_events = SongKickScraper.scrapeAllEvents(SongKickScraper.findLocation(self.city, self.country))
            if len(Location.objects.filter(country=self.country).filter(city=self.city)) == 0:
                self.__Location(city=self.city, country=self.country)
            self.Location_ID = Location.objects.filter(country=self.country).get(city=self.city)
            self.init_Models()

            # For testing
            print('Database done!')
        except:
            print('Events not found!')

    def init_Models(self):
        for event in self.all_events:

            # Add the artist to the database
            artist_name = event.artist
            if len(Artist.objects.filter(name=artist_name)) == 0:
               artist = self.__Artist(name=artist_name)
               
            self.Artist_ID = Artist.objects.get(name=artist_name)

            venue_info = None
            lineup = None
            additional_info = None
            tickets = None
            event_info = SongKickScraper.scrapeEventPage(event.eventLink)

            # Getting information for later use
            if event_info['lineUp']:
                lineup = list(event_info['lineUp'].keys())
            additional_info = event_info['additionalInfo']
            tickets = event_info['tickets']
            venue_info = event_info['venueInfo']

            # Add the venue to the database
            venue_name = event.venue
            if len(Venue.objects.filter(name=venue_name)) == 0:
                # venues.append(event.venueLink)
                self.__Venues(name=venue_name, info=venue_info)
            self.Venues_ID = Venue.objects.get(name=venue_name)

            # Add the event to the database
            date = event.date
            if date:
                date = datetime.strptime(date, '%A %d %B %Y').date()
            if len(Event.objects.filter(vid=self.Venues_ID).filter(aid=self.Artist_ID).filter(lid=self.Location_ID).filter(date=date)) == 0:
                self.__Event(self.Venues_ID, self.Artist_ID, self.Location_ID, date, lineup, additional_info, tickets)
            self.Event_ID = Event.objects.filter(vid=self.Venues_ID).filter(aid=self.Artist_ID).filter(lid=self.Location_ID).get(date=date)

            # Add a genre, artist/genre and update artist (info and img_link)
            if lineup:
                try:
                    info = []
                    img_links = []
                    for artist_name in lineup:
                        #artist_info = WikipediaScraper.searchForArtist(artist_name)
                        artist_info = ""
                        artist_spotifyID = base_client.SpotifyAPI().get_artist_id(artist_name)

                        artist_img_link = base_client.SpotifyAPI().get_artist_image(artist_name)
                        info.append(artist_info)
                        img_links.append(artist_img_link)
                        genre_names = base_client.SpotifyAPI().get_artists_genres(artist_name)

                        for genre_name in genre_names:
                            if len(Genre.objects.filter(name=genre_name)) == 0:
                                self.__Genre(genre_name)

                            self.Genre_ID = Genre.objects.get(name=genre_name)
                            if len(Artist_Genre.objects.filter(aid=self.Artist_ID).filter(gid=self.Genre_ID)) == 0:
                                self.__Artist_Genre(self.Artist_ID, self.Genre_ID)

                    temp_artist = self.__update_Artist(event.artist, info, img_links)
                    temp = self.__Artist_SpotifyID(temp_artist, artist_spotifyID)
                    print(temp)

                except Exception:
                    if len(Genre.objects.filter(name='unknown')) == 0:
                        self.__Genre(name='unknown')

                    self.Genre_ID = Genre.objects.get(name='unknown')
                    if len(Artist_Genre.objects.filter(aid=self.Artist_ID).filter(gid=self.Genre_ID)) == 0:
                        self.__Artist_Genre(self.Artist_ID, self.Genre_ID)
            else:
                try:
                    artist_info = ""
                    #artist_info = WikipediaScraper.searchForArtist(event.artist)
                    artist_spotifyID = base_client.SpotifyAPI().get_artist_id(artist_name)

                    artist_img_link = base_client.SpotifyAPI().get_artist_image(event.artist)
                    temp_artist = self.__update_Artist(event.artist, artist_info, artist_img_link)
                    self.__Artist_SpotifyID(temp_artist, artist_spotifyID)
                    genre_names = base_client.SpotifyAPI().get_artists_genres(event.artist)
                    
                    for genre_name in genre_names:
                        if (len(Genre.objects.filter(name=genre_name))) == 0:
                            self.__Genre(genre_name)

                        self.Genre_ID = Genre.objects.get(name=genre_name)
                        if len(Artist_Genre.objects.filter(aid=self.Artist_ID).filter(gid=self.Genre_ID)) == 0:
                            self.__Artist_Genre(self.Artist_ID, self.Genre_ID)

                except Exception:
                    if len(Genre.objects.filter(name='unknown')) == 0:
                        self.__Genre(name='unknown')
                        
                    self.G = Genre.objects.get(name='unknown')
                    if len(Artist_Genre.objects.filter(aid=self.Artist_ID).filter(gid=self.Genre_ID)) == 0:
                        self.__Artist_Genre(self.Artist_ID, self.Genre_ID)
    
    def __update_Artist(self, name, info, img_links):
        artist = Artist.objects.get(name=name)
        artist.info = info
        artist.img_link = img_links
        artist.save()
        return artist

    def __Artist(self, name, info=None, img_link=None):
        artist = Artist(name=name, info=info, img_link=img_link)
        artist.save()
        return artist

    def __Venues(self, name, info=None, additional_info=None, img_link=None,):
        venues = Venue(name=name, info=info, additional_info=additional_info, img_link=img_link)
        venues.save()

    def __Event(self, venues_id, artist_id, location_id, date, lineup=None, additional_info=None, tickets=None):
        event = Event(vid=venues_id, aid=artist_id, lid=location_id, date=date, lineup=lineup, additional_info=additional_info, tickets=tickets)
        event.save()

    def __Genre(self, name):
        genre = Genre(name = name)
        genre.save()

    def __Artist_Genre(self, artist_id, genre_id):
        artist_genre = Artist_Genre(aid=artist_id, gid=genre_id)
        artist_genre.save()

    def __Location(self, city, country):
        location = Location(city=city, country=country)
        location.save()

    def __Artist_SpotifyID(self, artist, spotifyid):
        artist_spotifyID = Artist_SpotifyID(artist=artist, spotify_id=spotifyid)
        artist_spotifyID.save()
        return artist_spotifyID