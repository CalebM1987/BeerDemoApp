<template>
  <b-modal id="new_beer" :title="title" ref="modal" :hide-footer="true">
    <div class="mt-2 mb-3 mx-auto">
      <div class="xhr-spinner-container" v-if="creatingNewItem">
        <spinner :visible="state === 'working'" :text="workingText"/>

        <b-alert :show="1" @dismissed="handleAddItem" v-if="state === 'complete'" variant="success">{{ successText }}</b-alert>
        <b-alert :show="1" @dismissed="reset(false)" v-if="state === 'error'" variant="danger">{{ errorText }}</b-alert>

      </div>
      <b-form-group v-else
                    label="Name:"
                    horizontal
                    label-cols="3">
        <b-form-input v-model="new_item_name"/>
      </b-form-group>
    </div>

    <div class="buttons mb-2 mt-3" v-if="state === 'ready'">
      <b-button @click="hide" variant="danger" class="bold mr-4" @dismissed="this.state = 'ready'">Cancel</b-button>
      <b-button class="theme" @click="addItem" @dismissed="handleAddItem">{{ title }}</b-button>
    </div>
  </b-modal>
</template>

<script>
  
  export default {
    name: "new-item-modal",
    props: {
      clickHandler: {
        type: Function,
        default(){
          return function(name){
            console.log('clicked add new item button: ', name)
          }
        }
      },
      itemName: {
        type: String,
        default: 'Beer'
      }
    },
    data() {
      return {
        state: 'ready',
        new_item_name: null,
        creatingNewItem: false,
        response: null
      }
    },
    methods: {
      async addItem(){
        console.log('clicked add beer');
        this.creatingNewItem = true;
        this.state = 'working';
        try {
          this.response = await this.clickHandler(this.new_item_name);
          this.state = 'complete';
        } catch(err){
          console.log('error creating item: ', err);
          this.state = 'error';
        }
      },

      handleAddItem(){
        // navigate to new beer edit
        console.log('CALLED HANDLE ADD ITEM FROM MODAL: ', this.response);
        this.$emit('created-item', this.response);

        // small timeout to prevent any possible race conditions (newBeerId being cleared before use)
        setTimeout(this.reset, 500);
      },

      reset(clearAtts=true){
        this.state = 'ready';
        if (clearAtts){
          this.new_item_name = null;
          this.response = null;
        }
        this.creatingNewItem = false;
      },

      show(){
        this.$refs.modal.show();
      },

      hide(){
        this.$refs.modal.hide();
        this.reset();
      }
    },

    computed: {
      title(){
        return `Create New ${this.itemName}`;
      },

      workingText() {
        return `Creating New ${this.itemName}...`;
      },

      successText() {
        return `Successfully Created New ${this.itemName}`;
      },

      errorText(){
        return `Failed to Create New ${this.itemName}, please try again`;
      }
    }
  }
</script>
