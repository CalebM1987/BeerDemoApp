<template>
  <div class="login-container">
    <b-card class="login-card">
      <b-img src="./assets/avatar_2x.png" class="avatar"></b-img>

      <div class="mt-4">
        <b-form-input v-model="username" placeholder="username"></b-form-input>
        <b-form-input type="password" v-model="password" placeholder="password" class="mt-2 mb-4"></b-form-input>

        <b-form-checkbox v-model="rememberMe" style="color: white;">Remember Me</b-form-checkbox>

        <b-btn block class="sign-in-btn mt-4 mb-4" @click="login">Sign In</b-btn>
      </div>

      <hr style="background-color: white;">
      <p class="acc">Don't have an Account? <a href="#" class="sign-up" @click="$emit('sign-up')">Sign Up</a></p>


    </b-card>
  </div>
</template>

<script>
  import api from '../modules/api';

  export default {
    name: "login-page",
    data(){
      return {
        state: null,
        username: null,
        password: null,
        rememberMe: false
      }
    },

    methods: {
      login(){
        return api.login(this.username, this.password, this.rememberMe);
      }
    }
  }
</script>

<style scoped>

  .avatar {
    border-radius: 50%;
    height: 5rem;
  }

  .login-card {
    padding: 2rem;
    background-color: rgba(34,139,34, .75);
  }

  .sign-in-btn {
    background-color: orange;
    font-weight: bold;
  }

  .sign-in-btn:hover {
    /*opacity: 0.5;*/
    background-color: darkorange;
  }

  .login-container {
    /*max-width: 350px;*/
    width: 75%;
    margin: auto;
  }

  .acc {
    color: white;
    font-size: 0.85rem;
  }

  .sign-up {
    color: orange;
    font-weight: bold;
    font-size: 0.9rem;
  }

  .sign-up:hover {
    color: darkorange;
  }

</style>