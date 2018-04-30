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

const styles = theme => ({
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
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    [theme.breakpoints.up('md')]: {
      paddingLeft: values.drawerWidth,
    },
  },
});

class MapPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      mobileOpen: false,
      geo: [
        { key: 0, checked: false, text: 'State' },
        { key: 1, checked: false, text: 'Zip' },
      ],
      data: [
        { key: 0, checked: false, text: 'Military Bases' },
        { key: 1, checked: false, text: 'Airports' },
        { key: 2, checked: false, text: 'All' },
        { key: 3, checked: false, text: 'Neither' },
      ],
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
    const arr = [...this.state.data];
    arr[name].checked = !arr[name].checked;

    this.setState({
      data: arr,
    });
  }

  geoHandler(event) {
    const { name } = event.target;
    const arr = [...this.state.geo];
    arr[name].checked = !arr[name].checked;

    this.setState({
      geo: arr,
    });
  }

  render() {
    const { classes, theme } = this.props;

    const drawer = (
      <DrawerOptions
        data={this.state.data}
        dataHandler={this.dataHandler}
        geo={this.state.geo}
        geoHandler={this.geoHandler}
      />
    );

    return (
      <div>
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
          <Typography noWrap>Testing</Typography>
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
