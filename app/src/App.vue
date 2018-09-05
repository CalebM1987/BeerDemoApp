<template>
  <div id="app">

    <!-- App Navbar -->
    <app-nav-bar @user-logged-in="isAuthenticated = true" @user-logged-out="isAuthenticated = false"></app-nav-bar>

    <!-- ROUTER VIEW -->
    <home :userIsAuthenticated="isAuthenticated"></home>

  </div>
</template>

<script>
  import AppNavBar from './components/AppNavBar';
  import Home from './components/Home/Home';

  export default {
    name: 'app',
    components: {
      AppNavBar,
      Home
    },

    data(){
      return {
        isAuthenticated: false,
      }
    },
    mounted(){hook.app = this;},

    methods: {},
  }
</script>

<style>

  .control-btn-active {
    background-color: orange;
  }

  .control-btn-active > button {
    color: white !important;
  }

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    /*margin-top: 60px;*/
  }

</style>
