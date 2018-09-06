<template>
  <div class="hours-container">

    <span class="in-line">
      <span class="weekday-label float-left">{{ weekday }}</span>
      <b-form-group class="w-45" horizontal label="open:">
        <b-form-input placeholder="ex: 12pm" v-model="open"></b-form-input>
      </b-form-group>

    <b-form-group class="w-45" horizontal label="close:">
      <b-form-input placeholder="ex: 10pm" v-model="close"></b-form-input>
    </b-form-group>
    </span>
  </div>
  
</template>

<script>
  export default {
    name: "open-hours",
    props: ['weekday'],
    mounted(){hook.oh = this;},
    data(){
      return {
        open: null,
        close: null
      }
    }

  }
</script>

<style>

  .weekday-label {
    font-size: 1.15rem;
    margin-top: 0.4rem;
    font-weight: bold;
  }

  .w-45 {
    width: 45% !important;
  }

  .in-line {
    display: flex;
    justify-content: space-between;
  }

</style>