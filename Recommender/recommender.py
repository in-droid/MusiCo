from data.DataBase import query
from SpotifyAPI import base_client
from data.models import *

class Recommender:
    def __init__(self, city, userID):
        self.userID = userID
        self.q = query.QueryDatabase()
        q = self.q
        country = q.get_location_country_by_city(city)
        self.loc_id = q.get_location_id(city, country)

        # make a dict in the form of artist_id = [artist_genres]
        events = q.get_eventIDs_for_location(self.loc_id)
        self.artist_genres_name = {}
        self.artist_genres_ids = {}
        for event in events:
            a_id = q.get_artistID_for_event(event)

            artist_name = q.get_artist_name(a_id)
            try:
                fetched = q.get_all_genres_for_artist(a_id)

                self.artist_genres_name[artist_name] = fetched
                self.artist_genres_ids[a_id] = fetched
            except:
                pass

    def get_user_genres(self):
        return query.QueryDatabase().get_user_gernes(User.objects.get(id=self.userID).username)

    # get weight based on artist popularity rating
    @staticmethod
    def weighing_value(rating):
        if rating in range(0, 30):
            return 0.6
        if rating in range(30, 70):
            return 0.8
        if rating in range(70, 101):
            return 1.0

    # returns list of (artist_id, score)
    def recommend(self):
        user_genres = self.get_user_genres()
        spotify = base_client.SpotifyAPI()

        # dict of name: popularity
        artists_popularity = spotify.get_artists_popularity_id(self.artist_genres_ids.keys())

        scores = {}

        for name, genres in self.artist_genres_name.items():
            artist_genres = set(genres)

            score = len(artist_genres.intersection(user_genres)) * \
                self.weighing_value(artists_popularity[name])

            scores[name] = score

        # returns list of tuples
        results = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        if len(results) < 5:
            return results

        return results[:5]
