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

# configuration 
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'hard_to_guess'
SECRET_KEY = str(os.random(24))

app = Flask(__name__)

# pulls in configurations by looking for uppercase variables
app.config.from_object(__name__)

# function use for connecting to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

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
def main():
    return render_template('main.html')

# define the logout path
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out. See you later!')

if __name__ == '__main__':
    app.run(debug=True) 
