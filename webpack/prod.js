const webpack = require('webpack');
const webpackMerge = require('webpack-merge');

const base = require('./base.js');

const prod = webpackMerge(base, {
  mode: 'production',

  plugins: [
    new webpack.DefinePlugin({
      ENV: JSON.stringify('prod'),
    }),
  ],
});

module.exports = prod;
