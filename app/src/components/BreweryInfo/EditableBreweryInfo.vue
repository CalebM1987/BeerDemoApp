<template>
  <b-card bg-variant="light" class="editable-brewery">

    <!--  SPINNER FOR LOADING -->
    <span style="font-size: 3.5rem;" class="centered" v-show="isLoading">
      <h5>loading brewery info...</h5>
      <i class="fas fa-spinner fa-spin"></i>
    </span>

    <!-- EDITABLE BREWERY CONTENT -->
    <b-container class="brewery-content" v-show="!isLoading">
      <b-row>
        <b-col sm="3"> <label for="brewreyName" class="float-left" style="margin-top: 0.5rem; font-size: 1.25rem;">Brewery Name:</label></b-col>
        <b-col sm="9"><b-form-input id="breweryName" class="brewery-name mt-2" v-model="brewery.name" type="text" placeholder="brewery name"/></b-col>
      </b-row>

      <open-hours :weekday="'Monday'"></open-hours>
    </b-container>

  </b-card>
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
        brewery: {},
        isLoading: false,
        typeOptions: [
          { text: 'Brewery', value: 'Brewery' },
          { text: 'Brew Pub', value: 'Brew Pub' }
        ]
      }
    },

    mounted: async function(){
      hook.eb = this;
      console.log('mounted editable brewery: ', this.$route.params);
      const brewery = await this.update();
      console.log('editable brewery is: ', brewery)

    },

    beforeRouteUpdate: async function(to, from, next){
      console.log('BEFORE ROUTE UPDATE: ', to, from, next);
      await this.update(to.params.id);
      console.log('updated brewery and calling next: ', this.brewery);
      this.next();
    },

    methods: {
      update: async function(id){
        this.isLoading = true;
        if (!id){
          id = this.$route.params.id;
        }
        this.brewery = await api.getBrewery(id, {'f': 'json'});
        this.isLoading = false;
        return this.brewery;
      }
    }
  }
</script>

<style scoped>

  .centered {
    color: gray;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  .editable-brewery {
    height: calc(100vh - 80px);
  }

  .brewery-name {
    font-size: 1.25rem;
    font-weight: bold;
    margin: auto;
  }

</style>