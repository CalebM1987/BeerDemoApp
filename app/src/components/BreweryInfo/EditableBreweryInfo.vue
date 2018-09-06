<template>
  <b-card bg-variant="light">
    <open-hours :weekday="'Monday'"></open-hours>
  </b-card>
  <!--<b-container>-->
    <!--<b-form-input class="brewery-name mt-2" v-model="brewery.name" type="text" placeholder="brewery name"/>-->
    <!--<b-row>-->


    <!--</b-row>-->

    <!--<b-row class="beer-list-container">-->
      <!--<b-col></b-col>-->
    <!--</b-row>-->

  <!--</b-container>-->
</template>

<script>
  import api from '../../modules/api';
  import OpenHours from './OpenHours';

  export default {
    name: "brewery-info",
    components: {
      OpenHours
    },
    data(){
      return {
        brewery: {}
      }
    },

    mounted: async function(){
      console.log('mounted editable brewery: ', this.$route.params);
      const brewery = await this.update();
      console.log('editable brewery is: ', brewery)

    },
    methods: {
      update: async function(){
        this.brewery = await api.getBrewery(this.$route.params.id, {'f': 'json'});
        return this.brewery;
      }
    }
  }
</script>

<style scoped>
  .brewery-name {
    font-size: 1.25rem;
    font-weight: bold;
    width: 60%;
    margin: auto;
  }

</style>