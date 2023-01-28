
import React, { createContext, useReducer} from 'react';
import {
    updateChatReducer, 
    updateChatState, 
    userDetailReducer,
    userDetailState,
} from './reducers';

const reduceReducers = (...reducers) => (prevState, value, ...args) => {
    reducers.reduce(
        (newState, reducer) => reducer(newState, value, ...args), prevState
    )
}

const combinedReducers = reduceReducers(
    updateChatReducer, userDetailReducer
    );


const initialState = {                                                         //초기화 
    ...updateChatState,
    ...userDetailState,
}; 

const store = createContext(initialState)
const {Provider} = store

const StoreProvider = ({children}) => {
    const [state, dispatch] = useReducer(combinedReducers, initialState);

    return <Provider value={{state, dispatch}}>{children}</Provider>;
};

export {store, StoreProvider} ;