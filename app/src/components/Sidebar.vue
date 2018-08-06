<template>
  <div id="sidebar" :class="{'active': active}">
    <slot></slot>
  </div>
</template>

<script>
  import { EventBus } from "../modules/EventBus";

  export default {
    name: "sidebar",
    data() {
      return {
        active: false
      }
    },
    mounted(){
      EventBus.$on('toggle-menu', (toggleOn)=>{
        if (toggleOn === undefined){
          this.active = !this.active;
        } else {
          this.active = toggleOn;
        }

      });
    },
    methods: {},
    watch: {
      active(newVal){
        EventBus.$emit('sidebar-expanded', newVal);
      }
    }
  }
</script>

<style scoped>
  #sidebar{
    display: none;
    width: 350px;
    background: whitesmoke;
    height: calc(100vh - 60px);
    overflow-y: scroll;
  }

  #sidebar.active {
    display: block;
  }
  #sidebar a {
    display: block;
    padding: 10px 5px;
    color: #666;
    border-bottom: 1px solid #bbb;
  }
</style>