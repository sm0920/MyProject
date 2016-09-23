# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio


@socketio.on('room_joined', namespace='/chat')
def room_joined(msg):
    user = session.get('username')
    room = session.get('roomname')

    join_room(room)
    emit('notice', {'notice': "<'" + user + "' 님이 입장하셨습니다.>"}, room=room)


@socketio.on('chat_submit', namespace='/chat')
def chat_submit(msg):
    user = session.get('username')
    room = session.get('roomname')

    emit('chat', {'chat': user + ': ' + msg['msg']}, room=room)


@socketio.on('room_left', namespace='/chat')
def room_left(msg):
    user = session.get('username')
    room = session.get('roomname')

    leave_room(room)
    emit('notice', {'notice': "<'" + user + "' 님이 퇴장하셨습니다.>"}, room=room)
