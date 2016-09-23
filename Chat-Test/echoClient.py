# _*_ coding: utf-8 _*_
import socket
 
HOST = '127.0.0.1'    # localhost
PORT = 50007          # 서버와 동일한 포트 지정

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 소켓 생성

s.connect((HOST,PORT))  # 서버 접속
        
s.send('Hello, python') # 문자 전송
data = s.recv(1024)     # 서버로 부터 정보를 받음
s.close()
print('Received by', data)
