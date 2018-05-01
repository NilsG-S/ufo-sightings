const express = require('express');

const manager = require('./manager.js');

const router = express.Router();

router.get('/none/all', (req, res) => {
  manager.all()
    .then((data) => {
      res.status(200).json(data);
    })
    .catch((err) => {
      res.status(400).json({ message: err.toString() }).end();
    });
});

router.get('/none/airports', (req, res) => {
  manager.airports()
    .then((data) => {
      res.status(200).json(data);
    })
    .catch((err) => {
      res.status(400).json({ message: err.toString() }).end();
    });
});

router.get('/state/airports', (req, res) => {
  manager.airportsState()
    .then((data) => {
      res.status(200).json(data);
    })
    .catch((err) => {
      res.status(400).json({ message: err.toString() }).end();
    });
});

module.exports = {
  router,
};
