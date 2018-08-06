<template>
  <div id="map-container">
    <mgl-map
            :accessToken="$root.config.accessToken"
            :mapStyle.sync="$root.config.mapStyle"
            :center="$root.config.center"
            :zoom="$root.config.zoom">

      <mgl-navigation-control position="top-left"/>
      <mgl-geolocate-control position="top-left" />

      <!-- add Breweries from our database -->
      <mgl-geojson-layer
              v-if="brewerySource"
              type="fill"
              :sourceId="'Breweries'"
              :layerId="'Breweries'"
              :source.sync="brewerySource">
      </mgl-geojson-layer>

    </mgl-map>

  </div>
  
</template>

<script>
  // import mapboxgl from 'mapbox-gl';
  import api from '../modules/api';
  hook.api = api;
  import {
    MglMap,
    MglNavigationControl,
    MglGeolocateControl,
    MglGeojsonLayer
  } from 'vue-mapbox';


  export default {
    name: "map-view",
    components: {
      MglMap,
      MglNavigationControl,
      MglGeolocateControl,
      MglGeojsonLayer
    },
    data(){
      return {
        map: null,
        brewerySource: null
      }
    },
    async mounted(){
      console.log('mapview is: ', this);
      console.log('mapgl: ', MglMap)
      hook.mp = this;

      this.brewerySource = await api.getBreweries();
      console.log('brewerySource: ', brewerySource)
      // mapboxgl.accessToken = this.$root.config.accessToken;
      // this.map = new mapboxgl.Map({
      //   container: 'map', // container id
      //   style: this.$root.config.mapStyle,
      //   center: [-93.50, 44], // starting position [lng, lat]
      //   zoom: 9 // starting zoom
      // });
    }
  }
</script>

<style>
  .mapboxgl-map {
    width: 100%;
    height: 500px;
  }

  /* need to override this */
  .mapboxgl-canvas{
    position: relative !important;
  }

</style>