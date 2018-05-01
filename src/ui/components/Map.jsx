import React from 'react';
import PropTypes from 'prop-types';

import { withStyles } from 'material-ui/styles';

import { loadJSON } from 'utils/server.js';

const data = {
  none: {
    mil: [],
    air: [],
    all: [],
    neither: [],
  },
  state: {
    poly: [],
    mil: [],
    air: [],
    all: [],
    neither: [],
  },
  county: {
    poly: [],
    mil: [],
    air: [],
    all: [],
    neither: [],
  },
};

const colors = [
  '#F44336',
  '#E53935',
  '#D32F2F',
  '#C62828',
  '#B71C1C',
];

const styles = () => ({
  map: {
    flexGrow: 1,
  },
});

class Map extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      ready: false,
    };
    this.mapRef = React.createRef();
    this.map = null;
    this.markers = [];
  }

  componentDidMount() {
    this.map = new google.maps.Map(this.mapRef.current, {
      zoom: 4,
      center: { lat: 33.584466, lng: -101.874670 },
    });

    const states = loadJSON('states.geojson')
      .then((res) => { data.state.poly = res; })
      .catch((err) => { console.log(err); });

    const counties = loadJSON('counties.geojson')
      .then((res) => { data.county.poly = res; })
      .catch((err) => { console.log(err); });

    const all = loadJSON('all.json')
      .then((res) => { data.none.all = res; })
      .catch((err) => { console.log(err); });

    const allState = loadJSON('allState.json')
      .then((res) => { data.state.all = res; })
      .catch((err) => { console.log(err); });

    const airports = loadJSON('airports.json')
      .then((res) => { data.none.air = res; })
      .catch((err) => { console.log(err); });

    const airportsState = loadJSON('airportsState.json')
      .then((res) => { data.state.air = res; })
      .catch((err) => { console.log(err); });

    const military = loadJSON('military.json')
      .then((res) => { data.none.mil = res; })
      .catch((err) => { console.log(err); });

    const militaryState = loadJSON('militaryState.json')
      .then((res) => { data.state.mil = res; })
      .catch((err) => { console.log(err); });

    Promise.all([
      states,
      counties,
      all,
      allState,
      airports,
      airportsState,
      military,
      militaryState,
    ])
      .then(() => { this.setState({ ready: true }); });
  }

  shouldComponentUpdate(nextProps, nextState) {
    if (nextState.ready === true && this.state.ready === false) {
      return true;
    }

    if (this.props.dataChecked !== nextProps.dataChecked) {
      return true;
    }

    if (this.props.geoChecked !== nextProps.geoChecked) {
      return true;
    }

    return false;
  }

  componentDidUpdate() {
    const { dataChecked, geoChecked } = this.props;

    this.map.data.forEach((feature) => {
      this.map.data.remove(feature);
    });
    this.markers.forEach((marker) => {
      marker.setMap(null);
    });

    if (geoChecked === 'none') {
      data[geoChecked][dataChecked].forEach((pos) => {
        const marker = new google.maps.Marker({
          position: { lat: pos.lat, lng: pos.lng },
        });

        this.markers.push(marker);
        marker.setMap(this.map);
      });
    } else {
      this.map.data.addGeoJson(data[geoChecked].poly);
      this.map.data.setStyle((feature) => {
        const index = Math.floor(data[geoChecked][dataChecked][feature.f.NAME] / 553);
        const color = colors[index];

        if (color === undefined) {
          return {
            strokeWeight: 0.5,
            fillColor: '#EF5350',
            fillOpacity: 1.0,
          };
        }

        return {
          strokeWeight: 0.5,
          fillColor: color,
          fillOpacity: 1.0,
        };
      });
    }
  }

  render() {
    return (
      <div className={this.props.classes.map} ref={this.mapRef} />
    );
  }
}

Map.propTypes = {
  classes: PropTypes.object.isRequired,
  dataChecked: PropTypes.string.isRequired,
  geoChecked: PropTypes.string.isRequired,
};

export default withStyles(styles)(Map);
