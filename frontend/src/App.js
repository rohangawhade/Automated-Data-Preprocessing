import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import { AuthProvider } from './Components/Contexts/AuthContext';


import SignUp from './Pages/SignUp/SignUp';

import 'antd/dist/antd.css';
import './App.css';
import Login from './Pages/Login/Login';
import SideBar from './Components/SideBar';


class App extends React.Component {

  render() {
    return (
      <Router>
        <AuthProvider>
          <Switch>
            <Route exact path="/">
              <SideBar comp={'home'}/>
            </Route>
            <Route exact path="/signup">
              <SignUp />
            </Route>
            <Route exact path="/login">
              <Login />
            </Route>
            <Route path="/process">
              <SideBar comp={'process'}/>
            </Route>
            <Route path="/model">
              <SideBar comp={'model'} />
            </Route>
            {/* <Route path="/CompModel">
              <SideBar comp={'compmodel'} />
            </Route> */}
            <Route path="/logout">
              <SideBar comp={'logout'} />
            </Route>
          </Switch>
        </AuthProvider>
      </Router>
    );
  }
}

export default App;