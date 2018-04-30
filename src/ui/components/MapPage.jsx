import React from 'react';
import PropTypes from 'prop-types';

import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Drawer from 'material-ui/Drawer';
import IconButton from 'material-ui/IconButton';
import Hidden from 'material-ui/Hidden';
import MenuIcon from '@material-ui/icons/Menu';
import ToolBar from 'material-ui/ToolBar';
import Typography from 'material-ui/Typography';

import values from 'utils/values.js';
import DrawerOptions from './DrawerOptions.jsx';
import Map from './Map.jsx';

const styles = theme => ({
  root: {
    margin: 0,
    padding: 0,
    width: '100%',
    height: '100%',
  },
  appbar: {
    position: 'fixed',
    [theme.breakpoints.up('md')]: {
      width: `calc(100% - ${values.drawerWidth}px)`,
    },
  },
  drawerButton: {
    [theme.breakpoints.up('md')]: {
      display: 'none',
    },
  },
  drawer: {
    width: values.drawerWidth,
    [theme.breakpoints.up('md')]: {
      position: 'fixed',
    },
  },
  // This is for spacing below toolbar
  toolbar: theme.mixins.toolbar,
  content: {
    display: 'flex',
    height: '100%',
    backgroundColor: theme.palette.background.default,
    [theme.breakpoints.up('md')]: {
      width: `calc(100% - ${values.drawerWidth}px)`,
      paddingLeft: values.drawerWidth,
    },
  },
});

class MapPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      mobileOpen: false,
      dataChecked: 0,
      geoChecked: 0,
    };
    this.data = {
      mil: { id: 1, name: 'mil', text: 'Military Bases' },
      air: { id: 2, name: 'air', text: 'Airports' },
      all: { id: 3, name: 'all', text: 'All' },
      neither: { id: 4, name: 'neither', text: 'Neither' },
    };
    this.geo = {
      state: { id: 1, name: 'state', text: 'State' },
      zip: { id: 2, name: 'zip', text: 'Zip' },
    };

    this.handleDrawerToggle = this.handleDrawerToggle.bind(this);
    this.dataHandler = this.dataHandler.bind(this);
    this.geoHandler = this.geoHandler.bind(this);
  }

  handleDrawerToggle() {
    this.setState({
      mobileOpen: !this.state.mobileOpen,
    });
  }

  dataHandler(event) {
    const { name } = event.target;

    this.setState({
      dataChecked: this.data[name].id,
    });
  }

  geoHandler(event) {
    const { name } = event.target;

    this.setState({
      geoChecked: this.geo[name].id,
    });
  }

  render() {
    const { classes, theme } = this.props;

    const drawer = (
      <DrawerOptions
        data={this.data}
        dataChecked={this.state.dataChecked}
        dataHandler={this.dataHandler}
        geo={this.geo}
        geoChecked={this.state.geoChecked}
        geoHandler={this.geoHandler}
      />
    );

    return (
      <div className={classes.root}>
        <AppBar className={classes.appbar}>
          <ToolBar>
            <IconButton
              className={classes.drawerButton}
              color='inherit'
              aria-label='open drawer'
              onClick={this.handleDrawerToggle}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant='title' color='inherit' noWrap>
              UFO Sightings
            </Typography>
          </ToolBar>
        </AppBar>
        <Hidden mdUp>
          <Drawer
            classes={{
              paper: classes.drawer,
            }}
            variant='temporary'
            anchor={theme.direction === 'rtl' ? 'right' : 'left'}
            open={this.state.mobileOpen}
            onClose={this.handleDrawerToggle}
            ModalProps={{
              keepMounted: true,
            }}
          >
            {drawer}
          </Drawer>
        </Hidden>
        <Hidden smDown implementation='css'>
          <Drawer
            classes={{
              paper: classes.drawer,
            }}
            variant='permanent'
            open
          >
            {drawer}
          </Drawer>
        </Hidden>
        <main className={classes.content}>
          <div className={classes.toolbar} />
          <Map />
        </main>
      </div>
    );
  }
}

MapPage.propTypes = {
  classes: PropTypes.object.isRequired,
  theme: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(MapPage);
