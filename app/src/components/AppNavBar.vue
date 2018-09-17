<template>
  <b-navbar toggleable="md" type="dark" class="theme-banner app-header" fixed>
    <b-navbar-brand href="#"><strong>Brewery Finder</strong></b-navbar-brand>

    <b-navbar-nav class="ml-auto">

      <span v-if="userLoggedIn" v-b-modal.export-modal>
        <i class="fas fa-external-link-alt mr-2 download-btn app-nav-btn"
           title="export brewery data">
        </i>
      </span>

      <span @click="userLoggedIn ? logout(): showModal = true"
            :title="`sign ${ userLoggedIn ? 'out': 'in' }`">
        <font-awesome-icon
                prefix="fas"
                icon="user-circle"
                :class="['login-btn', 'app-nav-btn', {'logged-in': userLoggedIn}]">
        </font-awesome-icon>
      </span>

    </b-navbar-nav>

    <!--  PLACEHOLDER FOR LOGIN MODAL -->
    <b-modal id="login-modal" :hide-footer="true" ref="loginModal" v-model="showModal">
      <login-page @user-logged-in="handleLogin" @dismiss-login-modal="dismissLogin"></login-page>
    </b-modal>

    <!-- PLACEHOLDER FOR LOGOUT MODAL -->
    <b-modal id="logout-modal" v-model="showLogout" :hide-footer="true">
      <div class="logout-container">
        <spinner :text="'Logging Out'" :visible="state === 'logging_out'" />
        <b-alert :show="2" v-if="state === 'logged_out'" @dismissed="showLogout = false" variant="success">Successfully Logged Out</b-alert>
      </div>
    </b-modal>

    <!-- PLACEHOLDER FOR EXPORT DATA MODAL -->
    <b-modal id="export-modal"
             title="Export Data"
             header-text-variant="secondary"
             body-text-variant="secondary"
             cancel-variant="danger"
             @ok="exportData"
             ok-title="Export Data">
      <b-card>
        <b-form-select v-model="selectedTable" :options="exportTables" class="mt-3 mb-3"/>
        <b-form-group label="Export Format" v-if="selectedTable === 'breweries'" label-class="bold mt-2">
          <b-form-radio-group v-model="selectedExportType" :options="exportOptions"/>
        </b-form-group>

        <!-- slot to override ok button -->
        <div slot="modal-ok">
          <b-button class="theme">Export Data</b-button>
        </div>
      </b-card>

    </b-modal>

  </b-navbar>
</template>

<script>
  import api from '../modules/api';
  import LoginPage from './Home/LoginPage';
  import Spinner from './UI/Spinner';
  import { EventBus } from "../modules/EventBus";

  export default {
    name: "app-nav-bar",
    components: {
      LoginPage,
      Spinner
    },
    data() {
      return {
        state: null,
        showModal: false,
        userLoggedIn: false,
        showLogout: false,
        selectedTable: null,
        selectedExportType: null,
        exportTables: [
          { value: null, text: 'Select table to export' },
          { value: 'breweries', text: 'Breweries' },
          { value: 'beers', text: 'Beers' },
          { value: 'styles', text: 'Beer Styles' },
          { value: 'categories', text: 'Beer Categories' }
        ],
        exportOptions: [
          { value: 'csv', text: 'CSV' },
          { value: 'shapefile', text: 'Shapefile' }
        ]
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
      async logout(){
        this.showLogout = true;
        this.state = 'logging_out';
        const resp = await api.logout();
        this.userLoggedIn = false;
        this.state = 'logged_out';

        // bubble up logout event
        EventBus.$emit('user-logged-out');
        return resp;
      },

      dismissLogin(){
        this.$refs.loginModal.hide();

        // for some reason the modal dismiss was causing a race condition and interfering with the router...
        setTimeout(()=>{
          this.$router.push('/sign-up');
        }, 100)
      },

      handleLogin(){
        this.userLoggedIn = true;
        this.state = 'logged_in';
        this.showModal = false;

        // bubble up login event
        EventBus.$emit('user-logged-in');
      },

      async exportData(){

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

  /*.app-header {*/
    /*background-color: forestgreen;*/
  /*}*/

  .app-nav-btn {
    font-size: 2.5rem;
    color: white;
    cursor: pointer;
  }

  .download-btn:hover {
    color: orange;
    /*background-color: white;*/
    /*-webkit-border-radius: 50%;*/
    /*-moz-border-radius: 50%;*/
    /*border-radius: 50%;*/
  }

  .login-btn:hover{
    background-color: orange;
    font-weight: bold;
    -webkit-border-radius: 50%;
    -moz-border-radius: 50%;
    border-radius: 50%;
    color: lightgray;
  }

  .logged-in{
    color: orange !important;
    background-color: white;
    -webkit-border-radius: 50%;
    -moz-border-radius: 50%;
    border-radius: 50%;
  }

  .logged-in:hover {
    color: darkorange !important;
    background-color: lightgray !important;
  }

</style>