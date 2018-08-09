<template>
  <div class="Typeahead">
    <i class="fa fa-spinner fa-spin" v-if="loading"></i>
    <template v-else>
      <i class="fa fa-search" v-show="isEmpty"></i>
      <i class="fa fa-times" v-show="isDirty" @click="reset"></i>
    </template>

    <b-form-input type="text"
           class="typeahead-input"
           placeholder="Search for brewery"
           autocomplete="off"
           v-model="query"
           @keydown.down="down"
           @keydown.up="up"
           @keydown.enter="hit"
           @keydown.esc="reset"
           @blur="reset"
           @input="update"/>

    <b-list-group v-show="hasItems" class="mt-1">
      <b-list-group-item v-for="(item, $item) in items"
        :class="activeClass($item)"
        @mousedown="hit"
        @mousemove="setActive($item)">
          <p class="brewery-name hit-result mb-2">{{ item.name }}</p>
          <p class="hit-result mb-1">{{ item.city }}</p>
      </b-list-group-item>

    </b-list-group>
    <!--<ul v-show="hasItems">-->
      <!--<li v-for="(item, $item) in items" :class="activeClass($item)" @mousedown="hit" @mousemove="setActive($item)">-->
        <!--<span class="name" v-text="item.name"></span>-->
        <!--<span class="screen-name" v-text="item.screen_name"></span>-->
      <!--</li>-->
    <!--</ul>-->
  </div>
</template>

<script>
  import { EventBus } from "../modules/EventBus";
  import VueTypeahead from 'vue-typeahead';

  export default {
    mixins: [VueTypeahead],
    data () {
      return {
        src: 'http://localhost:5000/breweries',
        data: {
          wildcards: 'name'

        },
        queryParamName: 'name',
        limit: 5,
        minChars: 2
      }
    },

    methods: {
      onHit (item) {
        //window.location.href = 'http://twitter.com/' + item.screen_name
        console.log('onHit: ', item);
        EventBus.$emit('brewery-search-result', {
          type: 'Feature',
          properties: item,
          geometry: {
            coordinates: [
              item.x,
              item.y]
          }
        });
      }
    }
  }
</script>

<style scoped>
  .Typeahead {
    position: relative;
  }

  .typeahead-input {
    width: 90%;
    font-size: 14px;
    text-align: center;
    /*color: #2c3e50;*/
    color: black !important;
    line-height: 1.42857143;
    box-shadow: inset 0 1px 4px rgba(0,0,0,.4);
    -webkit-transition: border-color ease-in-out .15s,-webkit-box-shadow ease-in-out .15s;
    transition: border-color ease-in-out .15s,box-shadow ease-in-out .15s;
    font-weight: 300;
    padding: 12px 26px;
    border: none;
    border-radius: 22px;
    letter-spacing: 1px;
    box-sizing: border-box;
  }

  .hit-result {
    color: black;
  }

  .brewery-name {
    font-weight: bold;
  }
  .typeahead-input:focus {
    border-color: #4fc08d;
    outline: 0;
    box-shadow: inset 0 1px 1px rgba(0,0,0,.075),0 0 8px #4fc08d;
  }

  .fa-times {
    cursor: pointer;
  }


  i {
    float: right;
    position: relative;
    top: 30px;
    right: 29px;
    opacity: 0.4;
  }

  /*ul {*/
    /*position: absolute;*/
    /*padding: 0;*/
    /*margin-top: 8px;*/
    /*min-width: 100%;*/
    /*background-color: #fff;*/
    /*list-style: none;*/
    /*border-radius: 4px;*/
    /*box-shadow: 0 0 10px rgba(0,0,0, 0.25);*/
    /*z-index: 1000;*/
  /*}*/
  
  /*li {*/
    /*padding: 10px 16px;*/
    /*border-bottom: 1px solid #ccc;*/
    /*cursor: pointer;*/
  /*}*/
  
  /*li:first-child {*/
    /*border-top-left-radius: 4px;*/
    /*border-top-right-radius: 4px;*/
  /*}*/
  
  /*li:last-child {*/
    /*border-bottom-left-radius: 4px;*/
    /*border-bottom-right-radius: 4px;*/
    /*border-bottom: 0;*/
  /*}*/

  /*span {*/
    /*display: block;*/
    /*color: #2c3e50;*/
  /*}*/

  .active {
    background-color: #3aa373 !important;
  }

  .active > p {
    color: white;
  }

  .name {
    font-weight: 700;
    font-size: 18px;
  }

  .screen-name {
    font-style: italic;
  }
</style>