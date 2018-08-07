<template>
  <div id="app">

    <!-- App Navbar -->
    <app-nav-bar></app-nav-bar>

    <sidebar ref="sidebar"
      @toggled="handleExpand">

      <!-- slot for sidebar content -->
      <brewery-info
              v-if="identifyActive"
              :feature="selectedBrewery">
      </brewery-info>

    </sidebar>

    <map-view
            ref="mapView"
            @toggle-identify="identifyActivePanel"
            @brewery-identified="showBreweryInfo"
            @toggle-menu="menuActivePanel">
    </map-view>

  </div>
</template>

<script>
import MapView from './components/MapViewMglv';
import AppNavBar from './components/AppNavBar';
import Sidebar from './components/Sidebar';
import BreweryInfo from './components/BreweryInfo';

export default {
  name: 'app',
  components: {
    AppNavBar,
    MapView,
    Sidebar,
    BreweryInfo
  },

  data(){
    return {
      selectedBrewery: null,
      menuActive: true,
      identifyActive: false
    }
  },

  methods: {

    showBreweryInfo(brewery){
      // force panel to open with identify active
      this.selectedBrewery = brewery;
      if (brewery){
        this.$refs.sidebar.expand();
        this.menuActive = false;
        this.identifyActive = true;
      }
    },

    menuActivePanel(){
      // if identify is shown, toggle on menu
      if (this.identifyActive && this.$refs.sidebar.active){
        this.identifyActive = false;
        this.menuActive = true;
      } else {
        this.identifyActive = false;
        this.menuActive = true;
        this.$refs.sidebar.toggle();
      }

    },

    identifyActivePanel(){
      if (this.menuActive && this.$refs.sidebar.active){
        this.menuActive = false;
        this.identifyActive = true;
      } else {
        this.menuActive = false;
        this.identifyActive = true;
        this.$refs.sidebar.toggle();
      }
    },

    handleExpand(expanded){
      console.log('sidebar toggled: ', expanded);
      // listen for sidebar to open and update move map's left position
      document.querySelector('#map').style.left = `${expanded ? 350: 0}px`;

    }
  }
}
</script>

<style>

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    /*margin-top: 60px;*/
  }

</style>
