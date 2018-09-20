<template>
  <b-modal id="new_beer" title="Create New Beer" ref="modal" :hide-footer="true">
    <div class="mt-2 mb-3 mx-auto">
      <div class="xhr-spinner-container" v-if="creatingNewBeer">
        <spinner :visible="state === 'working'" :text="workingText"/>

        <b-alert :show="1" @dismissed="handleAddBeer" v-if="state === 'complete'" variant="success">{{ successText }}</b-alert>
        <b-alert :show="1" @dismissed="reset(false)" v-if="state === 'error'" variant="danger">{{ errorText }}</b-alert>

      </div>
      <b-form-group v-else
                    label="Name:"
                    horizontal
                    label-cols="3">
        <b-form-input v-model="new_beer_name"/>
      </b-form-group>
    </div>

    <div class="buttons mb-2 mt-3">
      <b-button @click="hide" variant="danger" class="bold mr-4">Cancel</b-button>
      <b-button class="theme" @click="addBeer">Create Beer</b-button>
    </div>
  </b-modal>
</template>

<script>
  import api from '../modules/api';

  export default {
    name: "new-beer-modal",
    props: ['brewery'],
    data() {
      return {
        state: 'ready',
        new_beer_name: null,
        creatingNewBeer: false,
        newBeerId: null,
        workingText: 'Creating New Beer...',
        successText: 'Successfully Created New Beer',
        errorText: 'Failed to Create New Beer, please try again'
      }
    },
    methods: {
      async addBeer(){
        console.log('clicked add beer');
        this.creatingNewBeer = true;
        this.state = 'working';
        try {
          const resp = await api.createItem('beers', {
            name: this.new_beer_name,
            brewery_id: this.brewery.id
          });
          this.newBeerId = resp.id;
          this.state = 'complete';
        } catch(err){
          console.log('error creating beer: ', err);
          this.state = 'error';
        }
      },

      handleAddBeer(){
        // navigate to new beer edit
        this.$emit('created-beer', this.newBeerId);

        // small timeout to prevent any possible race conditions (newBeerId being cleared before use)
        setTimeout(this.reset, 500);
      },

      reset(clearAtts=true){
        this.state = 'ready';
        if (clearAtts){
          this.new_beer_name = null;
          this.newBeerId = null;
        }
        this.creatingNewBeer = false;
      },

      show(){
        this.$refs.modal.show();
      },

      hide(){
        this.$refs.modal.hide();
        this.reset();
      }
    }
  }
</script>

<style scoped>

</style>