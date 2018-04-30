import React from 'react';
import PropTypes from 'prop-types';

import { withStyles } from 'material-ui/styles';

import Option from './Option.jsx';
import Options from './Options.jsx';

const styles = theme => ({
  toolbar: theme.mixins.toolbar,
});

function DrawerOptions(props) {
  const { classes } = props;

  return (
    <div>
      <div className={classes.toolbar} />
      <Options>
        {props.geo.map(opt => (
          <Option
            key={opt.key}
            checked={opt.checked}
            handler={props.geoHandler}
            name={opt.key}
            text={opt.text}
          />
        ))}
      </Options>
      <Options>
        {props.data.map(opt => (
          <Option
            key={opt.key}
            checked={opt.checked}
            handler={props.dataHandler}
            name={opt.key}
            text={opt.text}
          />
        ))}
      </Options>
    </div>
  );
}

DrawerOptions.propTypes = {
  classes: PropTypes.object.isRequired,
  data: PropTypes.arrayOf(PropTypes.shape({
    key: PropTypes.number.isRequired,
    checked: PropTypes.bool.isRequired,
    text: PropTypes.string.isRequired,
  })).isRequired,
  dataHandler: PropTypes.func.isRequired,
  geo: PropTypes.arrayOf(PropTypes.shape({
    key: PropTypes.number.isRequired,
    checked: PropTypes.bool.isRequired,
    text: PropTypes.string.isRequired,
  })).isRequired,
  geoHandler: PropTypes.func.isRequired,
};

export default withStyles(styles)(DrawerOptions);
