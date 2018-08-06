import { request } from './xhr';

const default_request_options = {
  method: 'get',
  f: 'geojson'
}

const api = {
  host: 'localhost',
  port: '5000',
  // baseUrl: `${api.host}:${api.port}`,
  baseUrl: 'http://localhost:5000',

  getBreweries(options=default_request_options){

    // defaults
    options.method = options.method || 'get';
    options.f = options.f || 'geojson';

    // make request
    return request(`${api.baseUrl}/breweries`, options);
    
  },

  getBrewery(id, options=default_request_options){
    if (id){
      return request(`${api.baseUrl}//breweries/${id}`);
    }

  },

  getBeersFromBrewery(breweryId, options={}){
    const url = `${api.baseUrl}/breweries/${breweryId}/beers`;
    return request(url, options);
  },

  getBeers(options={}){
    return request(`${api.baseUrl}/breweries`, options);
  },

  getBeerPhotos(beerId, options={}){
    const url = `${api.baseUrl}/beers/${beerId}/photos`;
    return request(url, options);
  },

  queryBeerPhotos(photo_id, options={}){
    let url = `${api.baseUrl}/beer_photos`;
    if (photo_id){
      url += `/${photo_id}`;
    }
    return request(url, options);
  },

  getPhotoUrl(photo_id){
    return `${api.baseUrl}/beer_photos/${photo_id}/download`;
  },

  downloadPhoto(photo_id, options){
    const url = `${api.baseUrl}/beer_photos/${photo_id}`;
    return request(url, options);
  }
};

export default api;