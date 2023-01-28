import React from 'react';
import ReactDom from 'react-dom';
import App from './app'; //eslint-disable-line no-unused-vars
import {StoreProvider} from './stateManagement/store'; //eslint-disable-line no-unused-vars
import SocketService from './socketService'; //eslint-disable-line no-unused-vars


ReactDom.render(
    <StoreProvider>
        <App/>
        <SocketService/>
    </StoreProvider>,

    document.getElementById('root')

);  