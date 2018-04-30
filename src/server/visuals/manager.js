const conn = require('db-conn.js');

const allStateSQL = `
SELECT id, latitude_deg AS lat, longitude_deg AS lng
 FROM ufosightings;
`;

async function allState() {
  const res = await conn.exec(allStateSQL, []);
  return res;
}

module.exports = {
  allState,
};
