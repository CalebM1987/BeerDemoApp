<template>
  <b-card bg-variant="light" class="editable-beer" body-class="card-block">

    <!--  SPINNER FOR LOADING -->
    <span style="font-size: 3.5rem;" class="centered" v-show="isLoading">
      <spinner :text="'loading brewery info...'" :visible="isLoading"/>
    </span>

    <!-- EDITABLE BREWERY CONTENT -->
    <b-container class="mx-auto">
      <b-row class="mt-3">
        <b-col>
          <div class="img-container" v-if="photoUrl !== null && 0">
            <b-img :src="photoUrl" height="200" />
            <!--<font-awesome-icon prefix="fas"-->
                               <!--icon="minus-circle"-->
                               <!--title="remove/replace photo"-->
                               <!--class="mt-0 ml-3 mr-0 remove" />-->
            <div class="mt-3">
              <b-button class="theme">Update Photo</b-button>
            </div>

          </div>

          <div v-else class="file-uploader mx-auto w-50">
            <drop-zone />

          </div>
        </b-col>

      </b-row>

      <b-row class="mt-4">
        <b-col cols="12">
          <b-form-group label="Name:"
                        horizontal
                        label-text-align="right"
                        :label-cols="2">
            <b-form-input v-model="beer.name" style="font-weight: bold;" />
          </b-form-group>
        </b-col>

      </b-row>

      <b-row class="mt-2" align-h="end">
        <b-col :cols="prop.cols" v-for="prop in beer_props">
          <b-form-group :label="prop.label + ':'" label-text-align="left">
            <b-form-input :type="prop.type" v-model="beer[prop.field]" />
          </b-form-group>
        </b-col>
      </b-row>

      <b-row class="mt-2">
        <b-col cols="12">
          <b-form-group label="Style:"
                        horizontal
                        label-text-align="right"
                        :label-cols="2">
            <b-form-select :options="beerStyles" v-model="beer.style" />

          </b-form-group>
        </b-col>
      </b-row>

      <b-row class="mt-2">
        <b-col cols="12">
          <b-form-group label="Description:"
                        horizontal
                        label-text-align="right"
                        :label-cols="2">
            <b-form-textarea v-model="beer.description" :rows="6" />
          </b-form-group>
        </b-col>

      </b-row>

      <b-row class="mt-4 mb-4">
        <b-col>
          <b-button class="theme">Save Changes</b-button>
        </b-col>
      </b-row>

    </b-container>

  </b-card>
</template>

<script>
  import api from '../modules/api';
  import DropZone from './UI/DropZone';

  export default {
    name: "beer-info",
    components: {
      DropZone
    },
    data(){
      return {
        isLoading: false,
        beer: {},
        photoInfos: [],
        photoUrl: null,
        beerStyles: [],
        beer_props: [
          { label: 'IBU', field: 'ibu', type: 'number', cols: 2 },
          { label: 'Alcohol %', field: 'alc', type: 'number', cols: 2 },
          { label: 'Color', field: 'color', type: 'text', cols: 6 }
        ]
      }
    },

    async mounted(){
      hook.eb = this;
      console.log('mounted editable brewery: ', this.$route.params);
      const brewery = await this.update();
      console.log('editable brewery is: ', brewery);

      const styles = await api.getStyles();
      this.beerStyles.length = 0;
      this.beerStyles.push(...styles);

    },

    async beforeRouteUpdate(to, from, next){
      console.log('BEFORE BEER ROUTE UPDATE: ', to, from, next);
      await this.update(to.params.id);
      console.log('updated Beer and calling next: ', this.beer);
      this.next();
    },

    methods: {
      async update(id){
        this.isLoading = true;
        if (!id){
          id = this.$route.params.id;
        }
        this.beer = await api.getBeer(id);
        this.photoInfos.length = 0;
        const photoInfos = await api.getBeerPhotos(this.beer.id);
        console.log('photoInfos: ', photoInfos);
        this.photoInfos.push(...photoInfos);
        if (this.photoInfos.length){
          this.photoUrl = api.getPhotoUrl(this.photoInfos[0].id);
        }
        console.log('loaded beer: ', this.beer);
        this.isLoading = false;
        return this.beer;
      },
    }

  }
</script>

<style scoped>

  .remove {
    color: red;
    font-size: 1.25rem;
    cursor: pointer;
  }

</style>