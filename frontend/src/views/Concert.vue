<template>
    <v-main>
        <NavBar/>
        <v-card width="70%" class="mx-auto my-10 elevation-0">
            <v-parallax height="500" style="border-radius=10px" src="https://i.pinimg.com/originals/4a/94/26/4a94268541d7a0ed95a8be5138e8a288.jpg">
                <div >
                    <v-card class="elevation-0 " color="transparent" >
                        <v-row>
                            <v-col>
                                <v-card class="elevation-0 my-auto" color="transparent" >
                                    <div class="ml-10">
                                            
                                            <h1 class="red--text text--darken-1 font-weight-medium font-italic" style="font-size: 3em">{{date}}</h1>
                                        
                                        <h1 class="white--text font-weight-bold my-10" height="400" style="font-size: 4.7em; font-family: 'Verdana'">{{artist_name}}</h1>
                                        
                                            
                                        
                                    </div>
                                </v-card>
                            </v-col>
                            <v-col>
                                <v-card class="elevation-0 my-5" color="transparent">
                                    <v-img :src="artist_img" lazy-src="https://miro.medium.com/max/880/0*H3jZONKqRuAAeHnG.jpg" width="400" height="300" class="mx-auto"></v-img>
                                </v-card>
                            </v-col>
                        </v-row>
                    </v-card>
                </div>
            </v-parallax>
            <v-row class="my-10">
                <v-col>
                    <v-card class="elevation-0">
                        <div class="text-center">
                            <h1 class="font-weight-bold red--text text--darken-1 " style="font-family: 'Verdana'">Venue Details</h1>
                            <h1 class="my-10 text--darken-1 font-weight-medium" style="font-size: 3em; font-family: 'Verdana'">{{venue_name}}</h1>
                            <h2 class="font-weight-light">{{venue_info}}</h2>
                        </div>                      
                    </v-card>
                </v-col>
                <v-col>
                    <v-card class="elevation-0">
                        <div class="text-center">
                            <h1 class="font-weight-bold red--text text--darken-1 " style="font-family: 'Verdana'">Additional Details</h1>
                            <h2 class="my-10 font-weight-light">{{add_info}}</h2>
                        </div> 
                    </v-card>
                </v-col>
            </v-row>
        </v-card>
    </v-main>
</template>
<script>
import NavBar from '@/components/NavBar';


export default {
    name: 'Concert',
    components: {NavBar},
    props: {
        id: {
            type: String,
            required: true,
        },
        artist_name: {
            type: String,
            required: true,
        },
        artist_img: {
            type: String,
            required: true,
        },
        date: {
            type: String,
            required: true,
        },
        venue_name: {
            type: String,
            required: true,
        },
        venue_info: {
            type: String,
            required: true,
        },
        add_info: {
            type: String,
            required: true,
        }
    }
}
</script>