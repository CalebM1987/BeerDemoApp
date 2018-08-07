<template>
  <div class="map-container">
    <mapbox
            :access-token="$root.config.accessToken"
            :map-options="{
                style: $root.config.mapStyle,
                center: $root.config.center,
                zoom: $root.config.zoom
            }"
            :nav-control="{
              show: true,
              position: 'top-left'
            }"
            :geolocate-control="{
                show: true,
                position: 'top-left'
            }"
            :scale-control="{
                show: true,
                position: 'bottom-right'
            }"
            @map-init="mapInitialized"
            @map-load="mapLoaded"
            @map-click="mapClick">
    </mapbox>
  </div>
  
</template>

<script>
  import Mapbox from 'mapbox-gl-vue';
  import api from '../modules/api';
  import { MenuButtonControl } from '../modules/MenuButtonControl';
  import { EventBus } from "../modules/EventBus";

  export default {
    name: "map-view-mglv",
    components: {
      Mapbox
    },
    data() {
      return {
        map: null,
        selectionMarker: null
      }
    },
    mounted(){
      hook.mp = this;
      // listen for sidebar to open and update left position
      EventBus.$on('sidebar-expanded', (expanded)=>{
        console.log('exanded sidebar: ', expanded);
        document.querySelector('#map').style.left = `${expanded ? 350: 0}px`;
      });
    },
    methods: {
      mapInitialized(map){
        console.log('map initialized: ', map);
        this.map = map;

        // // add menu button for slideout
        // map.addControl(new MenuButtonControl(), 'top-left');

      },

      async mapLoaded(map){
        const brewerySource = await api.getBreweries();
        this.brewerySource = brewerySource;
        console.log('brewerySource: ', brewerySource);

        map.loadImage('./assets/beer.png', function (error, image) {
          if (error) throw error;
          map.addImage('beer', image);
          map.addLayer({
            "id": "breweries",
            "type": "symbol",
            "source": {
              "type": "geojson",
              "data": brewerySource
            },
            "layout": {
              "icon-image": "beer",
              "icon-size": 0.1,
              "text-field": "{name}",
              "text-size": 10,
              "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
              "text-offset": [0, 1.2],
              "text-anchor": "top"
            }
          });
        });
        // add menu button for slideout
        map.addControl(new MenuButtonControl(), 'top-left');
      },

      mapClick(map, e){
        console.log('map click: ', e);

        // find features
        const features = map.queryRenderedFeatures(e.point, {
          layers: ['breweries']
        });

        console.log('found features: ', features);
        if (features.length){
          const feature = features[0];
          this.$emit('brewery-identified', feature);

          // emit menu-expanded as well to ensure it is always open when feature is selected
          EventBus.$emit('toggle-menu', true);

          // add marker to map
          if (!this.selectionMarker){
            this.selectionMarker = new mapboxgl.Marker({color: 'red'})
                .setLngLat(feature.geometry.coordinates)
                .addTo(map);
          } else {
            this.selectionMarker.setLngLat(feature.geometry.coordinates)
          }
        }

      }

    }
  }
</script>

<style>
  #map {
    position:absolute;
    top: 60px;
    bottom:0;
    right: 0;
    left: 0;
    /*width:100%;*/
  }

  /* need to override this */
  .mapboxgl-canvas{
    position: relative !important;
  }

</style>