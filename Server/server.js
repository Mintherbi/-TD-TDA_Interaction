// server.js
const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const path = require('path');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// 웹페이지 파일들이 있는 폴더 지정 (public 폴더)
app.use(express.static(path.join(__dirname, 'public')));

// 웹소켓 연결 처리
wss.on('connection', (ws) => {
    console.log('새로운 유저가 접속했습니다.');

    // 유저(웹)로부터 메시지를 받으면
    ws.on('message', (message) => {
        // Buffer를 문자열로 변환 (중요: 브라우저가 Blob으로 받지 않도록 함)
        const msgString = message.toString();

        // TouchDesigner가 연결된 소켓으로 그대로 전달 (브로드캐스트)
        wss.clients.forEach((client) => {
            if (client !== ws && client.readyState === WebSocket.OPEN) {
                client.send(msgString);
            }
        });
    });
});

// 서버 시작 (환경 변수 포트 또는 3000번)
const PORT = process.env.PORT || 3000;
server.listen(PORT, '0.0.0.0', () => {
    console.log(`서버가 실행되었습니다. 포트: ${PORT}`);
});