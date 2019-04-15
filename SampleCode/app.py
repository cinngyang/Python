from flask import Flask,request,jsonify
import os
import pandas as pd

#Init App
app=Flask(__name__)

dfRaw=pd.read_csv('Sample.csv')

@app.route('/',methods=['GET'])
def get():
    return jsonify({'msg':'Hello World'})

# 沒定 Moethods=GET
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath

@app.route('/raw/')
def show_df():
    #return dfRaw.to_json(orient='columns')
    return dfRaw.to_json(orient='records')

#run Server

if __name__=='__main__':
    app.run(port=8000,debug=True)

