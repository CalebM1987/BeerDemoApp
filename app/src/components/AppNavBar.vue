<template>
  <b-navbar toggleable="md" type="dark" class="app-header" fixed>
    <b-navbar-brand href="#"><strong>Brewery Finder</strong></b-navbar-brand>

    <b-navbar-nav class="ml-auto">

      <span @click="userLoggedIn ? logout(): showModal = true"
            :title="`sign ${ userLoggedIn ? 'out': 'in' }`">
        <font-awesome-icon
                prefix="fas"
                icon="user-circle"
                :class="['login-btn', {'logged-in': userLoggedIn}]">
        </font-awesome-icon>
      </span>

    </b-navbar-nav>

    <!--  PLACEHOLDER FOR LOGIN MODAL -->
    <b-modal id="login-modal" :hide-footer="true" ref="loginModal" v-model="showModal">
      <login-page @user-logged-in="handleLogin"></login-page>
    </b-modal>

    <!-- PLACEHOLDER FOR LOGOUT MODAL -->
    <b-modal id="logout-modal" v-model="showLogout" :hide-footer="true">
      <div class="logout-container">
        <div class="logout-spinner" v-if="state === 'logging_out'">
          <h4>Logging Out</h4>
          <span style="font-size: 2.5rem;" class="fas fa-spinner fa-spin"></span>
        </div>
        <b-alert :show="2" v-if="state === 'logged_out'" @dismissed="showLogout = false" variant="success">Successfully Logged Out</b-alert>
      </div>
    </b-modal>

  </b-navbar>
</template>

<script>
  import api from '../modules/api';
  import LoginPage from './Home/LoginPage';
  import { EventBus } from "../modules/EventBus";

  export default {
    name: "app-nav-bar",
    components: {
      LoginPage
    },
    data() {
      return {
        state: null,
        showModal: false,
        userLoggedIn: false,
        showLogout: false
      }
    },
    mounted: async function(){
      // check if user is already logged in via the remember me token cookie
      try {
        const resp = await api.authTest();
        if (resp.status === 'success'){
          this.userLoggedIn = true;
        }
      } catch (err){
        // ignore, just means user isn't authenticated from a prior session
      }

      hook.nb = this;
    },
    methods: {
      logout: async function(){
        this.showLogout = true;
        this.state = 'logging_out';
        const resp = await api.logout();
        this.userLoggedIn = false;
        this.state = 'logged_out';

        // bubble up logout event
        EventBus.$emit('user-logged-out');
        return resp;
      },

      handleLogin(){
        this.userLoggedIn = true;
        this.state = 'logged_in';
        this.showModal = false;

        // bubble up login event
        EventBus.$emit('user-logged-in');
      }
    }
  }
</script>

<style scoped>

  .logout-container {
    margin: auto;
    margin-top: 2rem;
    margin-bottom: 2rem;
  }

  .logout-spinner {
    color: gray;
  }

  .app-header {
    background-color: forestgreen;
  }

  .logged-in {
    color: orange !important;
    background-color: white;
    border-radius: 50%;
  }

  .login-btn{
    color: gainsboro;
    font-size: 2.5rem;
    cursor: pointer;
  }

  .login-btn:hover{
    background-color: orange;
    font-weight: bold;
    border-radius: 50%;
    color: lightgray;
  }

  .logged-in:hover {
    color: darkorange !important;
    background-color: lightgray !important;
  }

</style>