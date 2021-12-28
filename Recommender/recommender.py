from base_client_spotify import SpotifyAPI
import pandas as pd
import math


class Recommender:
    def __init__(self):
        self.spotify = SpotifyAPI()
        self.data = pd.read_csv("data.csv", encoding="latin-1")

    def get_user_genres(self):
        artists = []

        artists.append(self.spotify.get_top_artists("short_term", 25))
        artists.append(self.spotify.get_top_artists(limit=25))
        artists.append(self.spotify.get_top_artists("long_term", 25))

        genres = set()
        popularity = []
        for artist_period in artists:
            for artist in artist_period:
                popularity.append(artist["popularity"])
                for genre in artist["genres"]:
                    genres.add(genre)

        return (genres, popularity)

    def weighing_value(self, num):
        if num in range(0, 30):
            return 0.6
        if num in range(30, 70):
            return 0.8
        if num in range(70, 101):
            return 1.0

    def get_scores(self, df, data):
        user_genres = data[0]
        artist_popularity = data[1]
        scores = []

        index = 0
        for _, row in df.iterrows():
            artist_genres = set(row['genres'].split(";"))

            score = len(artist_genres.intersection(user_genres)) * \
                self.weighing_value(artist_popularity[index])

            scores.append(score)
            index += 1

        df["score"] = scores
        results = df.sort_values('score', ascending=False)["name"].values
        
        if len(results) < 5:
            return results
        
        return results[:5]

    def recommend(self):
        return self.get_scores(self.data, self.get_user_genres())


rec = Recommender()
print(rec.recommend())
