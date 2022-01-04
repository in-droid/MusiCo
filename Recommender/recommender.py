class Recommender:
    def __init__(self, city, country):
        self.q = query.QueryDatabase()
        q = self.q
        self.loc_id = q.get_location_id(city, country)

        # make a dict in the form of artist_id = [artist_genres]
        events = q.get_eventIDs_for_location(self.loc_id)
        self.artist_genres = []
        self.artist_names = []
        for event in events:
            a_id = q.get_artistID_for_event(event)

            self.artist_genres[a_id] = q.get_all_genres_for_artist(a_id)
            self.artist_names.append(q.get_artist_name(a_id))

    def get_user_genres(self):
        # waiting on Ivan ಠ_ಠ
        return []

    # get weight based on artist popularity rating
    @staticmethod
    def weighing_value(rating):
        if rating in range(0, 30):
            return 0.6
        if rating in range(30, 70):
            return 0.8
        if rating in range(70, 101):
            return 1.0

    def recommend(self):
        user_genres = self.get_user_genres()
        spotify = base_client.SpotifyAPI()

        artists_popularity = spotify.get_artists_popularity(self.artist_names)
        scores = {}

        index = 0
        for a_id, genres in self.artist_genres:
            artist_genres = set(genres)

            score = len(artist_genres.intersection(user_genres)) * \
                self.weighing_value(artists_popularity[index])

            scores[a_id] = score
            index += 1

        # returns list of tuples
        results = sorted(scores.items(), key=lambda x: x[1])

        if len(results) < 5:
            return results

        return results[:5]
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
