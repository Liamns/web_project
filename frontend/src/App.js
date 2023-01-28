import React, { useState, useEffect, useContext } from 'react'; //eslint-disable-line no-unused-vars
import { userDetailAction } from './stateManagement/actions';
import { store } from './stateManagement/store';

const SimpleMessage = (props) => {

    const [name, setName] = useState('');
    const [showMessage, setShowMessage] = useState(false);


    const {dispatch} = useContext(store)

    const onsubmit = (e) => {
        e.preventDefault();
        dispatch({ type: userDetailAction, payload: name});
        setShowMessage(true);

    };

    return (
        <>
        {!showMessage ? (
          <div>
            <h3>Hello there, Please Enter your name</h3>
            <form onSubmit={onsubmit}>
              <input value={name} onChange={(e) => setName(e.target.value)} />
              <button type="submit">submit</button>
            </form>
          </div>
        ) : (
          <MessageInterface />
        )}
      </>
    );
};  

export default SimpleMessage;



const MessageInterface = props => {

    const [name, setName] = useState('');

    const { state } = useContext(store);

    return (
        <div>
            <h2> Hello Username</h2>
            <form action="">
                <textarea></textarea>
                <button>send</button>
            </form>
            <br/>
            {
                messages.length < 1 ? <div>No messages yet</div>
                messages.map()

            }
            
        </div>
    );
};