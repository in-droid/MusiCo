<template>
  <v-main>
    <NavBar />

    <v-container fluid>
      <v-row align="center" justify="space-around" class="pa-1 ma-2">
        <!-- Lig -->
        <v-btn @click="logSpotify()" dark large color="green">
          <span class="text-truncate">Spotify log-in</span>
        </v-btn>
        <!-- Fill -->
        <v-btn
          @click="loadData()"
          dark
          large
          color="green"
          outlined
          v-if="logged"
        >
          <span class="text-truncate">Load your data</span>
        </v-btn>
        <!-- Get -->
        <v-btn
          @click="getData()"
          dark
          large
          color="green"
          outlined
          v-if="logged"
        >
          <span class="text-truncate">Get your data</span>
        </v-btn>
      </v-row>

      <v-row dense>
        <v-col v-for="artist in this.artists" :key="artist.id" :cols="3">
          <v-card>
            <v-img
              :src="artist.img_link"
              class="white--text align-end"
              gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
              height="150px"
              width="auto"
            >
              <v-card-title v-text="artist.name"></v-card-title>
            </v-img>
          </v-card>
        </v-col>
      </v-row>

      <v-timeline align-top dense>
        <v-timeline-item v-for="genre in this.genres" :key="genre.name" small>
          <div>
            <div class="font-weight-normal">
              <strong>{{ genre.name }}</strong>
            </div>
          </div>
        </v-timeline-item>
      </v-timeline>
    </v-container>
  </v-main>
</template>

<script>
import NavBar from "@/components/NavBar";
import { getAPI } from "../axios-api.js";

export default {
  name: "MyProfile",

  components: { NavBar },
  created() {
    this.token = JSON.parse(localStorage.getItem("token"));

    this.config = {
      headers: { Authorization: `Token ${this.token}` },
    };
    // console.log(this.token);
  },
  data: () => ({
    token: "",
    config: null,
    artists: null,
    genres: null,
    logged: false,
  }),
  methods: {
    loadData() {
        // This actually fills the data
        // /user/spotify-is-auth/
        getAPI
        .get("user/spotify-is-auth/", this.config)
        .then((response) => {
            console.log(response, 'success');
        })
        .catch((err) => {
          console.log(err);
        });
    },
    logSpotify() {
      // GET at 127.0.0.1:8000/user/spotify-auth/ and redirect to its url\
      getAPI
        .get("user/spotify-auth/", this.config)
        .then((response) => {
          const url = response.data.url;
          //   console.log(url);
          window.open(url, "_blank");
          this.logged = true;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getData() {
      getAPI
        .get("user/profile/", this.config)
        .then((response) => {
          this.artists = response.data.ARTISTS;
          this.genres = response.data.GENRES;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
