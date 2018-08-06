<template>
  <b-navbar toggleable="md" type="dark" class="app-header" fixed>
    <b-navbar-brand href="#">Brewery Finder</b-navbar-brand>

    <b-navbar-nav class="ml-auto">
      <b-btn title="save configuration changes" class="mr-3 test-btn">Add Brewery</b-btn>
    </b-navbar-nav>

  </b-navbar>
</template>

<script>
  export default {
    name: "app-nav-bar",
    data() {
      return {}
    },
    methods: {}
  }
</script>

<style scoped>

  .app-header {
    background-color: forestgreen;
  }

</style>