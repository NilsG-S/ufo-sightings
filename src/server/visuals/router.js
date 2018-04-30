const express = require('express');

const manager = require('./manager.js');

const router = express.Router();

router.get('/state/all', (req, res) => {
  manager.allState()
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
