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

    <!--  PLACEHOLDER FOR MODAL -->
    <b-modal id="login-modal" :hide-footer="true" ref="loginModal" v-model="showModal">
      <login-page @user-logged-in="handleLogin"></login-page>
    </b-modal>

  </b-navbar>
</template>

<script>
  import api from '../modules/api';
  import LoginPage from './LoginPage';

  export default {
    name: "app-nav-bar",
    components: {
      LoginPage
    },
    data() {
      return {
        showModal: false,
        userLoggedIn: false,
        logStyle: {
          color: 'gainsboro',
          'font-size': '2.5rem',
          cursor: 'pointer'
        }
      }
    },
    mounted(){hook.nb = this;},
    methods: {
      logout(){
        this.$emit('user-logged-out');
        console.log('user logged out')
        this.userLoggedIn = false;
        return api.logout();
      },

      handleLogin(){
        this.userLoggedIn = true;
        this.showModal = false;
      }
    }
  }
</script>

<style scoped>

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