#測試JSON Format 資料
from flask import Flask,request,jsonify
from flask_cors import CORS
from flask import render_template
import os
import pandas as pd 
from pandas.io.json import json_normalize 
import numpy as np
from werkzeug.utils import secure_filename
import json

# Lextar 模組
import testApi


#Init App
app=Flask(__name__)
CORS(app)
app.config["DolodFiPath"] ="static/data/"
app.config["UploadPath"] ="tmp/"

def df_to_html_with_id(df, id, *args, **kwargs):
    s = df.to_html(*args, **kwargs)
    return s[:7] + 'id="%s" ' % id + s[7:]

@app.route('/',methods=['GET','POST'])
def home():   
    return render_template("LexTableTenp.html",title="基本測試",Function="功能測試")


@app.route('/Json/PostData',methods=['POST'])
def GetData():
                
        request_body=request.get_json() # <class 'dict'>               
        jb=json.loads(request_body) #<class 'list'>
        df=pd.DataFrame(jb)
        print(df.columns)
        headers=request.headers  
        
        df=pd.DataFrame([['PostJson','OK']],columns=['Function','Status'])

        return df.to_json(orient='table')

    

@app.route('/Json/PostFile',methods=['POST'])
def GetJsonFile():    
    #接收Excel File
    File =request.files['file']     
    df=pd.read_excel(File)
    #Header 資料
    headers=request.headers         
    Function=headers['Function']
    User=headers['User']  

    print("Function={} User={}".format(Function,User))
    
    #寫檔
    filename = secure_filename(File.filename)
    File.save(app.config["UploadPath"]+filename)

    #df=pd.DataFrame([['PostFile',filename,'OK']],columns=['Function','FielName','Status'])
        
    return df.to_json(orient='table')

@app.route('/api/Download',methods=["GET", "POST"])
def Download():
    try:
        fiName="dummy_data.xlsx"
        return send_from_directory(app.config["DolodFiPath"], filename=fiName, as_attachment=True)
    except FileNotFoundError:
        abort(404)   

#run Server
if __name__=='__main__':
    app.run(port=8000,debug=True)    
