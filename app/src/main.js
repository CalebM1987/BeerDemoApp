import Vue from 'vue'
import App from './App.vue'
import { request } from "./modules/xhr";
import VueMapbox from 'vue-mapbox';
import Mapbox from 'mapbox-gl';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import '@fortawesome/fontawesome-free/js/all';

Vue.use(BootstrapVue);
Vue.use(VueMapbox, { mapboxgl: Mapbox });


Vue.config.productionTip = false;

// wait for config to load before initializing Vue instance
request('./config.json').then((config) => {
  console.log(config)

  new Vue({
    render: h => h(App),

    // data must be a function that returns an object
    data(){
      return {
        config: config
      }
    }
  }).$mount('#app');
});
