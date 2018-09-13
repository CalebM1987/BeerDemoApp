<template>
  <div class="jumbotron signup-container mb-0">
    <h3 class="theme">Sign Up for Brewery Finder</h3>
    <b-card class="w-50 mx-auto p-4">
      <b-form-group label="Email:" label-text-align="left">
        <b-form-input type="email"
                      v-model.trim="email"
                      :state="validEmail"
                      aria-describedby="invalidEmail"/>
        <b-form-invalid-feedback id="invalidEmail">Invalid email address</b-form-invalid-feedback>
      </b-form-group>

      <b-form-group label="Username:" label-text-align="left">
        <b-form-input type="text" v-model.trim="username" :state="username.length >= 5" aria-describedby="tooShort"/>
        <b-form-invalid-feedback id="tooShort">Username must be at least 5 characters</b-form-invalid-feedback>
      </b-form-group>

      <b-form-group label="Password:" label-text-align="left">
        <b-form-input type="password"
                      v-model.trim="password"
                      aria-describedby="strongFeedback"
                      :state="strongPassword"/>
        <b-form-invalid-feedback id="strongFeedback">Password must be at least 8 characters long and contain letters and numbers</b-form-invalid-feedback>
      </b-form-group>

      <b-form-group label="Retype Password:" label-text-align="left">
        <b-form-input type="password"
                      v-model.trim="passwordVerify"
                      aria-describedby="retypeFeedback"
                      :state="passwordsMatch" />
        <b-form-invalid-feedback id="retypeFeedback">Passwords do not match</b-form-invalid-feedback>
      </b-form-group>

      <b-btn class="theme mt-2">Sign Up</b-btn>

    </b-card>

  </div>
</template>

<script>
  import { validationMixin } from "vuelidate"
  export default {
    name: "sign-up",
    mixins: [
      validationMixin
    ],
    mounted(){hook.su = this},
    data(){
      return {
        username: '',
        password: '',
        passwordVerify: '',
        email: '',
        weakPassword: '',
      }
    },
    methods: {
      testStrength(s=''){
        const medStrength = new RegExp("^(((?=.*[a-z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{8,})");
        return medStrength.test(s);
      },

      testEmail(s=''){
        // http://emailregex.com/
        const emailTest = new RegExp('^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$');
        return emailTest.test(s);
      }
    },
    computed: {
      passwordsMatch(){
        return (this.password || '').length >= 8 && this.password === this.passwordVerify;
      },

      validEmail(){
        return this.testEmail(this.email || '');
      },

      strongPassword(){
        return this.testStrength(this.password || '');
      }
    }
  }
</script>

<style scoped>

  .signup-container {
    height: calc(100vh - 60px);
    /*background-color: rgba(34,139,34, .75);*/
    /*color: white;*/
  }

</style>