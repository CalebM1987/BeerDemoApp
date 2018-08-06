<template>
  <div id="map">


  </div>
  
</template>

<script>
  import mapboxgl from 'mapbox-gl';
  import api from '../modules/api';
  hook.api = api;



  export default {
    name: "map-view",
    components: {
    },
    data(){
      return {
        map: null,
        brewerySource: null
      }
    },
    async mounted(){
      console.log('mapview is: ', this);
      // console.log('mapgl: ', MglMap)
      hook.mp = this;

      // set access token
      mapboxgl.accessToken = this.$root.config.accessToken;

      // initialize map
      const map = new mapboxgl.Map({
        container: 'map', // container id
        style: this.$root.config.mapStyle,
        center: this.$root.config.center, // starting position [lng, lat]
        zoom: this.$root.config.zoom // starting zoom
      });

      // some es6 functions will not work here, using arrow functions breaks the app. ¯\_(ツ)_/¯
      let brewerySource;
      const _this = this;
      api.getBreweries().then(function(resp){
        brewerySource = resp;
        _this.brewerySource = brewerySource;
        console.log(brewerySource);

        map.on('load', function() {
          map.loadImage('./assets/beer.png', async function (error, image) {
            if (error) throw error;
            map.addImage('beer', image);
            map.addLayer({
              "id": "points",
              "type": "symbol",
              "source": {
                "type": "geojson",
                "data": brewerySource
              },
              "layout": {
                "icon-image": "beer",
                "icon-size": 0.1
              }
            });
          });

        });

      });

      this.map = map;

    }
  }
</script>

<style>
  #map {
    position:absolute;
    top: 60px;
    bottom:0;
    width:100%;
  }
  /*.mapboxgl-map {*/
    /*width: 100%;*/
    /*height: 500px;*/
  /*}*/

  /* need to override this */
  .mapboxgl-canvas{
    position: relative !important;
  }

</style>