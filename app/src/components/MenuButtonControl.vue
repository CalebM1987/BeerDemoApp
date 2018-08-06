<template>
  <div class="mapboxgl-ctrl mapboxgl-ctrl-group" ref="container" v-if="!removed">
    <button class="mapboxgl-ctrl-icon" aria-label="Toggle Menu">☰</button>
  </div>
</template>

<script>
  export default {
    name: "menu-button-control",
    data() {
      return {
        removed: false
      }
    },
    methods: {
      onAdd(map){
        const container = document.createElement('div');
        const button = document.createElement('button');

        this._container = this.$refs.container;
        this._map = map;
        return this._container;
      },

      onRemove(){
        this._map = undefined;
        this.removed = true;
      }
    }
  }
</script>

<style scoped>

</style>