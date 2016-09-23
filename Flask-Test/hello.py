# _*_ coding: utf-8 _*_
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, render_template, request, session, redirect, url_for, \
        make_response, flash
from database import db_session

app = Flask(__name__)
app.secret_key = 'test_0920'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

@app.route('/')
def index():
    if 'username' in session:
        return '%s 님 환영합니다.' % session['username']
    return 'Index Page'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        passward = request.form['password']

        session['logFlag'] = True
        session['username'] = username
        return redirect(url_for('index'))
    else:
        if session['logFlag'] == True:
            return '이미 로그인 상태입니다.'
        else:
            return render_template('login_test.html')

@app.route('/logout')
def logout():
    if 'logFlag' in session and session['logFlag'] == True:
        app.logger.debug('엥??')

        session['logFlag'] = False
        session.pop('username', None)
        flash('로그아웃 하셨습니다.')
        return redirect(url_for('index'))
    else:
        app.logger.debug(session['logFlag'])
        return '로그인 상태가 아닙니다.'

@app.errorhandler(405)
def catchToError(error):
    resp = make_response(render_template('hello.html'), 405)
    return resp     

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
