<template>
  <b-container>
    <b-row>
      <b-img v-if="photoUrl"></b-img>
      <div v-else class="drop-zone"></div>

    </b-row>

    <b-row>
      <b-col></b-col>
    </b-row>

  </b-container>
</template>

<script>
  import api from '../modules/api';

  export default {
    name: "beer-info",
    props: {
      beer: {
        type: Object,
        default(){
          return {};
        }
      },
      photoUrl: String
    },

  }
</script>

<style scoped>

</style>