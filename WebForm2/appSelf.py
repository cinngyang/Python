import os

from flask import Flask, render_template
from flask import flash, redirect,url_for, request, send_from_directory, session
from LexLib import ConnectDB
from flask_cors import CORS
from forms import LoginForm

app=Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/basic')
def basic():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('index'))
    return render_template('basic.html', form=form)

@app.route('/bootstrap', methods=['GET', 'POST'])
def bootstrap():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('index'))
    return render_template('bootstrap.html', form=form)

if __name__=='__main__':
    app.run(port=8000,debug=True)