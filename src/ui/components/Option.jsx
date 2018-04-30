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
          checked={props.checked}
          name={props.name}
          onChange={props.handler}
        />
      </ListItemSecondaryAction>
    </ListItem>
  );
}

Option.propTypes = {
  checked: PropTypes.bool.isRequired,
  handler: PropTypes.func.isRequired,
  name: PropTypes.number.isRequired,
  text: PropTypes.string.isRequired,
};

export default Option;
