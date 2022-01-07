<template>
    <v-main>
        <NavBar/>
        <v-card width="70%" class="mx-auto my-10 elevation-0">
                <v-parallax height="500" style="border-radius=10px" src="https://images.pexels.com/photos/3122799/pexels-photo-3122799.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940">
                    <div class="text-center">
                        <v-card class="elevation-0 " color="transparent" >
                            <v-row>
                                <v-col>
                                    <v-card class="elevation-0 my-auto" color="transparent" >
                                        <div class="text-center">
                                            <h3 class="white--text font-weight-medium" style="font-family: 'Verdana'">Artist:</h3>
                                            <h1 class="white--text font-weight-bold" height="400" style="font-size: 4.7em; font-family: 'Verdana'">{{name}}</h1>
                                        </div>
                                    </v-card>
                                </v-col>
                                <v-col>
                                    <v-card class="elevation-0" color="transparent">
                                        <v-img :src="img" lazy-src="https://miro.medium.com/max/880/0*H3jZONKqRuAAeHnG.jpg" width="400" height="300" class="mx-auto"></v-img>
                                    </v-card>
                                </v-col>
                            </v-row>
                        </v-card>
                    </div>
                </v-parallax>
                <template>
                <v-card class="mt-5 elevation-0">
                    <v-tabs centered>
                        <v-tab>Concerts</v-tab>
                        <v-tab>Genres</v-tab>
                        <v-tab-item>
                            <v-card class="mt-10 mx-auto elevation-0" width="70%">
                                <h1 style="font-family: 'Verdana'">Upcoming concerts</h1>
                            </v-card>
                            <v-card class="mt-10 mx-auto elevation-0" width="70%">
                                
                                <v-card>
                                    <v-expansion-panels focusable>
                                        <v-expansion-panel class="my-5">
                                            <v-expansion-panel-header>
                                                <v-row>
                                                    <v-col cols="2">
                                                        <div class="text-center">
                                                            <h3 class="font-weight-medium">mart</h3>
                                                            <h1 class="font-weight-bold my-2">04</h1>
                                                            <h3 class="font-weight-medium my-2">2022</h3>
                                                        </div>
                                                    </v-col>
                                                    <v-col cols="6">
                                                        <h1 class="red--text text--darken-1" style="font-family: 'Verdana'">Beogradska Arena</h1>
                                                        <h3 class="font-weight-light my-2" >Bulevar Arsenija Čarnojevica 58, Beograd 11070 </h3>
                                                        <h3 class="font-weight-thin my-2">22:00</h3>
                                                    </v-col>
                                                </v-row>
                                            </v-expansion-panel-header>
                                            <v-expansion-panel-content>
                                                <p class="my-10">The Štark Arena (Serbian Cyrillic: Штарк арена), also known as Belgrade Arena (Serbian Cyrillic: Београдска арена), is a multi-purpose indoor arena located in Belgrade, Serbia. It is designed as a universal hall for sports, cultural events and other programs. The venue is used for several different sports events, such as basketball, futsal, handball, judo, table tennis, tennis, volleyball, water polo, as well as for concerts.!</p>
                                            </v-expansion-panel-content>
                                        </v-expansion-panel>
                                    </v-expansion-panels>
                                </v-card>
                            </v-card>
                        </v-tab-item>
                        <v-tab-item>
                            <v-card class="mt-10 elevation-0">
                                <div class="text-center">
                                    <h1 style="font-family: 'Verdana'">Genres</h1>
                                </div>
                                <v-card class="my-10 elevation-0">
                                    <v-row>
                                        <v-col v-for="gen in genres" :key="gen"  md="4" xs="12">
                                            <v-card class="elevation-3">
                                                <div class="text-center">
                                                    <h1 class="red--text text--darken-1 font-italic" style="font-family: 'Verdana'">{{gen}}</h1>
                                                </div>                                            
                                            </v-card>
                                        </v-col>
                                    </v-row>
                                </v-card>
                                
                            </v-card>
                        </v-tab-item>
                    </v-tabs>
                </v-card>
                
            </template>
            </v-card>
    </v-main>
</template>

<script>

import NavBar from '@/components/NavBar';

export default {
    name: 'ArtistDetails',
    components: {NavBar},
    props: {
        id: {
            type: Number,
            required: false,
        },
        name: {
            type: String,
            required: false,
        },
        genres: {
            type: Array,
            required: false,
        },
        img: {
            type: String,
            required: false
        }
    }
}
</script>