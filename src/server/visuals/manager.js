const conn = require('db-conn.js');

const allSQL = `
SELECT id, latitude_deg AS lat, longitude_deg AS lng
 FROM ufosightings;
`;

async function all() {
  return conn.exec(allSQL, []);
}

const allStateSQL = `
SELECT A.state, COUNT(*) AS num
 FROM ufosightings U
 INNER JOIN addresses A
 ON U.latitude_deg = A.latitude_deg AND U.longitude_deg = A.longitude_deg
 GROUP BY A.state;
`;

async function allState() {
  const res = await conn.exec(allStateSQL, []);
  const out = {};

  res.forEach((row) => {
    out[row.state] = row.num;
  });

  return out;
}

const airportsSQL = `
SELECT DISTINCT U.latitude_deg AS lat, U.longitude_deg AS lng
 FROM ufosightings U
 INNER JOIN addresses A
 ON U.latitude_deg = A.latitude_deg AND U.longitude_deg = A.longitude_deg
 INNER JOIN
 (
   SELECT DISTINCT county, state
   FROM airports AP
   INNER JOIN addresses A
   ON AP.latitude_deg = A.latitude_deg AND AP.longitude_deg = A.longitude_deg
 ) AP
 ON A.state = AP.state AND A.county = AP.county;
`;

async function airports() {
  return conn.exec(airportsSQL, []);
}

const airportsStateSQL = `
SELECT A.state, COUNT(*) AS num
 FROM ufosightings U
 INNER JOIN addresses A
 ON U.latitude_deg = A.latitude_deg AND U.longitude_deg = A.longitude_deg
 INNER JOIN
 (
   SELECT DISTINCT county, state
   FROM airports AP
   INNER JOIN addresses A
   ON AP.latitude_deg = A.latitude_deg AND AP.longitude_deg = A.longitude_deg
 ) AP
 ON A.state = AP.state AND A.county = AP.county
 GROUP BY A.state;
`;

async function airportsState() {
  const res = await conn.exec(airportsStateSQL, []);
  const out = {};

  res.forEach((row) => {
    out[row.state] = row.num;
  });

  return out;
}

const militarySQL = `
SELECT DISTINCT U.latitude_deg AS lat, U.longitude_deg AS lng
 FROM ufosightings U
 INNER JOIN addresses A
 ON U.latitude_deg = A.latitude_deg AND U.longitude_deg = A.longitude_deg
 INNER JOIN
 (
   SELECT DISTINCT county, state
   FROM militarybases M
   INNER JOIN addresses A
   ON M.latitude_deg = A.latitude_deg AND M.longitude_deg = A.longitude_deg
 ) M
 ON A.state = M.state AND A.county = M.county;
`;

async function military() {
  return conn.exec(militarySQL, []);
}

const militaryStateSQL = `
SELECT A.state, COUNT(*) AS num
 FROM ufosightings U
 INNER JOIN addresses A
 ON U.latitude_deg = A.latitude_deg AND U.longitude_deg = A.longitude_deg
 INNER JOIN
 (
   SELECT DISTINCT county, state
   FROM militarybases M
   INNER JOIN addresses A
   ON M.latitude_deg = A.latitude_deg AND M.longitude_deg = A.longitude_deg
 ) M
 ON A.state = M.state AND A.county = M.county
 GROUP BY A.state;
`;

async function militaryState() {
  const res = await conn.exec(militaryStateSQL, []);
  const out = {};

  res.forEach((row) => {
    out[row.state] = row.num;
  });

  return out;
}

// TODO(NilsG-S): EXCEPT not supported by MariaDB 10.2 finish this out later
const neitherSQL = `
SELECT DISTINCT U.latitude_deg AS lat, U.longitude_deg AS lng
 FROM ufosightings U
 EXCEPT
 SELECT DISTINCT U.latitude_deg AS lat, U.longitude_deg AS lng
 FROM ufosightings U
 INNER JOIN addresses A
 ON U.latitude_deg = A.latitude_deg AND U.longitude_deg = A.longitude_deg
 INNER JOIN
 (
   SELECT DISTINCT county, state
   FROM militarybases M
   INNER JOIN addresses A
   ON M.latitude_deg = A.latitude_deg AND M.longitude_deg = A.longitude_deg
   UNION
   SELECT DISTINCT county, state
   FROM airports AP
   INNER JOIN addresses A
   ON AP.latitude_deg = A.latitude_deg AND AP.longitude_deg = A.longitude_deg
 ) C
 ON A.state = C.state AND A.county = C.county;
`;

async function neither() {
  return conn.exec(neitherSQL, []);
}

// TODO(NilsG-S): EXCEPT not supported by MariaDB 10.2 finish this out later
const neitherStateSQL = `
SELECT DISTINCT U.latitude_deg AS lat, U.longitude_deg AS lng
 FROM ufosightings U
 EXCEPT
 SELECT DISTINCT U.latitude_deg AS lat, U.longitude_deg AS lng
 FROM ufosightings U
 INNER JOIN addresses A
 ON U.latitude_deg = A.latitude_deg AND U.longitude_deg = A.longitude_deg
 INNER JOIN
 (
   SELECT DISTINCT county, state
   FROM militarybases M
   INNER JOIN addresses A
   ON M.latitude_deg = A.latitude_deg AND M.longitude_deg = A.longitude_deg
   UNION
   SELECT DISTINCT county, state
   FROM airports AP
   INNER JOIN addresses A
   ON AP.latitude_deg = A.latitude_deg AND AP.longitude_deg = A.longitude_deg
 ) C
 ON A.state = C.state AND A.county = C.county;
`;

async function neitherState() {
  const res = await conn.exec(neitherStateSQL, []);
  const out = {};

  res.forEach((row) => {
    out[row.state] = row.num;
  });

  return out;
}

module.exports = {
  all,
  allState,
  airports,
  airportsState,
  military,
  militaryState,
  neither,
  neitherState,
};
