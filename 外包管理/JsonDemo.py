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


#%%
def LoadExcelFile():

    df=pd.read_excel('外包CHIP庫存.xlsm',sheet_name='外包庫存')
    colimns=df.iloc[0,:].tolist()
    df.columns=colimns
    df=df.drop(df.index[0],axis=0).reset_index(drop=True)
    return df


# %%
#傳送 Post File
df=LoadExcelFile()
strFiName='外包庫存.xlsx'
df.to_excel(strFiName)

fin = open(strFiName, 'rb')
url="http://127.0.0.1:6500/api/UploadExcel"
files = {'file': fin}
#files = {'file': (strFiName, open(strFiName, 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
r = requests.post(url, files=files)
data=json.loads(r.text)   
df = json_normalize(data['data'])



# %%


# %%
