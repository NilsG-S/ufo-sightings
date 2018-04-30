import React from 'react';
import PropTypes from 'prop-types';

import Checkbox from 'material-ui/Checkbox';
import {
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
} from 'material-ui/List';

function Option(props) {
  return (
    <ListItem>
      <ListItemText primary={props.text} />
      <ListItemSecondaryAction>
        <Checkbox
          onChange={props.handle}
          checked={props.checked}
        />
      </ListItemSecondaryAction>
    </ListItem>
  );
}

Option.propTypes = {
  checked: PropTypes.bool.isRequired,
  handle: PropTypes.func.isRequired,
  text: PropTypes.string.isRequired,
};

export default Option;
