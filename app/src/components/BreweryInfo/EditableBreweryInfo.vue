<template>
  <b-card bg-variant="light" class="editable-brewery">

    <!--  SPINNER FOR LOADING -->
    <span style="font-size: 3.5rem;" class="centered" v-show="isLoading">
      <spinner :text="'loading brewery info...'" :visible="isLoading"/>
    </span>

    <!-- EDITABLE BREWERY CONTENT -->
    <b-container class="brewery-content" v-show="!isLoading">

      <b-row>
        <b-col sm="2"> <label for="brewreyName" class="float-right" style="margin-top: 0.5rem; font-size: 1.25rem;">Brewery Name:</label></b-col>
        <b-col sm="10"><b-form-input id="breweryName" class="brewery-name mt-2" v-model="brewery.name" type="text" placeholder="brewery name"/></b-col>
      </b-row>

      <!-- ADDRESS -->
      <b-row class="mt-2">
        <b-col sm="2"><label for="address" class="float-right">Address:</label></b-col>
        <b-col sm="10"><b-form-input id="address" v-model="brewery.address"/></b-col>
      </b-row>

      <!-- WEBSITE -->
      <b-row class="mt-2">
        <b-col sm="2"><label for="website" class="float-right">Website:</label></b-col>
        <b-col sm="10"><b-form-input id="website" v-model="brewery.website"/></b-col>
      </b-row>

      <!--  city, st zip -->
      <b-row class="mt-2">
        <!--<div class="row justify-content-end">-->
          <b-col sm="2"><label for="city" class="city-align float-right">City:</label></b-col>
          <b-col sm="5"><b-form-input v-model="brewery.city" class="city-align"/></b-col>
          <b-col sm="3">
            <b-form-group label="State:" label-text-align="left">
              <b-form-select :options="stateList" v-model="brewery.state"></b-form-select>
            </b-form-group>
          </b-col>

          <b-col sm="2">
            <b-form-group label="Zip Code:" label-text-align="left">
              <b-form-input v-model="brewery.zip"/>
            </b-form-group>
          </b-col>
        <!--</div>-->
      </b-row>

      <!--  WEEKDAY HOURS -->
      <b-row class="mt-2" >
        <b-col sm="6">
          <b-form-group v-for="weekday in weekday_fields"
                        horizontal
                        :label-cols="4"
                        label-class="capitalize"
                        :label="`${weekday} Hours:`"
                        :key="weekday" class="mt-2">
            <b-form-input :id="weekday" v-model="brewery[weekday]" placeholder="ex: 11am-7pm" />
          </b-form-group>
        </b-col>
        <b-col sm="6">
          <b-form-group label="Brewery Description:" label-text-align="left" class="mt-2" id="description">
            <b-form-textarea :rows="weekday_fields.length + 6" v-model="brewery.comments"></b-form-textarea>
          </b-form-group>
        </b-col>

      </b-row>

      <!--  SAVE BUTTON AND TYPE -->
      <b-row class="mt-4">
        <b-col sm="6">
          <b-form-group label="Type">
            <b-form-radio-group v-model="brewery.brew_type" :options="typeOptions">
            </b-form-radio-group>
          </b-form-group>
        </b-col>

        <b-col sm="6">
          <b-button @click="submitEdits" class="theme mt-2">Save Changes</b-button>
        </b-col>

      </b-row>


      <!--  BEER ROWS -->
      <b-row class="mt-4">
        <accordion :header="'Featured Beers'" @action-btn-clicked="addBeer">
          <template slot="action_btn">
            <i class="fas fa-plus-circle" title="add new beer"></i>
          </template>

          <b-list-group v-for="beer in beers" v-show="beers.length">
            <beer-preview :beer="beer"/>
          </b-list-group>

          <h5 v-show="!beers.length" style="color: gray;" class="mt-2">No beers found, use plus button to add new beers</h5>

        </accordion>
      </b-row>


    </b-container>


  </b-card>
</template>

<script>
  import api from '../../modules/api';
  import BeerPreview from './BeerPreview';
  import enums from '../../modules/enums';
  import Accordion from '../UI/Accordion';
  import Spinner from '../UI/Spinner';
  import { FormTextarea } from 'bootstrap-vue/es/components';
  import Vue from 'vue';
  Vue.use(FormTextarea);

  export default {
    name: "brewery-info",
    components: {
      BeerPreview,
      Accordion,
      Spinner
    },
    data(){
      return {
        brewery: {},
        isLoading: false,
        weekday_fields: ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'],
        stateList: enums.states,
        beers: [],
        typeOptions: [
          { text: 'Brewery', value: 'Brewery' },
          { text: 'Brew Pub', value: 'Brew Pub' }
        ]
      }
    },

    async mounted(){
      hook.eb = this;
      console.log('mounted editable brewery: ', this.$route.params);
      const brewery = await this.update();
      console.log('editable brewery is: ', brewery);
    },

    async beforeRouteUpdate(to, from, next){
      console.log('BEFORE ROUTE UPDATE: ', to, from, next);
      await this.update(to.params.id);
      console.log('updated brewery and calling next: ', this.brewery);
      this.next();
    },

    methods: {
      async update(id){
        this.isLoading = true;
        this.beers.length = 0;
        if (!id){
          id = this.$route.params.id;
        }
        this.brewery = await api.getBrewery(id, {'f': 'json'});
        this.beers.push(...await api.getBeersFromBrewery(id || this.brewery.id));
        this.isLoading = false;
        return this.brewery;
      },

      async addBeer(){
        console.log('clicked add beer')
      },

      goToEditBeer(id){
        this.$router.push({ name: 'editableBeerInfo', params: {id: id} })
      },

      submitEdits(){
        console.log('submitting edits: ', this.brewery);
      }
    }
  }
</script>

<style scoped>

  .city-align {
    margin-top: 2rem;
  }

  .editable-brewery {
    min-height: calc(100vh - 60px);
  }

  .brewery-name {
    font-size: 1.25rem;
    font-weight: bold;
    margin: auto;
  }

</style>