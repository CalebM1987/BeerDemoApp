<template>
  <div class="map-container">
    <mapbox
            :access-token="$root.config.map.accessToken"
            :map-options="{
                style: $root.config.map.mapStyle,
                center: $root.config.map.center,
                zoom: $root.config.map.zoom
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
  import api from '../../modules/api';
  import { createControlButton } from "../../modules/MenuButtonControl";
  import { EventBus } from "../../modules/EventBus";
  hook.api = api;


  export default {
    name: "map-view-mglv",
    components: {
      Mapbox
    },
    props: {
      userIsAuthenticated: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        map: null,
        selectionMarker: null,
        state: 'default',
        canvas: null,
        addBreweryButton: null,
      }
    },
    mounted(){
      hook.mp = this;
      EventBus.$on('brewery-search-result', (feature)=>{
        this.handleIdentify(feature, true);
      });

      // update the brewery source when breweries have changed
      EventBus.$on('brewery-changed', async (obj)=>{
        console.log('brewery changed from map component: ', obj);
        this.map.getSource('breweries').setData(await api.getBreweries());
      });

    },
    methods: {
      mapInitialized(map){
        console.log('map initialized: ', map);
        this.map = map;

      },

      createAddBreweryButton(){
        const addButton = createControlButton({
          className: 'add-brewery',
          iconClass: 'fas fa-plus',
          onClick: this.addNewBrewery,
          title: 'add new brewery'
        });

        this.map.addControl(addButton, 'top-left');
        this.addBreweryButton = addButton;
      },

      deactivateAddBrewery(){
        this.state = 'default';
        this.canvas ? this.canvas.style.cursor = 'grab': null;
      },

      addNewBrewery(){
        console.log('clicked add new brewery!');
        if (this.state === 'adding'){
          this.deactivateAddBrewery();
          this.$emit('add-brewery-cancelled');
          return;
        }
        this.$emit('clicked-add-brewery');
        // set cursor to crosshair temporarily
        this.canvas = document.querySelector('.mapboxgl-canvas-container');
        this.canvas.style.cursor = 'crosshair';
        this.state = 'adding';
      },


      async mapLoaded(map){
        const brewerySource = await api.getBreweries();
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

        // add control buttons
        const toggleMenu =(evt)=>{
          this.$emit('toggle-menu');
        };

        const menuButton = createControlButton({
          className: 'expand-menu',
          iconClass: 'fas fa-bars',
          onClick: toggleMenu,
          title: 'expand menu'
        });

        map.addControl(menuButton, 'top-left');

        // add identify button
        const toggleIdentify =(evt)=>{
          this.$emit('toggle-identify');
        };

        const identifyButton = createControlButton({
          className: 'expand-identify',
          iconClass: 'fas fa-info',
          onClick: toggleIdentify,
          title: 'expand identify window'
        });
        map.addControl(identifyButton, 'top-left');

        // create add button if authenticated
        this.$root.userIsAuthenticated ? this.createAddBreweryButton(): null;
      },

      mapClick(map, e){
        console.log('map click: ', e);

        // find features
        if (this.state === 'default'){
          const features = map.queryRenderedFeatures(e.point, {
            layers: ['breweries']
          });

          console.log('found features: ', features);
          if (features.length){

            // handle selection on map
            const feature = features[0];
            this.handleIdentify(feature);
          } else if (this.selectionMarker){

            // clear selection on map and close identify
            this.selectionMarker.remove();
            this.selectionMarker = null;
            this.$emit('cleared-selection')
          }
        } else {
          this.$emit('new-brewery-point', e.lngLat);
        }
      },

      handleIdentify(feature, updateCenter=false){
        if (!feature){
          return;
        }
        this.$emit('brewery-identified', feature);

        // add marker to map
        if (!this.selectionMarker){

          this.selectionMarker = new mapboxgl.Marker({color: 'red'})
              .setLngLat(feature.geometry.coordinates)
              .addTo(this.map);
        } else {
          this.selectionMarker.setLngLat(feature.geometry.coordinates)//[feature.properties.x, feature.properties.y]
        }

        if (updateCenter){
          this.map.setCenter(feature.geometry.coordinates);
        }
      }
    },

    watch: {
      '$root.userIsAuthenticated'(newVal){
        if (newVal) {
          if (!this.addBreweryButton){
            this.createAddBreweryButton()
          }
        } else {
          if (this.addBreweryButton){
            this.map.removeControl(this.addBreweryButton);
            this.addBreweryButton = null;
          }
        }
      }
    }
  }
</script>

<style>
  #map {
    position: absolute;
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