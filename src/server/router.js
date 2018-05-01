const express = require('express');

// Routers.
const visuals = require('./visuals/router.js');

// App routes.
const router = express.Router();
router.use('/visuals', visuals.router);

module.exports = router;
