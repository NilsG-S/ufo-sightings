import React from 'react';
import PropTypes from 'prop-types';

import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Divider from 'material-ui/Divider';
import Drawer from 'material-ui/Drawer';
import IconButton from 'material-ui/IconButton';
import Hidden from 'material-ui/Hidden';
import List, { ListItem, ListItemText } from 'material-ui/List';
import MenuIcon from '@material-ui/icons/Menu';
import ToolBar from 'material-ui/ToolBar';
import Typography from 'material-ui/Typography';

const drawerWidth = 240;
const styles = theme => ({
  appbar: {
    position: 'fixed',
    [theme.breakpoints.up('md')]: {
      width: `calc(100% - ${drawerWidth}px)`,
    },
  },
  drawerButton: {
    [theme.breakpoints.up('md')]: {
      display: 'none',
    },
  },
  drawer: {
    width: drawerWidth,
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
      paddingLeft: drawerWidth,
    },
  },
});

class ResponsiveApp extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      mobileOpen: false,
    };

    this.handleDrawerToggle = this.handleDrawerToggle.bind(this);
  }

  handleDrawerToggle() {
    this.setState({
      mobileOpen: !this.state.mobileOpen,
    });
  }

  render() {
    const { classes, theme } = this.props;

    const drawer = (
      <div>
        <div className={classes.toolbar} />
        <Divider />
        <List>
          <ListItem>
            <ListItemText primary='State' />
          </ListItem>
          <ListItem>
            <ListItemText primary='Zip' />
          </ListItem>
        </List>
        <Divider />
        <List>
          <ListItem>
            <ListItemText primary='Military Bases' />
          </ListItem>
          <ListItem>
            <ListItemText primary='Airports' />
          </ListItem>
          <ListItem>
            <ListItemText primary='All' />
          </ListItem>
          <ListItem>
            <ListItemText primary='Neither' />
          </ListItem>
        </List>
      </div>
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

ResponsiveApp.propTypes = {
  classes: PropTypes.object.isRequired,
  theme: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(ResponsiveApp);
