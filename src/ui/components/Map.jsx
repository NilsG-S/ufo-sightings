import React from 'react';
import PropTypes from 'prop-types';
import { withScriptjs, withGoogleMap, GoogleMap, Marker } from 'react-google-maps';

import { loadJSON } from 'utils/server.js';

const data = {
  all: [],
};

class Map extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      ready: false,
    };
  }

  componentDidMount() {
    const all = loadJSON('all.json')
      .then((res) => {
        data.all = res;
      })
      .catch((err) => {
        console.log(err);
      });

    Promise.all([
      all,
    ])
      .then(() => {
        this.setState({
          ready: true,
        });
      });
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

  render() {
    return (
      <GoogleMap
        defaultZoom={4}
        defaultCenter={{ lat: 33.584466, lng: -101.874670 }}
      >
        {data.all.map(pos => (
          <Marker key={pos.id} position={{ lat: pos.lat, lng: pos.lng }} />
        ))}
      </GoogleMap>
    );
  }
}

Map.propTypes = {
  dataChecked: PropTypes.number.isRequired,
  geoChecked: PropTypes.number.isRequired,
};

function inject(Wrapped) {
  return props => (
    <Wrapped
      googleMapURL='https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places'
      loadingElement={<div style={{ height: '100%' }} />}
      containerElement={<div style={{ flexGrow: 1 }} />}
      mapElement={<div style={{ height: '100%' }} />}
      {...props}
    />
  );
}

export default inject(withScriptjs(withGoogleMap(Map)));
