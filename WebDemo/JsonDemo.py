#jsonify vs json.dump() : Content-Type有不同 json vs txt 
#jsonify 可與
#request 快速上手
#https://segmentfault.com/a/1190000018374275

#%%
import pandas as  pd 
from pandas.io.json import json_normalize 
import json
import requests
from flask import jsonify
import os


#%%
def LoadExcelFile():
    #測試資料
    file=os.path.abspath('.')+"//static//data//"+'dummy_data.xlsx'
    df=pd.read_excel(file)
    #colimns=df.iloc[0,:].tolist()
    #df.columns=colimns
    #df=df.drop(df.index[0],axis=0).reset_index(drop=True)
    return df


# %%
#傳送 Excel File
def PostFile():
    strFiName=os.path.abspath('.')+"//static//data//"+'dummy_data.xlsx'
    fin = open(strFiName, 'rb')
    url="http://127.0.0.1:8000/Json/PostFile"
    files = {'file': fin}
    headers={'Function':'POST_Header','User':os.getlogin()}
    print("Post Message Send {0}".format(url))
    r = requests.post(url,headers=headers,files=files)

    # 接收傳資料
    data=json.loads(r.text)   
    df = json_normalize(data['data'])
    print(df.head(2))

# %%
#傳送 JSON Data
def PostJson():
    dataset=LoadExcelFile()
    dataset=dataset.to_json(orient='records')        
    post_data=dataset  
    
    headers={'Function':'POST_Header','User':os.getlogin()}
    #print(dataset)            
    #Send 
    url="http://127.0.0.1:8000/Json/PostData"
    r = requests.post(url,headers=headers,json=post_data)    
    print("Message Send")   


# %%

def PostJson2():
    dataset=pd.DataFrame([['2020/01/01',222,'AB'],['2020/01/02',232,'CD']],
    columns=['Date','Numner','var'])
    
    dataset=dataset.to_json(orient='records')
    #post_data = { 'object': dataset}  
    post_data =dataset

    headers={'Function':'POST_Header','User':os.getlogin()}
    #print(dataset)            
    #Send 
    url="http://127.0.0.1:8000/Json/PostData"
    r = requests.post(url,headers=headers,json=post_data)    
    print("Message Send")   
    


# %%


