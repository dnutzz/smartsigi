import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";

import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Grid
} from "@material-ui/core";
import MenuIcon from '@material-ui/icons/Menu';

// Import components
import Home from "./components/Home";

function App() {
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <IconButton edge="start" color="inherit" aria-label="menu">
            <MenuIcon />
          </IconButton>
          <Typography>
            smart.sigi
          </Typography>
        </Toolbar>
      </AppBar>
      <Grid
        container
        direction="row"
        justify="left"
        alignItems="center"
        style={{ padding: 10 }}
      >
        <Router>
          <Switch>
            <Route path="/">
              <Home />
            </Route>
          </Switch>
        </Router>
      </Grid>
    </div>

  );
}



export default App;
