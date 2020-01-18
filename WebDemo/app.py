#%%
from flask import Flask,request,jsonify
from flask import render_template
import os
import pandas as pd 


#Init App
app=Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return render_template("home.html")

@app.route("/tables")
def show_tables():
    data = pd.DataFrame(
        {
        'Name':['Carly','Rachel','Rice','Jason'],
        'Birth Month': [1, 12, 1, 3],
        'Origin': ['UK','USA', "TW", 'CN'],
        'Age': [29, 18, 16, 30],
        'Gender': ['f', 'f', 'm', 'm']
        })
   
    data.set_index(['Name'], inplace=True)
    data.index.name=None
    females = data.loc[data.Gender=='f']
    males = data.loc[data.Gender=='m']
    return render_template('view.html',tables=[females.to_html(classes='female'), males.to_html(classes='male')],
    titles = ['na', 'Female surfers', 'Male surfers'])

@app.route('/function',methods=['GET'])
def get():
    return jsonify({'msg':'Hello World'})

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

#run Server

if __name__=='__main__':
    app.run(port=8000,debug=True)
