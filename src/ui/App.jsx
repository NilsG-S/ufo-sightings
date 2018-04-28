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
  root: {
    flexGrow: 1,
    height: 430,
    zIndex: 1,
    overflow: 'hidden',
    position: 'relative',
    display: 'flex',
    width: '100%',
  },
  appBar: {
    position: 'absolute',
    marginLeft: drawerWidth,
    [theme.breakpoints.up('md')]: {
      width: `calc(100% - ${drawerWidth}px)`,
    },
  },
  navIconHide: {
    [theme.breakpoints.up('md')]: {
      display: 'none',
    },
  },
  toolbar: theme.mixins.toolbar,
  drawerPaper: {
    width: drawerWidth,
    [theme.breakpoints.up('md')]: {
      position: 'relative',
    },
  },
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing.unit * 3,
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
      <div className={classes.root}>
        <AppBar className={classes.appBar}>
          <ToolBar>
            <IconButton
              className={classes.navIconHide}
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
              paper: classes.drawerPaper,
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
              paper: classes.drawerPaper,
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
