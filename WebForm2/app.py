#%%
from LexLib import ConnectDB
import pandas as pd 
from flask import Flask, render_template, flash, redirect, url_for,Markup
from flask_cors import CORS
import os

#%%
app=Flask(__name__)
CORS(app)

# %% 變數
# @app.context_Processpr
# def inject_env():

#自訂過濾器
@app.template_filter()
def usrFun(s):
    return s+5;

user = {
    'username': 'Chin Yang',
    'bio': 'A boy who loves movies and music.',
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]

# register template filter
@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')

# register template test
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False

@app.context_processor
def inject_info():
    foo = 'I am foo.'
    return dict(foo=foo)  # equal to: return {'foo': foo}


# register template global function
@app.template_global()
def bar():
    return 'I am bar.'

@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/watchlist2')
def watchlist_with_static():
    return render_template('watchlist_with_static.html', user=user, movies=movies)

# message flashing
@app.route('/flash')
def just_flash():
    flash('I am flash, who is looking for me?')
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(port=8000,debug=True)
