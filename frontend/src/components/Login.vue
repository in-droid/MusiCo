<template>
  <v-main>
    <v-btn v-if="!checkToken()" x-large text @click="dialog = true" class="white--text">Profile</v-btn>
    <v-btn v-if="checkToken()" to="/myProfile" x-large text class="green--text">Profile</v-btn>

    <v-dialog v-model="dialog" max-width="600px" min-width="360px">
      <div>
        <v-tabs
          v-model="tab"
          show-arrows
          background-color="grey darken-2 "
          icons-and-text
          dark
          grow
        >
          <v-tabs-slider color="grey lighten-1"></v-tabs-slider>
          <v-tab v-for="tab in tabs" :key="tab.id">
            <v-icon large>{{ tab.icon }}</v-icon>
            <div class="caption py-1">{{ tab.name }}</div>
          </v-tab>
          <v-tab-item>
            <v-card class="px-4">
              <v-card-text>
                <v-form ref="loginForm" v-model="valid" lazy-validation>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        v-model="loginUsername"
                        :rules="loginUsernameRules"
                        label="Username"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="loginPassword"
                        :append-icon="show1 ? 'eye' : 'eye-off'"
                        :rules="[rules.required, rules.min]"
                        :type="show1 ? 'text' : 'password'"
                        name="input-10-1"
                        label="Password"
                        hint="At least 8 characters"
                        counter
                        @click:append="show1 = !show1"
                      ></v-text-field>
                    </v-col>
                    <v-col class="d-flex" cols="12" sm="6" xsm="12"> </v-col>
                    <v-spacer></v-spacer>

                    <v-col class="d-flex" cols="12" sm="4" xsm="12" align-end>
                      <v-btn
                        x-large
                        block
                        :disabled="!valid"
                        color="blue"
                        @click="validate"
                        v-if="!successLogin"
                      >
                        Login
                      </v-btn>

                      <v-alert v-if="successLogin" type="success"
                        >Logged in</v-alert
                      >
                    </v-col>
                  </v-row>
                </v-form>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card class="px-4">
              <v-card-text>
                <v-form ref="registerForm" v-model="valid" lazy-validation>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        v-model="username"
                        :rules="usernameRules"
                        label="Username"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="password"
                        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                        :rules="[rules.required, rules.min]"
                        :type="show1 ? 'text' : 'password'"
                        name="input-10-1"
                        label="Password"
                        hint="At least 8 characters"
                        counter
                        @click:append="show1 = !show1"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        block
                        v-model="verify"
                        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                        :rules="[rules.required, passwordMatch]"
                        :type="show1 ? 'text' : 'password'"
                        name="input-10-1"
                        label="Confirm Password"
                        counter
                        @click:append="show1 = !show1"
                      ></v-text-field>
                    </v-col>
                    <v-spacer></v-spacer>
                    <v-col class="d-flex ml-auto" cols="12" sm="4" xsm="12">
                      <v-btn
                        x-large
                        block
                        :disabled="!valid"
                        color="blue"
                        @click="validate"
                        v-if="showRegister"
                        >Register</v-btn
                      >
                      <v-alert v-if="successRegister" type="success"
                        >User registered</v-alert
                      >

                      <v-alert v-else-if="failedRegister" type="error"
                        >User already exists</v-alert
                      >
                    </v-col>
                  </v-row>
                </v-form>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs>
      </div>
    </v-dialog>
  </v-main>
</template>

<script>
import { getAPI } from "../axios-api.js";

export default {
  name: "Login",

  computed: {
    passwordMatch() {
      return () => this.password === this.verify || "Password must match";
    },
  },
  methods: {
    beforeDestroy () {
      localStorage.removeItem('token');
    },
    checkToken() {
      return JSON.parse(localStorage.getItem('token')) != null;
    },
    validate() {
      // Log in
      if (this.$refs.loginForm.validate()) {
        getAPI
          .post("/user/login/", {
            username: this.loginUsername,
            password: this.loginPassword,
          })
          .then((response) => {
            const message = response.data.data.message; // ? Because the response's json is already called data
            const token = response.data.token;

            localStorage.setItem( 'token', JSON.stringify(token) );

            console.log("Message: " + message, "\nTOKEN: " + token);
            console.log("User: " + this.loginUsername + " logged succesfully");
            this.successLogin = true;
          })
          .catch((err) => {
            console.log(err);
          });
      }

      // Registration
      else if (this.$refs.registerForm.validate()) {
        getAPI
          .post("/user/register/", {
            username: this.username,
            password: this.password,
            password2: this.password,
          })
          .then((response) => {
            const message = response.data.message; // ? Because the response's json is already called data
            const token = response.data.token;


            if (response.data.username == "A user with that username already exists.") {
              console.log("User already exists");
              this.successRegister = false;
              this.failedRegister = true;
              this.showRegister = false;
            } else {
              console.log("Message: " + message, "\nTOKEN: " + token);
              console.log("User: " + this.username + " registered succesfully");
              localStorage.setItem( 'token', JSON.stringify(token) );
              this.showRegister = false;
              this.successRegister = true;
              this.failedRegister = false;
            }
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },
  },
  data: () => ({
    dialog: false,
    tab: 0,
    tabs: [
      { id: 0, name: "Login", icon: "mdi-account" },
      { id: 1, name: "Register", icon: "mdi-account-outline" },
    ],
    valid: true,

    successLogin: false,
    showRegister: true,
    successRegister: false,
    failedRegister: false,

    username: "",
    password: "",
    verify: "",
    loginPassword: "",
    loginUsername: "",
    loginUsernameRules: [
      (v) => !!v || "Required",
      (v) => /^[a-zA-Z0-9]+$/.test(v) || "Username must be valid",
    ],
    usernameRules: [
      (v) => !!v || "Required",
      (v) => /^[a-zA-Z0-9]+$/.test(v) || "Username must be valid",
    ],

    show1: false,
    rules: {
      required: (value) => !!value || "Required.",
      min: (v) => (v && v.length >= 8) || "Min 8 characters",
    },
  }),
};
</script>

<style></style>
