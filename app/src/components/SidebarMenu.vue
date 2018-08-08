<template>
  <div class="menu-container">
    <typeahead></typeahead>
  </div>
  
</template>

<script>
  import Typeahead from './Typeahead';
  export default {
    name: "sidebar-menu",
    components: {
      Typeahead
    },
    data() {
      return {}
    },
    methods: {}
  }
</script>

<style scoped>

</style>