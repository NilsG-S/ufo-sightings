import React from 'react';
import PropTypes from 'prop-types';
import { withScriptjs, withGoogleMap, GoogleMap, Marker } from 'react-google-maps';

function Map(props) {
  return (
    <GoogleMap
      defaultZoom={8}
      defaultCenter={{ lat: -34.397, lng: 150.644 }}
    >
      <Marker position={{ lat: -34.397, lng: 150.644 }} />
    </GoogleMap>
  );
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
