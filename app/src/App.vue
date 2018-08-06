<template>
  <div id="app">
    <!--<mapbox-->
      <!--:access-token="$root.config.mapbox_token"-->
      <!--:map-options="{-->
      <!--style: 'mapbox://styles/mapbox/light-v9',-->
      <!--center: [-93, 44.8],-->
      <!--zoom: 3-->
      <!--}"-->
      <!--:geolocate-control="{-->
      <!--show: true,-->
      <!--position: 'top-left'-->
      <!--}"-->
      <!--:scale-control="{-->
      <!--show: true,-->
      <!--position: 'top-left'-->
      <!--}"-->
      <!--:fullscreen-control="{-->
      <!--show: true,-->
      <!--position: 'top-left'-->
    <!--}">-->
    <!--</mapbox>-->

    <!--<mgl-map-->
            <!--:accessToken="$root.config.accessToken"-->
            <!--:mapStyle.sync="$root.config.mapStyle">-->
    <!--</mgl-map>-->
    <map-view></map-view>
  </div>
</template>

</div>
</template>

<script>
// import Mapbox from 'mapbox-gl-vue';
// import { MglMap } from 'vue-mapbox'
import MapView from './components/MapView';

export default {
  name: 'app',
  components: {
    // Mapbox
    // MglMap
    MapView
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
    margin-top: 60px;
  }

</style>
