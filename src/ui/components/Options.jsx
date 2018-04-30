import React from 'react';
import PropTypes from 'prop-types';

import Divider from 'material-ui/Divider';
import List from 'material-ui/List';

function Options(props) {
  return (
    <div>
      <Divider />
      <List>
        {props.children}
      </List>
    </div>
  );
}

Options.propTypes = {
  children: PropTypes.element.isRequired,
};

export default Options;
