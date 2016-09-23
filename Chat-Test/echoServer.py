# _*_ coding: utf-8 _*_
import socket
 
HOST = ''     # 가능한 모든 인터페이스를 의미
PORT = 50007  # 포트 지정

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # 소켓 생성
s.bind((HOST,PORT))                                  # 소켓 설정

s.listen(1)             # 접속 대기
conn, addr = s.accept() # 접속 승인
print('Connected by', addr)

while True:
    data = conn.recv(1024)
    if not data: 
        break
    conn.send(data)     # 받은 데이터를 그대로 클라이언트에 전송
conn.close()
