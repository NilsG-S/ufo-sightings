import React from 'react';
import PropTypes from 'prop-types';

import { withStyles } from 'material-ui/styles';

import { loadJSON } from 'utils/server.js';

const data = {
  states: [],
  counties: [],
  none: {
    mil: [],
    air: [],
    all: [],
    neither: [],
  },
  state: {
    mil: [],
    air: [],
    all: [],
    neither: [],
  },
  county: {
    mil: [],
    air: [],
    all: [],
    neither: [],
  },
};

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
  }

  componentDidMount() {
    const states = loadJSON('states.json')
      .then((res) => { data.state.mil = Object.entries(res); })
      .catch((err) => { console.log(err); });

    const all = loadJSON('all.json')
      .then((res) => { data.none.all = Object.entries(res); })
      .catch((err) => { console.log(err); });

    const airports = loadJSON('airports.json')
      .then((res) => { data.none.air = Object.entries(res); })
      .catch((err) => { console.log(err); });

    const airportsState = loadJSON('airportsState.json')
      .then((res) => { data.state.air = Object.entries(res); })
      .catch((err) => { console.log(err); });

    Promise.all([
      states,
      all,
      airports,
      airportsState,
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
    const map = new google.maps.Map(this.mapRef.current, {
      zoom: 4,
      center: { lat: 33.584466, lng: -101.874670 },
    });

    // if (this.props.geoChecked === 'none') {
    // } else {
    // }
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
