const webpack = require('webpack');
module.exports = {
  configureWebpack: {
    plugins: [
      new webpack.ProvidePlugin({
        // mapboxgl: 'mapbox-gl-vue'
        mapboxgl: 'mapbox-gl'
      })
    ]
  }
};