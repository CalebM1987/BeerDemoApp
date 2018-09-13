<template>
  <div class="jumbotron signup-container">
    <h3>Sign Up</h3>
    <b-card>
      <b-form-group label="Email:">
        <b-form-input type="email" v-model="email" />
      </b-form-group>

      <b-form-group label="Username">
        <b-form-input type="text" v-model="email" />
      </b-form-group>

      <b-form-group label="Password">
        <b-form-input type="password" v-model="password" />
      </b-form-group>

      <b-form-group label="Retype Password">
        <b-form-input type="password" v-model="passwordVerify" />
      </b-form-group>

      <b-btn>Sign Up</b-btn>

    </b-card>

  </div>
</template>

<script>
  export default {
    name: "sign-up",
    data(){
      return {
        username: null,
        password: null,
        passwordVerify: null,
        email: null,
      }
    }
  }
</script>

<style scoped>

  .signup-container {
    /*background-color: rgba(34,139,34, .75);*/
    /*color: white;*/
  }

</style>