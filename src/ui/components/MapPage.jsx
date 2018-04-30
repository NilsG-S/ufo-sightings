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
    height: `calc(100% - ${theme.mixins.toolbar.minHeight}px)`,
    backgroundColor: theme.palette.background.default,
    [theme.breakpoints.up('md')]: {
      height: 'calc(100% - 64px)',
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
      dataChecked: 'mil',
      geoChecked: 'none',
    };
    this.data = {
      mil: { name: 'mil', text: 'Military Bases' },
      air: { name: 'air', text: 'Airports' },
      all: { name: 'all', text: 'All' },
      neither: { name: 'neither', text: 'Neither' },
    };
    this.geo = {
      none: { name: 'none', text: 'None' },
      state: { name: 'state', text: 'State' },
      county: { name: 'county', text: 'County' },
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
      dataChecked: name,
    });
  }

  geoHandler(event) {
    const { name } = event.target;

    this.setState({
      geoChecked: name,
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
        <div className={classes.toolbar} />
        <main className={classes.content}>
          <Map
            dataChecked={this.state.dataChecked}
            geoChecked={this.state.geoChecked}
          />
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
