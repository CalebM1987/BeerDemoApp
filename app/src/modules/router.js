import Router from 'vue-router';
import Vue from 'vue';
import MapViewMglv from '../components/MapViewMglv';

Vue.use(Router);

const routes = [
  { path: '/map', name: 'Map', component: MapViewMglv}
];

export default new Router(routes);