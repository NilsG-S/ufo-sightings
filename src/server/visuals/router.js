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

router.get('/state/all', (req, res) => {
  manager.allState()
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

router.get('/none/military', (req, res) => {
  manager.military()
    .then((data) => {
      res.status(200).json(data);
    })
    .catch((err) => {
      res.status(400).json({ message: err.toString() }).end();
    });
});

router.get('/state/military', (req, res) => {
  manager.militaryState()
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
