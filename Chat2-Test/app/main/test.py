# coding: utf-8

# Imports
#----------------------------------------------------------------------------#
from flask import render_template, session
from flask_socketio import emit
from . import main
from .. import socketio

# Config
#----------------------------------------------------------------------------#
'''app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat2_test_0920'

socketio = SocketIO(app)'''

user_no = 1

# Init
#----------------------------------------------------------------------------#
@main.before_request
def before_request():
    global user_no

    if 'username' in session:
        pass
    else:
        session['username'] = 'user'+str(user_no)
        user_no+=1

# Controllers
#----------------------------------------------------------------------------#
@main.route('/')
def index():
    return render_template('test.html')

@socketio.on('connect', namespace='/test')
def connect():
    emit('response', {'username': session['username'], 'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def disconnect():
    print 'Client disconnected'

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    emit('response', {'username': session['username'], 'data': 'Disconnected'})
    #disconnect()
    
@socketio.on('broadcast_event', namespace='/test')
def broadcast_event(msg):
    emit('response', {'username': session['username'], 'data': msg['data']}, broadcast=True)

# Launch
#----------------------------------------------------------------------------#
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
