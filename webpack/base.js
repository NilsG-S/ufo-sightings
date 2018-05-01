const path = require('path');

const appPath = path.resolve(__dirname, '../src/ui');
const nodePath = path.resolve(__dirname, '../node_modules');
const buildPath = path.resolve(__dirname, '../public');

const base = {
  // Allows for absolute paths from locations indicated in `resolve.modules`
  resolve: {
    modules: [
      appPath,
      nodePath,
    ],
  },

  output: {
    path: buildPath,
    publicPath: '/',
    filename: 'bundle.js',
  },

  entry: {
    app: [
      './src/ui/index.jsx',
    ],
  },

  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: nodePath,
        loader: 'babel-loader',
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.ttf$/,
        loader: 'file-loader',
        options: {
          name: 'fonts/[name].[ext]',
        },
      },
    ],
  },
};

module.exports = base;
