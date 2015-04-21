# Python Controller for complete Flask Blog

# imports
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import flash
from flask import redirect
from flask import url_for
from flask import g

import sqlite3
import os

from functools import wraps

# configuration 
DATABASE = 'sports_stats.db'
USERNAME = 'admin'
PASSWORD = 'hard_to_guess'
SECRET_KEY = os.urandom(24)

app = Flask(__name__)

# pulls in configurations by looking for uppercase variables
app.config.from_object(__name__)

# function use for connecting to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# define login_required decorator
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash ('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# define the root path, i.e. the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = "Invalid Credentials. Please try again."
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error = error)
    
# define the main page that will be displaying the blog posts
@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM soccer')
    posts = [dict(season=row[0], player=row[1], club=row[2], competition=row[3], goals=row[4]) for row in cur.fetchall()]
    g.db.close()
    return render_template('main.html', posts=posts)

# define function for adding and updating posts
@app.route('/add', methods=['POST'])
@login_required
def add():
    season = request.form['season']
    player = request.form['player']
    club = request.form['club']
    competition = request.form['competition']
    goals = request.form['goals']
    if not season or not player or not club or not competition or not goals:
        flash("All fields are required for a new entry. Please try again.")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('INSERT INTO soccer (season, player, club, competition, goals) values (?, ?, ?, ?, ?)',\
                     [season, player, club, competition, goals])
        g.db.commit()
        g.db.close()
        flash('New entry was successfully posted!')
        return redirect(url_for('main'))

# define the logout path
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out. See you later!')
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True) 
