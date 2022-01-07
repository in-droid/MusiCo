<template>
    <v-main>
        <NavBar/>
        <v-card width="70%" class="mx-auto my-10 elevation-0">
            
            <div >
                <v-parallax class="my" height="400" src="https://www.pier17ny.com/wp-content/uploads/2021/09/PassionPit-TheBeaches-Night1-115-1560x960.jpg">
                <v-card class="elevation-0 ml-5" color="transparent">
                    <h1 class="white--text font-weight-bold" style="font-size:3em; font-family: 'Verdana'" >Discover your favorite artists</h1>
                </v-card>
                <v-card class="elevation-0 font-weight-light font-italic my-5 ml-5" color="transparent">
                    <h3 class="white--text">Be the first to know about concerts, tour announcements <br> and news based on the music you love</h3>
                </v-card>
                <v-card class="elevation-0 ml-5" color="transparent" height="100">
                    <v-btn x-large class="my-10" color="green accent-3" to="/">Log in with Spotify</v-btn>
                </v-card>
                </v-parallax>
            </div>
            <div class="text-center my-5">
                <h2 class="font-weight-medium text-decoration-underline" style="font-family: 'Verdana'">Search for artists</h2>
                <v-row>
                    <v-text-field :loading="loadingSearch" v-model="name"  outline label="Search for an artist" append-icon="mdi-search" prepend-inner-icon="mdi-account-music"></v-text-field>
                    <v-btn @click="getEvents" color="primary" x-large elevation="1" plain icon >
                        <v-icon>mdi-magnify</v-icon>
                    </v-btn>
                </v-row>
            </div>
            <div class="text-center " v-if="noArtists">
                <v-card class="elevation-0 my-5">
                    <h1 style="font-size: 2.5em; font-family: 'Verdana'" class="red--text text--darken-1 font-weight-bold " >Most popular artists worldwide</h1>
                </v-card>
                <v-card class="elevation-0 my-5">
                    <v-row>
                        <v-col>
                            <v-card class="elevation-1 my-5">
                                <v-img height="300" width="300" class="mx-auto" src="https://media.nu.nl/m/7w3x7mza4otb_sqr256.jpg/drake-reageert-voor-het-eerst-op-festivaldrama-na-aanklacht-hart-is-gebroken.jpg"></v-img>
                                <h3 class="my-4" style="font-family: 'Verdana'">Drake</h3>
                            </v-card>
                        </v-col>
                        <v-col>
                            <v-card class="elevation-1 my-5">
                                <v-img height="300" width="300" class="mx-auto" src="https://i.scdn.co/image/ab6761610000e5ebcdce7620dc940db079bf4952"></v-img>
                                <h3 class="my-4" style="font-family: 'Verdana'">Ariana Grande</h3>
                            </v-card>
                        </v-col>
                        <v-col>
                            <v-card class="elevation-1 my-5">
                                <v-img height="300" width="300" class="mx-auto" src="https://iscale.iheart.com/catalog/artist/744880"></v-img>
                                <h3 class="my-4" style="font-family: 'Verdana'">The Weeknd</h3>
                            </v-card>
                        </v-col>
                        <v-col>
                            <v-card class="elevation- my-5">
                                <v-img height="300" width="300" class="mx-auto" src="https://mogujatosama.rs/sites/default/files/images/5(626).jpg"></v-img>
                                <h3 class="my-4" style="font-family: 'Verdana'">Adele</h3>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-card>
                
            </div>
            <v-card class="elevation-0 my-5">
                <v-row>
                    <v-col v-for="artist in filtered" :key="artist.id" md="3" xs="12">          
                            <v-card
                                class="elevation-1 my-5 mx-auto"
                            >
                                <v-img
                                height="300" width="300" class="mx-auto"
                                :src="artist.img_link"
                                lazy-src="https://miro.medium.com/max/880/0*H3jZONKqRuAAeHnG.jpg"
                                >
                                </v-img>
                                <div class="text-center">
                                    <h3 class="my-4">
                                        <router-link
                                        class="link-style black--text"
                                        style="text-decoration:none; font-family: 'Verdana'"
                                        :to="{name: 'artistdetails', params: {id:artist.id, name: artist.name, genres: artist.genres, img: artist.img_link}}"
                                        >
                                        {{ artist.name }}
                                        </router-link>    
                                    </h3>   
                                </div>

                            </v-card>
                    </v-col>
                </v-row>
            </v-card>
            
        </v-card>

    </v-main>
</template>

<script>
import NavBar from '@/components/NavBar';

import { getAPI } from "../axios-api.js";

export default {
    name: 'Artists',
    components: {NavBar},
    data: () => ({
        loadingSearch: false,
        noArtists:true,
        
        name: '',
        artists: [
        ],
        filtered: [

        ]
    }),
    methods: {
        checkPictures() {
            for (let i = 0; i < this.artists.length; i++) {
                // Event gets default image if it doesn't have the artist image
                if (this.artists[i].img_link === null) {
                    this.artists[i].img_link = 'https://media.istockphoto.com/photos/concert-stage-on-rock-festival-music-instruments-silhouettes-picture-id1199243596?k=20&m=1199243596&s=612x612&w=0&h=5L3fWhbB4YtVOPsnnqrUg22FaHnSGVCjkrG79wB31Tc=';
                }
            }
        },
        getEvents() {
            this.loadingSearch = true;

            // Formatting the input for searching
            this.name.toLowerCase;
            this.name = this.name.charAt(0).toUpperCase() + this.name.slice(1);

            getAPI
                .get('artist/')
                .then((response) => {

                    
                    //this.filtered = []
                    this.artists = response.data;
                    this.artists.forEach(element => {
                        if(element.name.includes(this.name)){
                            this.filtered.push(element);
                        }
                    });
                    
                    if (this.artists.length == 0 ) {
                        this.noArtists = true;
                    } else {
                        this.noArtists = false;
                    }
                })
                .catch((err) => {
                    console.log(err);
                    this.noArtists = true;
            });

            // To make the loading bar go brr
            setTimeout(() => { this.loadingSearch = false; this.checkPictures() } , 2000);
        }
    },
}
</script>