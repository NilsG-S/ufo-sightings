const fs = require('fs');

function ccw(p) {
  let a = 0;
  for (let i = 0; i < p.length - 2; i += 1) {
  	a += ((p[i+1].lat - p[i].lat) * (p[i+2].lng - p[i].lng) - (p[i+2].lat - p[i].lat) * (p[i+1].lng - path[i].lng));
  }
  if (a > 0) {
    return true;
  }
  return false;
}

function multipolygon(coords) {
  const obj = [];
  coords.forEach((i) => {
    const paths = [];
    let exterior;
    let interior;
    i.forEach((j) => {
      const path = [];
      j.forEach((k) => {
        path.push({
          lng: k[0],
          lat: k[1],
        });
      });
      if (!j) {
        exterior = ccw(path);
        paths.push(path);
      } else if (j === 1) {
        interior = ccw(path);
        if (exterior === interior) {
          paths.push(path.reverse());
        } else {
          paths.push(path);
        }
      } else if (exterior === interior) {
        paths.push(path.reverse());
      } else {
        paths.push(path);
      }
    });
    obj.push(paths);
  });
  return obj;
}

const countiesIn = JSON.parse(fs.readFileSync('./counties.geojson', 'utf8'));
const statesIn = JSON.parse(fs.readFileSync('./states.geojson', 'utf8'));
const countiesOut = {};
const statesOut = {};

statesIn.features.forEach((feature) => {
  statesOut[feature.properties.NAME] = multipolygon(feature.geometry.coordinates);
});
fs.writeFileSync('./simple-states.json', JSON.stringify(statesOut), 'utf8');
