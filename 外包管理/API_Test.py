#%%
import API_Chip 
import pandas as pd
import importlib
import requests,json,jsonify
from pandas.io.json import json_normalize 


# %%
importlib.reload(API_Chip)

# %%
funName="GetPkgOspo"
df=API_Chip.ApiProcess(funName)
data=json.loads(df)   
result = json_normalize(data['data'])
result

# %%
url="http://10.226.51.154:6500/api/RPTFunction/?Function=GetPkgOspo"

dataset=pd.DataFrame()
r = requests.post(url)
data=json.loads(r.text)   
df = json_normalize(data['data'])




# %%
#接收資料
url="http://10.226.51.154:6500/api/WebApiTest?function=Hello"
r = requests.post(url)
data=json.loads(r.text) 
result = json_normalize(data['data'])
result

# %%
#Upload 資料
#發送測試
df = pd.DataFrame([['a', 'b'], ['c', 'd']],
                  index=['0', '1'],
                  columns=['Col_1', 'Col_2'])

dataset=df.to_json(orient='records')

#dataset = dataset.to_dict(orient='list')
#post_data = {'dataset ID': "makis", 'date start': "1", 'date end': "2", 'data': dataset}
post_data = { 'data': dataset}
url = "http://10.226.51.154:6500/api/WebApiTest/Upload?Function=123"
print("MessageSend")
r = requests.post(url, json=post_data)
print(r.text)
#retData=json.loads(r.text) 

#result = json_normalize(retData['data'])
#print(result.head(2))



# %%
