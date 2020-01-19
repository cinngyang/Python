#%%
from flask import Flask,request,jsonify
from flask_cors import CORS
from flask import render_template
import os,testApi
import pandas as pd 
import numpy as np


#Init App

app=Flask(__name__)
CORS(app)

def df_to_html_with_id(df, id, *args, **kwargs):
    s = df.to_html(*args, **kwargs)
    return s[:7] + 'id="%s" ' % id + s[7:]

#網址工功能定義
@app.route('/',methods=['GET'])
def home():
    return render_template("home.html")

@app.route("/tables")
def show_tables():
    #http://127.0.0.1:8000/tables
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

@app.route("/jquerytable")
def showJqueryTable():
    x=pd.DataFrame(np.random.randn(20, 5))   
    xtable=df_to_html_with_id(x,"example",classes='display')
    return render_template("jqueryTable.html",data=xtable,title="Download")

@app.route('/Getfunc',methods=['GET'])
def get():
    #http://127.0.0.1:8000/Getfunc?function=GetModelName
    strFun=request.args.get('function')
    #print(strFun)
    df=testApi.ApiProcess(strFun)            
    return render_template('view.html',tables=[df.to_html(classes='male')], titles=['Model Group'])

   

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

#run Server

if __name__=='__main__':
    app.run(port=8000,debug=True)


#%%


# %%
