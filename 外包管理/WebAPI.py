import pandas as pd 
from pandas.io.json import json_normalize 
import os
from flask import Flask,request,jsonify
from flask_cors import CORS
from LexLib import ConnectDB
import json


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
        
    
    

if __name__ == '__main__':
    # RunRyFile 直接執行
    #app.run(host=server,port=iprot)
    app.run(host=server,port=iprot)