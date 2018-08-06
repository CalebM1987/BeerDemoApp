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
      return request(`/breweries/${id}`);
    }

  }
};

export default api;