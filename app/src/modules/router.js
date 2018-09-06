import Router from 'vue-router';
import Vue from 'vue';
import Home from '../components/Home/Home';
import EditableBreweryInfo from '../components/BreweryInfo/EditableBreweryInfo';
import EditableBeerInfo from '../components/EditableBeerInfo';

Vue.use(Router);

const routes = [
  { path: '/home', name: 'home', component: Home },
  { path: '/brewery/:id', name: 'editableBreweryInfo', component: EditableBreweryInfo },
  { path: '/beers/:id', name: 'editableBeerInfo', component: EditableBeerInfo }
];

export default new Router({routes: routes});