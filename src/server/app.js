const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');

const router = require('./router.js');

// Declarations/Definitions
const port = 3000;
const app = express();
const format = ':method :url :status :response-time ms - :res[content-length]';

// Express configuration.
app.set('port', port);
app.use(morgan(format, {
  skip() { return process.env.NODE_ENV === 'testing'; },
}));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Routes.
app.use(router);

// 404.
app.use((req, res, next) => {
  const err = new Error('Route not found.');

  err.status = 404;
  next(err);
});

app.use((err, req, res) => {
  res.status(err.status || 500);
  res.json(err.message);
});

module.exports = app;
