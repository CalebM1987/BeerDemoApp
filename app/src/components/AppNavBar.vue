<template>
  <b-navbar toggleable="md" type="dark" class="app-header" fixed>
    <b-navbar-brand href="#"><strong>Brewery Finder</strong></b-navbar-brand>

    <b-navbar-nav class="ml-auto">
      <!--<div title="login" class="mr-3 login-btn"><i class="fas fa-user-circle"></i></div>-->
      <i title="sign in" class="fas fa-user-circle login-btn mr-2"></i>
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

  .login-btn{
    color: orange;
    font-size: 2.5rem;
    background-color: white;
    border-radius: 50%;
    /*border-radius: 50%;*/
    cursor: pointer;
  }

  .login-btn:hover{
    background-color: orange;
    font-weight: bold;
    border-radius: 50%;
    color: lightgray;
  }

</style>