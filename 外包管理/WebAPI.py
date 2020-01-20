#%%
import pandas as pd 
from pandas.io.json import json_normalize 
import os
from flask import Flask,request,jsonify
from flask import render_template
from flask_cors import CORS
from LexLib import ConnectDB
import json
    #Download File
    #https://pythonise.com/series/learning-flask/flask-http-methods
from flask import send_file, send_from_directory, safe_join, abort


#客製 API imoprt
import API_Chip

#全域變數
dncn=ConnectDB.OracCn()
#server='10.226.51.154'
server='127.0.0.1'
iprot=6500
FilePath=os.path.abspath(".")
FilePath=FilePath+("\\APPData\\")



app = Flask(__name__)
CORS(app)
app.config.from_pyfile("app.cfg")
app.config["DolodFiPath"] ="static/data/"

def df_to_html_with_id(df, id, *args, **kwargs):
    s = df.to_html(*args, **kwargs)
    return s[:7] + 'id="%s" ' % id + s[7:]


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route('/api/Web', methods=["GET", "POST"])
def BasTable():
    x=pd.read_excel("外包庫存.xlsx")
    xtable=df_to_html_with_id(x,"example",classes='display')
    return render_template("jqueryTable.html",data=xtable,title="Download")

@app.route('/api/RptFunction/pkgOutSoring', methods=["GET", "POST"])
def PkgOutSource():
    # Function
    
    Function=""
    df=pd.DataFrame()
    
    if request.method=="GET" :        
        Function = request.args['Function']
    else:
               
        post_data =request.get_json()    
        df = json_normalize(post_data)   
        headers=request.headers         
        Function=headers['Function']
        User=headers['User']    
        df=API_Chip.ApiProcess(Function,df)
        
        return df.to_json(orient='table')

    #print(df.head(2))
  
    return df.to_json(orient='table')

@app.route('/api/UploadExcel', methods=["GET", "POST"])
def UploadFile():
    if request.method=="GET" :
        return "HELLO"
    else :
        df=pd.DataFrame([['UploadFile', 'Sucess']],columns=['Function','Status'])
        file = request.files['file']
        filename=file.filename        
        #df=pd.read_excel(filename)
        #file.save("C:\\Data\\GitHub\\Python\\外包管理\\tmp\\"+filename)
        return df.to_json(orient='table')

@app.route('/api/Download',methods=["GET", "POST"])
def Download():
    try:
        fiName="dummy_data.xlsx"
        return send_from_directory(app.config["DolodFiPath"], filename=fiName, as_attachment=True)
    except FileNotFoundError:
        abort(404)        
    
    

if __name__ == '__main__':
    # RunRyFile 直接執行
    #app.run(host=server,port=iprot)
    app.run(host=server,port=iprot)

# %%
