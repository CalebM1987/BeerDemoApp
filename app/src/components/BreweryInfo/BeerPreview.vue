<template>
  <b-list-group-item @click="goToBeer">
    <b-media>
      <b-img slot="aside" :src="thumbnailUrl" v-if="thumbnailUrl" height="128"/>
      <h5>{{ beer.name }}
        <span class="float-right action-btn" @click="emitDeleteBeer(beer.id)">
          <i class="fas fa-minus-circle remove-beer"
             title="remove beer">
          </i>
        </span>
        <span class="float-right action-btn" style="margin-right: 0.35rem;">
          <i class="fas fa-pen" style="color: forestgreen;" title="edit beer"></i>
        </span>
      </h5>
      <p>{{ beer.description }}</p>

    </b-media>
  </b-list-group-item>
</template>

<script>
  import api from '../../modules/api';
  export default {
    name: "beer-preview",
    mounted(){
      this.getThumbnailUrl();
      hook.bp=this;
      },
    props: {
      beer: {
        type: Object,
        default(){
          return {};
        }
      }
    },
    data(){
      return {
        thumbnailUrl: null
      }
    },
    methods: {
      goToBeer(){

      },

      async emitDeleteBeer(id){
        this.$emit('delete-beer', id);
        console.log('deleting beer with id: ', id)
      },

      async getThumbnailUrl(){
        const photos = await api.getBeerPhotos(this.beer.id);
        console.log('beer photos: ', photos);
        if (photos.length){
          console.log('setting photo url: ', api.getPhotoUrl(photos[0].id));
          this.thumbnailUrl = api.getPhotoUrl(photos[0].id, true)
        }
      }
    }
  }
</script>

<style scoped>

  .action-btn {
    cursor: pointer;
    font-size: 1.25rem;
  }

  .remove-beer {
    color: red;
  }

</style>