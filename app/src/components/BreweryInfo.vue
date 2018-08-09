<template>
  <div class="brewery-info-container">
    <b-card>
      <h4><strong>{{ properties.name }}</strong></h4>
      <hr>
      <p>{{ properties.address }}</p>
      <p>{{ properties.city }}</p>
      <b-link :href="properties.website" target="_blank" v-if="properties.website">view website</b-link>


      <!-- featured beers -->
      <div v-if="featuredBeers.length">
        <hr>
        <h5><strong>Featured Beers</strong></h5>
        <b-list-group class="featured-beers-container">
          <b-list-group-item v-for="beer in featuredBeers">
            <featured-beer :beer="beer"></featured-beer>
          </b-list-group-item>

        </b-list-group>
      </div>

    </b-card>
  </div>
</template>

<script>
  import api from '../modules/api';
  import FeaturedBeer from './FeaturedBeer';

  export default {
    name: "brewery-info",
    components: {
      FeaturedBeer
    },
    props: {
      feature: {
        type: Object,
        default(){
          return {
            properties: {}
          }
        }
      }
    },
    data() {
      return {
        featuredBeers: []
      }
    },

    mounted(){
      console.log('breweryInfo: ', this.properties);
      this.fetchBeers();
    },

    methods: {
      async fetchBeers(id){
        const beers = await api.getBeersFromBrewery(id || this.properties.id);
        console.log('beers found: ', beers);
        this.featuredBeers.push(...beers);
      }
    },
    computed: {
      properties(){
        return this.feature.properties || this.feature || {};
      }
    },

    watch: {
      'properties.id'(newVal){
        console.log('brewery id changed: ', newVal);
        // make sure to fetch beers each time a new brewery is identified
        this.featuredBeers.length = 0;
        this.fetchBeers(newVal);
      }
    }


  }
</script>

<style scoped>

  .featured-beers-container {
    max-height: 650px;
    overflow-y: auto;
  }

</style>