let express = require("express"); /* 말그대로 express 프레임 워크 사용  */
let cors = require("cors"); /* 비용 문제 취소  */
let http = require("http"); /* 프로토콜에 대한  */
let bodyParser = require("body-Parser"); /* 말그대로 express 프레임 워크 사용  */
let path = require("path"); /* 말그대로 express 프레임 워크 사용  */

const port = 3000;


app = express();
const server = http.createServer(app).listen(port, () => {});


app.use(cors());
app.use(express.static(path.join(__dirname, 'client')));  /* 클라이언트 정의  */


app.use(bodyParser.json());

app.post('/server', (rep, res) => {
    io.emit('command', req.body);
    res.status(201).json({ status: 'reached'});
});

let io = require("socket.io")(server);

io.on('connection', (socket) => {
    socket.on('command', function(data) {
        io.emit('command', data);
    });
});  

