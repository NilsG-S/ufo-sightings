const path = require('path');

require('app-module-path').addPath(__dirname);
require('dotenv').load({ path: path.resolve(__dirname, '../../.env') });

const app = require('./app.js');

const port = 3000;

app.listen(port, () => {
  console.log(`App running at ${port} in ${app.get('env')} mode\n  Press ctrl-c to stop\n`);
});
