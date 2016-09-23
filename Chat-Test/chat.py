# _*_ coding: utf-8 _*_
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# Imports
#----------------------------------------------------------------------------#
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash
from contextlib import closing

import random
import string

# Config
#----------------------------------------------------------------------------#
DATABASE = 'chat.db'
SECRET_KEY = 'chat_test_0920'
NAME = None

app = Flask(__name__)
app.config.from_object(__name__)


# Database connection
#----------------------------------------------------------------------------#
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as sql:
            db.cursor().executescript(sql.read())
        db.commit()

@app.before_request
def before_request():
    if app.config['NAME'] == None:
        name = random.sample(string.lowercase + string.digits, 8)
        app.config['NAME'] = ''.join(name)
        init_db()
    g.db = connect_db()
@app.teardown_request
def teardown_request(exception):
    g.db.close()


# Controllers
#----------------------------------------------------------------------------#
@app.route('/')
def show_chatLog():
    cursor = g.db.execute('select name, text from chatLog order by sequence asc')
    chatLog = [dict(name=row[0], text=row[1]) for row in cursor.fetchall()]
    return render_template('show_chatLog.html', chatLog=chatLog)

@app.route('/chatting', methods=['GET', 'POST'])
def add_chatLog():
    if request.method == 'GET' or len(request.form['text']) == 0:
        flash('글자를 입력해주세요.')
    
    else:
        g.db.execute('insert into chatLog (name, text) values (?, ?)',
             [app.config['NAME'], request.form['text']])
        g.db.commit()
    return redirect(url_for('show_chatLog'))

# App launch
#----------------------------------------------------------------------------#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)

