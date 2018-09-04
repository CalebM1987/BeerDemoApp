import { request, axios } from './xhr';


const default_request_options = {
  method: 'get',
  f: 'geojson'
};

// request wrapper to pass in token
function _request(url, options={}){
  // api.token ? options.token = api.token: null;
  console.log('OPTIONS IS: ', options);
  return request(url, options);
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
      return _request(`/breweries/${id}`);
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
    return `/beer_photos/${photo_id}/download`;
  },

  downloadPhoto(photo_id, options){
    return request(`/beer_photos/${photo_id}`, options);
  },

  login: async function(usr, pw, remember_me=false){
    const resp = await request('/users/login', {
      method: 'post',
      username: usr,
      password: pw,
      remember: remember_me
    });
    api.token = resp.token;
    axios.defaults.headers.common.Authorization = resp.token;
    console.log('LOGIN RESPONSE: ', resp);
    return resp;
  },

  logout: async function(){
    const response = await _request('/users/logout', {method: 'post'}, false);
    console.log('FULL LOGOUT RESPONSE: ', response);
    return response.data;
  },

  authTest(){
    return _request('/users/welcome');
  }
};

export default api;