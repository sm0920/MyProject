# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from flask import render_template, request, session, redirect, url_for, flash
from . import main
from app.db import User, call_query
from app.manager import input_data, Password


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.args.get('clear'):
        session.clear()

    if request.method == 'POST':
        error = False

        session['userid'] = request.form['userid']
        session['password'] = request.form['password']
        session['username'] = request.form['username']

        if request.form['userid'] == '':
            flash('필수 입력란입니다.', 'id')
            error = True
        if request.form['password'] == '':
            flash('필수 입력란입니다.', 'pw')
            error = True
        if request.form['username'] == '':
            flash('필수 입력란입니다.', 'name')
            error = True
        
        if error:
            return redirect(url_for('main.signUp'))
        
        input_data(userid=request.form['userid'], 
                    password=request.form['password'], 
                    username=request.form['username'])
        
    return render_template('index.html', page='대기실')


@main.route('/signUp', methods=['GET'])
def signUp():
    return render_template('signUp.html', page='계정 만들기')


@main.route('/chat', methods=['POST'])
@call_query
def chat(query):
    error = False

    userid = session['userid'] = request.form['userid']
    password = session['password'] = request.form['password']
    roomname = session['roomname'] = request.form['roomname']
    
    if not bool(userid):
        flash('아이디를 입력하세요.', 'id')
        error = True
    elif query.filter(User.userid == userid).count() == 0:
        flash('유효한 아이디를 입력하세요.', 'id')
        error = True
        session.pop('userid')

    if not bool(password):
        flash('비밀번호를 입력하세요.', 'pw')
        error = True
    else:
        user = query.filter_by(userid=userid).first()

        if not user or not user.password_hash == Password(password):
            flash('잘못된 비밀번호입니다.', 'pw')
            error = True
            session.pop('password')
        
    if not bool(roomname):
        flash('방제목을 입력하세요.', 'room')
        error = True

    if error:
        return redirect(url_for('main.index'))
    session['username'] = query.filter_by(userid=userid).one().username
    return render_template('chat.html', page=roomname)
