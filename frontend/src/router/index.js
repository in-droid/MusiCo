import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home'
import Events from '../views/Events'
import Concert from '../views/Concert'
import AllArtists from '../views/AllArtists'
import ArtistDetails from '../views/ArtistDetails'
import MyProfile from '../views/MyProfile'

Vue.use(VueRouter)

const routes = [{
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/events',
    name: 'Events',
    component: Events
  },
  {
    path: '/myProfile',
    name: 'MyProfile',
    component: MyProfile
  },
  {
    path: '/allartists',
    name: 'AllArtists',
    component: AllArtists
  },
  {
    path: '/artistdetails/:id',
    name: 'artistdetails',
    component: ArtistDetails,
    props: true,
  },
  {
    path: '/concert/:id',
    name: 'concert',
    component: Concert,
    props: true,
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router