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
  import { parseURI } from "./modules/utils";

  export default {
    name: 'app',
    components: {
      AppNavBar,
      Home
    },

    data(){
      return {
        isAuthenticated: false,
        args: {}
      }
    },
    mounted(){
      hook.app = this;
      // this.args = parseURI();
      // console.log('uri args: ', this.args);
      // if ('activate' in this.args){
      //   this.$router.push({name: 'activate', params: { id: 2 }});
      // }
    },

    methods: {},
  }
</script>

<style>

  .centered {
    color: gray;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  .capitalize {
    text-transform: capitalize !important;
  }

  .theme {
    color: forestgreen;
    font-weight: bold;
  }

  .theme-banner {
    background-color: forestgreen;
    /*font-weight: bold;*/
    color: white;
  }

  .bold {
    font-weight: bold !important;
  }

  button.theme {
    min-width: 6rem;
    background-color: orange;
    border-color: orange;
    font-weight: bold;
    color: white;
  }
  button.theme:hover:enabled, button.theme.active:enabled {
    background-color: darkorange !important;
    border-color: darkorange !important;
    font-weight: bold;
    color: white;
  }

  button.theme:disabled{
    background-color: rgba(153, 61, 0, 0.3);
    cursor: not-allowed;
    color: gray;
  }

  button.theme:disabled:hover{

  }

  .btn-danger {
    min-width: 6rem;
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
