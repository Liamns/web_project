import React, {useEffect}from 'react'; //eslint-disable-line no-unused-vars
import openSocket from 'socket.io-client'



const SOCKET_URL = 'http://localhost:3000' //eslint-disable-line no-unused-vars
let socket;                                  //eslint-disable-line no-unused-vars

const SocketService = () => {                        //eslint-disable-line no-unused-vars
                                              //eslint-disable-line no-unused-vars
    
    const setupSocket = () => {

        socket = openSocket(SOCKET_URL);
        socket.on('command', (data) => {
            console.log(data);
        });

    };

    useEffect(setupSocket, []);

    return <></>;
}

export default SocketService;


const sendSocket = (data) => {
    socket.emit('command', {
        type: data.type,
        id:data.id,
        content: data, content,
    });
};