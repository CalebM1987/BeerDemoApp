import Router from 'vue-router';
import Vue from 'vue';
import Home from '../components/Home/Home';
import SignUp from '../components/SignUp/SignUp';
import EditableBreweryInfo from '../components/BreweryInfo/EditableBreweryInfo';
import EditableBeerInfo from '../components/EditableBeerInfo';
import PageNotFound from '../components/PageNotFound';
import ActivationPage from '../components/ActivationPage';

Vue.use(Router);

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/sign-up', name: 'signup', component: SignUp },
  { path: '/brewery/:id', name: 'editableBreweryInfo', component: EditableBreweryInfo },
  { path: '/beers/:id', name: 'editableBeerInfo', component: EditableBeerInfo },
  { path: '/users/:id/activate', name: 'activate', component: ActivationPage },

  // catch all route
  { path: '*', component: PageNotFound }
];

export default new Router({
  mode: 'history',
  routes: routes
});