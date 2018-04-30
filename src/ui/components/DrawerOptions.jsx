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
        {Object.values(props.geo).map(opt => (
          <Option
            key={opt.name}
            checked={props.geoChecked}
            handler={props.geoHandler}
            name={opt.name}
            text={opt.text}
          />
        ))}
      </Options>
      <Options>
        {Object.values(props.data).map(opt => (
          <Option
            key={opt.name}
            checked={props.dataChecked}
            handler={props.dataHandler}
            name={opt.name}
            text={opt.text}
          />
        ))}
      </Options>
    </div>
  );
}

DrawerOptions.propTypes = {
  classes: PropTypes.object.isRequired,
  data: PropTypes.object.isRequired,
  dataChecked: PropTypes.string.isRequired,
  dataHandler: PropTypes.func.isRequired,
  geo: PropTypes.object.isRequired,
  geoChecked: PropTypes.string.isRequired,
  geoHandler: PropTypes.func.isRequired,
};

export default withStyles(styles)(DrawerOptions);
