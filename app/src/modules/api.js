import { request } from './xhr';
import axios from 'axios';


const default_request_options = {
  method: 'get',
  f: 'geojson'
};

const default_activation_url = window.location.href.replace('/sign-up', '/users/{id}/activate');

// request wrapper to pass in token
function _request(url, options={}, dataOnly=true){
  // api.token ? options.token = api.token: null;
  console.log('OPTIONS IS: ', options);
  return request(url, options, dataOnly);
}

const api = {
  token: null,

  getBreweries(options=default_request_options){

    // defaults
    options.method = options.method || 'get';
    options.f = options.f || 'geojson';

    // make request
    return request('/breweries', options);
  },

  getBrewery(id, options=default_request_options){
    if (id){
      return _request(`/breweries/${id}`, options);
    }

  },

  getBeersFromBrewery(breweryId, options={}){
    return request(`/breweries/${breweryId}/beers`, options);
  },

  getBeers(options={}){
    return request('/beers', options);
  },

  getBeerPhotos(beerId, options={}){
    return request(`/beers/${beerId}/photos`, options);
  },

  queryBeerPhotos(photo_id, options={}){
    let url = '/beer_photos';
    if (photo_id){
      url += `/${photo_id}`;
    }
    return request(url, options);
  },

  getPhotoUrl(photo_id){
    return `${axios.defaults.baseURL}/beer_photos/${photo_id}/download`;
  },


  downloadPhoto(photo_id, options){
    return request(`/beer_photos/${photo_id}`, options);
  },

  async login(usr, pw, remember_me=false){
    const resp = await request('/users/login', {
      method: 'post',
      username: usr,
      password: btoa(pw),
      remember: remember_me
    });
    api.token = resp.token;
    axios.defaults.headers.common.Authorization = resp.token;
    console.log('LOGIN RESPONSE: ', resp);
    return resp;
  },

  async logout(){
    const response = await _request('/users/logout', {method: 'post'}, false);
    console.log('FULL LOGOUT RESPONSE: ', response);
    return response.data;
  },

  async fetchUsernames(){
    const resp = await request('/users?fields=username');
    return resp.map(u => u.username);
  },

  createUser({name, email, username, password, activation_url=default_activation_url } = {}){
    return request('/users/create', {
      method: 'post',
      data: {
        name: name,
        email: email,
        username: username,
        password: btoa(password),
        activation_url: activation_url
      }
    });

  },

  activate(id){
    return request(`/users/${id}/activate`, { method: 'post' });
  },

  authTest(){
    return _request('/users/welcome');
  },

  async exportData({table='breweries', format='csv'}={}){
    try {
      const resp = await _request(`/data/${table}/export?f=${format}`, {
        method: 'post'
      });
      // const blob = format === 'csv' ? new Blob(['\ufeff', resp.data]): new Blob([resp], { type: 'octet/stream' });
      // console.log('RESP: ', resp);
      // return { data: URL.createObjectURL(blob), filename: 'breweries.csv' };//axios.defaults.baseURL + resp.url;
      const parts = resp.url.split('/');
      return { url: resp.url, filename: parts[parts.length-1] };
    } catch(err){
      console.warn('export data failed: ', err);
    }

  },

  async maboxReverseGeocode(lat, lng, access_token){
    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${lng}%2C${lat}.json?access_token=${access_token}`;
    const resp = await request(url);
    if ((resp.features || []).length){
      const parts = resp.features[0].place_name.split(',');
      const stZip = parts[2].split(' ').filter(s => s.length);
      return {
        address: parts[0],
        city: parts[1].trim(),
        state: stZip[0],
        zip: stZip[1]
      }
    }
    return {
      address: null,
      city: null,
      state: null,
      zip: null
    }
  }
};

export default api;