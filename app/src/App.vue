<template>
  <div id="app">

    <!-- App Navbar -->
    <app-nav-bar />

    <!-- ROUTER VIEW -->
    <keep-alive>
      <router-view></router-view>
    </keep-alive>


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
    mounted(){
      hook.app = this;
    },

    methods: {},
  }
</script>

<style>

  .theme {
    color: forestgreen;
    font-weight: bold;
  }

  .theme-banner {
    background-color: forestgreen;
    font-weight: bold;
    color: white;
  }

  button.theme {
    min-width: 6rem;
    background-color: orange;
    border-color: orange;
    font-weight: bold;
    color: white;
  }

  button.theme:hover {
    background-color: darkorange;
    border-color: darkorange;
    font-weight: bold;
    color: white;
  }
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
  }

</style>
