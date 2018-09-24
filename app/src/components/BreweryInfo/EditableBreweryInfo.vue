<template>
  <b-card bg-variant="light" class="editable-brewery">

    <!--  SPINNER FOR LOADING -->
    <span style="font-size: 3.5rem;" class="centered" v-if="state === 'loading'">
      <spinner :text="'loading brewery info...'"/>
    </span>

    <!-- EDITABLE BREWERY CONTENT -->
    <b-container class="brewery-content" v-else>
      <b-row class="mt-2">
        <b-col sm="12">
          <b-form-group label="Name:"
                        horizontal
                        label-text-align="right"
                        :label-cols="2">
            <b-form-input v-model="brewery.name" class="bold" />
          </b-form-group>
        </b-col>
      </b-row>

      <!-- ADDRESS -->
      <b-row md="12">
        <b-col sm="12">
          <b-form-group label="Address:"
                        horizontal
                        label-text-align="right"
                        :label-cols="2">
            <b-form-input id="address" v-model="brewery.address"/>
          </b-form-group>
        </b-col>
      </b-row>

      <!--  city, st zip -->
      <b-row class="mt-2" align-h="end">
        <!--<div class="row justify-content-end">-->
          <b-col sm="12" md="6">
            <b-form-group label="City:" label-text-align="left">
              <!--class="city-align"-->
              <b-form-input v-model="brewery.city" />
            </b-form-group>
          </b-col>
          <b-col sm="6" md="3">
            <b-form-group label="State:" label-text-align="left">
              <b-form-select :options="stateList" v-model="brewery.state"></b-form-select>
            </b-form-group>
          </b-col>

          <b-col sm="6" md="2">
            <b-form-group label="Zip Code:" label-text-align="left">
              <b-form-input v-model="brewery.zip"/>
            </b-form-group>
          </b-col>
        <!--</div>-->
      </b-row>

      <!-- WEBSITE -->
      <b-row class="mt-2">
        <b-col sm="12">
          <b-form-group label="Website:"
                        horizontal
                        label-text-align="right"
                        :label-cols="2">
            <b-form-input id="website" v-model="brewery.website"/>
          </b-form-group>
        </b-col>
      </b-row>

      <!--  WEEKDAY HOURS -->
      <b-row class="mt-2" >
        <b-col sm="12" md="6">
          <b-form-group v-for="weekday in weekday_fields"
                        horizontal
                        :label-cols="5"
                        label-class="capitalize"
                        :label="`${weekday} Hours:`"
                        :key="weekday" class="mt-2">
            <b-form-input :id="weekday" v-model="brewery[weekday]" placeholder="ex: 11am-7pm" />
          </b-form-group>
        </b-col>
        <b-col sm="12" md="6">
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
          <div class="save-container">
            <b-button @click="saveChanges" class="theme mt-2" v-if="state === 'loaded'">Save Changes</b-button>
            <div v-else>
              <spinner text="Saving Changes..." :visible="state === 'saving'"/>

              <b-alert :show="1" @dismissed="state = 'loaded'"
                       v-if="state === 'saved'"
                       variant="success">
                Successfully Updated Brewery.
              </b-alert>

              <b-alert :show="1" @dismissed="state = 'loaded'"
                       v-if="state === 'error'"
                       variant="danger">
                Failed to Update Brewery, please try again.
              </b-alert>
            </div>
          </div>
        </b-col>
      </b-row>


      <!--  BEER ROWS -->
      <b-row class="mt-4">
        <accordion :header="'Featured Beers'" @action-btn-clicked="openNewBeerModal">
          <template slot="action_btn">
            <i class="fas fa-plus-circle" title="add new beer"></i>
          </template>

          <b-list-group v-for="beer in beers" v-show="beers.length" :key="beer.id">
            <beer-preview :beer="beer" @delete-beer="deleteBeer"/>
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
  import { EventBus } from "../../modules/EventBus";
  import swal from 'sweetalert2';

  export default {
    name: "brewery-info",
    components: {
      BeerPreview,
      Accordion,
      NewBeerModal
    },
    data(){
      return {
        state: 'loading',
        brewery: {},
        copy: {},
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
            this.saveChanges();
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
        this.state = 'loading';
        this.beers.length = 0;
        if (!id){
          id = this.$route.params.brewery_id;
        }
        this.brewery = await api.getBrewery(id, {'f': 'json'});
        this.copy = Object.assign({}, this.brewery);
        this.updateBeers();
        this.state = 'loaded';
        return this.brewery;
      },

      async updateBeers(){
        this.beers.length = 0;
        this.beers.push(...await api.getBeersFromBrewery(this.brewery.id));
      },

      openNewBeerModal(){
        this.$refs.newBeerModal.show();
      },
      goToEditBeer(id){
        console.log('navigating to new beer: ', id);
        this.emitBeerChange(id, 'create');
        this.$refs.newBeerModal.hide();
        setTimeout(()=>{
          this.$router.push({ name: 'editableBeerInfo', params: { beer_id: id } });
        }, 250);
      },

      async deleteBeer(id){
        const resp = await api.deleteItem('beers', id);
        console.log('delete beer resp:', resp);
        this.emitBeerChange(id, 'delete');
        this.updateBeers();

      },

      async saveChanges(){
        console.log('submitting edits: ', this.brewery);
        this.state = 'saving';
        try {
          const resp = await api.updateItem('breweries', this.brewery);

          // make sure to update copy so router guard isn't thrown
          this.copy = Object.assign({}, this.brewery);

          // emit change
          this.emitBreweryChange('update');
          this.state = 'saved';
        } catch(err){
          console.log('err: ', err);
          this.state = 'error';
        }

      },

      emitBreweryChange(type){
        EventBus.$emit('brewery-changed', {
          id: this.brewery.id,
          type: type
        });
      },

      emitBeerChange(id, type){
        EventBus.$emit('beers-changed', {
          brewery_id: this.beer.brewery_id,
          beer_id: id,
          type: type
        });
      },
    }
  }
</script>

<style>

  .editable-brewery {
    min-height: calc(100vh - 60px);
  }

</style>