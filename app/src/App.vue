<template>
  <div id="app">
    <app-nav-bar></app-nav-bar>

    <!--<mgl-map-->
            <!--:accessToken="$root.config.accessToken"-->
            <!--:mapStyle.sync="$root.config.mapStyle">-->
    <!--</mgl-map>-->
    <!--<Slideout :toggleSelectors="['.test-btn']" @on-open="slideoutOpened">-->

    <!--</Slideout>-->
    <sidebar>
      <!-- slot for sidebar content -->
      <brewery-info :feature="selectedBrewery" v-if="selectedBrewery"></brewery-info>

    </sidebar>
    <map-view
      @brewery-identified="showBreweryInfo">

    </map-view>

  </div>
</template>

<script>
// import Mapbox from 'mapbox-gl-vue';
// import { MglMap } from 'vue-mapbox'
import MapView from './components/MapViewMglv';
import AppNavBar from './components/AppNavBar';
import Slideout from 'vue-slideout';
import Sidebar from './components/Sidebar';
import BreweryInfo from './components/BreweryInfo';

export default {
  name: 'app',
  components: {
    // Mapbox
    // MglMap
    AppNavBar,
    MapView,
    Slideout,
    Sidebar,
    BreweryInfo
  },

  data(){
    return {
      selectedBrewery: null
    }
  },

  methods: {
    slideoutOpened(){
      console.log('slideout opened');
    },

    showBreweryInfo(brewery){
      this.selectedBrewery = brewery;
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
