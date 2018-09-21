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
        <accordion :header="'Featured Beers'" @action-btn-clicked="openNewBeerModal">
          <template slot="action_btn">
            <i class="fas fa-plus-circle" title="add new beer"></i>
          </template>

          <b-list-group v-for="beer in beers" v-show="beers.length" :key="beer.id">
            <beer-preview :beer="beer"/>
          </b-list-group>

          <h5 v-show="!beers.length" style="color: gray;" class="mt-2">No beers found, use plus button to add new beers</h5>

        </accordion>
      </b-row>


    </b-container>

    <!-- PLACEHOLDER FOR NEW BEER MODAL -->
    <new-beer-modal :brewery="brewery" @created-beer="goToEditBeer" ref="newBeerModal"/>


  </b-card>
</template>

<script>
  import api from '../../modules/api';
  import BeerPreview from './BeerPreview';
  import enums from '../../modules/enums';
  import Accordion from '../UI/Accordion';
  import NewBeerModal from '../NewBeerModal';
  import { FormTextarea } from 'bootstrap-vue/es/components';
  import Vue from 'vue';
  import swal from 'sweetalert2';
  Vue.use(FormTextarea);

  export default {
    name: "brewery-info",
    components: {
      BeerPreview,
      Accordion,
      NewBeerModal
    },
    data(){
      return {
        brewery: {},
        copy: {},
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
      // const brewery = await this.update();
      // console.log('editable brewery is: ', brewery);
    },

    // we want to make sure to intercept this to force the router to update
    // the current brewery
    beforeRouteEnter(to, from, next){
      next(async (vm)=>{
        // vm is reference to this component!
        await vm.update(to.params.brewery_id);
        console.log('updated brewery and calling next: ', vm.brewery);
        next();
      })

    },

    beforeRouteLeave (to, from, next) {
      // called when the route that renders this component is about to
      // be navigated away from.
      // has access to `this` component instance.
      // make sure there haven't been any changes before leaving route
      if (JSON.stringify(this.brewery) != JSON.stringify(this.copy)){
        swal({
          type: 'warning',
          title: 'You have unsaved Edits',
          text: 'You are about to leave this page but have unsaved edits. Do you want to save your changes before proceeding?',
          showCancelButton: true,
          confirmButtonColor: 'forestgreen',
          cancelButtonColor: '#d33',
          cancelButtonText: "Don't Save Changes",
          confirmButtonText: 'Save Changes'
        }).then((choice)=>{
          if (choice){
            // save here before proceeding
            console.log('SAVE HERE!');
          }

          // now proceed
          next();
        })
      } else {
        next();
      }
    },

    methods: {
      async update(id){
        this.isLoading = true;
        this.beers.length = 0;
        if (!id){
          id = this.$route.params.brewery_id;
        }
        this.brewery = await api.getBrewery(id, {'f': 'json'});
        this.copy = Object.assign({}, this.brewery);
        this.beers.push(...await api.getBeersFromBrewery(id || this.brewery.id));
        this.isLoading = false;
        return this.brewery;
      },
      openNewBeerModal(){
        this.$refs.newBeerModal.show();
      },
      goToEditBeer(id){
        console.log('navigating to new beer: ', id);
        this.$refs.newBeerModal.hide();
        setTimeout(()=>{
          this.$router.push({ name: 'editableBeerInfo', params: {id: id} });
        }, 250);
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