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
          checked={props.checked === props.name}
          name={props.name}
          onChange={props.handler}
        />
      </ListItemSecondaryAction>
    </ListItem>
  );
}

Option.propTypes = {
  checked: PropTypes.string.isRequired,
  handler: PropTypes.func.isRequired,
  name: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
};

export default Option;
