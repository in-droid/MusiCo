<template>
  <v-toolbar class="elevation-0 blue-grey darken-1">
    <v-toolbar-title style="cursor: pointer" to="/">
      <v-btn x-large text to="/" class="ml-10"> <v-img width="70" height="100" src="@/assets/logo_white.png"></v-img> </v-btn>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn x-large text to="/events" class="white--text">Events</v-btn>
    <v-spacer></v-spacer>
    <v-btn x-large text to="/allartists" class="white--text">Artists</v-btn>
    <v-spacer></v-spacer>
    <!-- Sign in button is in here as well -->
    <div width="50%" class="mr-10">
      <Login />

    </div>
  </v-toolbar>
</template>


<script>
export default {
  components: {
    Login: () => import("@/components/Login"),
  },
};
</script>