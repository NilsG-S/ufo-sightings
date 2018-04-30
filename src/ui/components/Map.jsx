import React from 'react';
import PropTypes from 'prop-types';
import { withScriptjs, withGoogleMap, GoogleMap, Marker } from 'react-google-maps';

import { loadJSON } from 'utils/server.js';

class Map extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      all: [],
    };
  }

  componentDidMount() {
    loadJSON('all.json')
      .then((res) => {
        this.setState({
          all: res,
        });
      })
      .catch((err) => {
        console.log(err);
      });
  }

  render() {
    return (
      <GoogleMap
        defaultZoom={4}
        defaultCenter={{ lat: 33.584466, lng: -101.874670 }}
      >
        {this.state.all.map(pos => (
          <Marker key={pos.id} position={{ lat: pos.lat, lng: pos.lng }} />
        ))}
      </GoogleMap>
    );
  }
}

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
