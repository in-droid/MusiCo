<template>
    <v-main>
        <NavBar/>
        <v-card width="70%" class="mx-auto my-10 elevation-0">
            <div class="text-center">
                <v-row>
                    <v-text-field :loading="loadingSearch" v-model="city" outline label="City" 
                    append-icon="mdi-search" prepend-inner-icon="mdi-map-search"></v-text-field>
                    
                    <v-select
                    v-model="country"
                    :items="countries"
                    label="Country"
                    ></v-select>

                    <v-btn @click="getEvents" color="primary" x-large elevation="1" plain icon >
                        <v-icon>mdi-magnify</v-icon>
                    </v-btn>
                </v-row>
            </div>
        </v-card>
        <v-card width="70%" class="mx-auto my-10 elevation-0">
            <div class="text-center">
                <h1 style="font-family: 'Verdana'">Events at your location:</h1>
                <div class="subtitle-1">Fixed country: {{ this.
                    country }}</div>
            </div>
        </v-card>

        <div class="events">
            <v-container class="mt-5">

                <v-alert
                class="text-center" 
                v-if="noMovies"
                border="bottom"
                colored-border
                type="warning"
                elevation="2"
                >
                    No events for that city
                </v-alert>
                <v-card v-if="noMovies" class="my-14 elevation-0"> 
                    <v-row>
                        <v-col>
                            <v-img width="600" height="350" class="mx-auto" style="border-radius: 10px" 
                            src="https://www.czechuniversities.com/uploads/2020/01/3380.jpg"></v-img>
                        </v-col>
                        <v-col>
                            <v-img width="600" height="350" class="mx-auto" style="border-radius: 10px" 
                            src="https://cdn.londonandpartners.com/visit/london-organisations/alexandra-palace/92923-640x360-alexandra-palace-gig-640.jpg"></v-img>
                        </v-col>
                    </v-row>
                    <div class="text-center my-14">
                        <h1 class="red--text text--darken-1 font-italic" 
                        style="font-family: 'Verdana'">Life is made of small moments like this!</h1>
                    </div>
                </v-card>
                
                <v-row>
                    <v-col v-for="event in events" :key="event.id" md="4" xs="12">
                        
                    <v-card
                        class="mx-auto"
                        max-width="400"
                        height="350"
                    >
                        <v-img
                        class="white--text align-end"
                        height="200px"
                        :src="event.artist.img_link"
                        >
                        <v-card-title >
                            <div class="font-weight-bold text-h5">
                                <v-card>
                                    <router-link
                                    class="link-style black--text"
                                    style="text-decoration:none"
                                    :to="{name: 'concert', params: {id: event.artist.id, artist_name: event.artist.name, artist_img: event.artist.img_link, date: event.date, venue_name: event.venue.name, venue_info: event.venue.info, add_info: event.additional_info}}"
                                >
                                    <h4 class="pa-1" style="font-family: 'Verdana'">{{ event.artist.name }}</h4>
                                </router-link>
                                </v-card>
                                
                            
                            </div>
                        </v-card-title>
                        </v-img>

                        <v-card-subtitle class="pb-0 font-weight-bold">
                        {{ event.date }}
                        </v-card-subtitle>

                        <v-card-text class="text--primary">

                        <div ><h2 class="red--text text--darken-1 my-2" 
                        style="font-family: 'Verdana'">{{ event.venue.name }}</h2></div>
                        <div><h3 class="font-weight-light my-2"><v-icon >mdi-map-marker</v-icon>{{ event.venue.info }}</h3></div>
                        </v-card-text>

                    </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </div>
    </v-main>
</template>

<script>
import NavBar from '@/components/NavBar';

import { getAPI } from "../axios-api.js";


export default {
    name: 'Events',
    components: {NavBar},
    data: () => ({
        country: 'Slovenia',
        countries: [
            'Slovenia', 'Macedonia', 'Italy', 'Serbia', 'France'
        ],
        loadingSearch: false,
        noMovies:true,
        
        city: '',
        events: [
        ]
    }),
    methods: {
        checkPictures() {
            for (let i = 0; i < this.events.length; i++) {
                // Event gets default image if it doesn't have the artist image
                if (this.events[i].artist.img_link === null) {
                    this.events[i].artist.img_link = 'https://media.istockphoto.com/photos/concert-stage-on-rock-festival-music-instruments-silhouettes-picture-id1199243596?k=20&m=1199243596&s=612x612&w=0&h=5L3fWhbB4YtVOPsnnqrUg22FaHnSGVCjkrG79wB31Tc=';
                } 
                else {
                    // Lil bit of cringe string formatting
                    let img_link_string = String(this.events[i].artist.img_link);
                    img_link_string = img_link_string.split(",")[0].replace("[","").replace("]","").replace(/'/g, '');
                    this.events[i].artist.img_link = img_link_string;
                }
            }
        },
        getEvents() {
            // Testing fetching token
            // let token = JSON.parse( localStorage.getItem('token') );
            // console.log(token);

            this.loadingSearch = true;

            // Formatting the input for searching
            this.city.toLowerCase;
            this.city = this.city.charAt(0).toUpperCase() + this.city.slice(1);

            // API: event/?city=Ljubljana&country=Slovenia
            getAPI
                .get('event/?city=' + this.city + '&country=' + this.country)
                .then((response) => {
                    console.log(response.data);
                    this.events = response.data;
                    
                    if (this.events.length == 0 ) {
                        this.noMovies = true;
                    } else {
                        this.noMovies = false;
                    }
                })
                .catch((err) => {
                    console.log(err);
                    this.noMovies = true;
            });

            // To make the loading bar go brr
            setTimeout(() => { this.loadingSearch = false; this.checkPictures() } , 2000);
        }
    },
}
</script>