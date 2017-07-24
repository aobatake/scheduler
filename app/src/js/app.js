import ReactDOM  from 'react-dom';
import React from 'react';
import {Provider} from 'react-redux';
import {BrowserRouter, Route} from 'react-router-dom';

import Classes from './components/Classes';
import configureStore from './store';

const Store = configureStore();

ReactDOM.render(
  <Provider store={Store}>
    <BrowserRouter>
      <div>
        <Route path='/' component={Classes} />
        <Route path='classes' component={Classes} />
      </div>
    </BrowserRouter>
  </Provider>
, document.getElementById('app'));
