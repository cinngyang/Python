#%%
import pandas as  pd 
import requests
from flask import Flask,request,jsonify,render_template 
from flask_cors import CORS
import os

app=Flask(__name__)
CORS(app)


# %%
#Post 傳送 File 
def PostFile():
    """利用Jason 傳送 File 另一總方式利用File Server download """
    strFiName=os.path.abspath('.')+"//static//data//"+'dummy_data.xlsx'
    fin = open(strFiName, 'rb')
    url="http://127.0.0.1:8000/Json/PostFile"
    files = {'file': fin}
    headers={'Function':'POST_Header','User':os.getlogin()}
    print("Post Message Send {0}".format(url))
    r = requests.post(url,headers=headers,files=files)

    # # 接收傳資料
    # data=json.loads(r.text)   
    # df = json_normalize(data['data'])
    # print(df.head(2))


def PostJson2():
    dataset=pd.DataFrame([['2020/01/01',222,'AB'],['2020/01/02',232,'CD']],
    columns=['Date','Numner','var'])
    
    post_data=dataset.to_json(orient='records')
    #post_data = { 'object': dataset}      

    headers={'Function':'POST_Header','User':os.getlogin()}
    #print(dataset)            
    #Send 
    url="http://127.0.0.1:8000/Json/PostData"
    r = requests.post(url,headers=headers,json=post_data)    
    print("Message Send response={}".format(r))   
    

def df_to_html_with_id(df, id, *args, **kwargs):
    """新增 dataframe html id """
    s = df.to_html(*args, **kwargs)
    return s[:7] + 'id="%s" ' % id + s[7:]

@app.route('/',methods=['GET'])
def home():
    """網頁 Demo"""
    return render_template("Json.html")

@app.route('/Jqgride',methods=['GET'])
def Jqgride():
    """網頁 Demo"""
    #return render_template("Jqgride_1.html")
    return render_template("Jqgride_2.html")
    

@app.route('/SendMessage',methods=['POST','GET'])
def sendJson():
    if (request.method=="GET"):
        return "<H1> OK"
    else:        
        PostJson2()
        print("Message send")   


if __name__=='__main__':
    app.run(port=8000,debug=True)



