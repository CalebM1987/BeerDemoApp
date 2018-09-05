import Router from 'vue-router';
import Vue from 'vue';
import Home from '../components/Home/Home';
import EditableBreweryInfo from '../components/EditableBreweryInfo';
import EditableBeerInfo from '../components/EditableBeerInfo';

Vue.use(Router);

const routes = [
  { path: '/home', name: 'Home', component: Home },
  { path: '/brewery/:id', name: 'EditableBreweryInfo', component: EditableBreweryInfo },
  { path: '/beers/:id', name: 'EditableBeerInfo', comp: EditableBeerInfo }
];

export default new Router(routes);