使用 Flask 建立 RESTful API

<code>
#service.py
from flask import Flask,request,abort
from sqlalchemy import create_engine
import pandas as pd
from bson.json_util import dumps, default

app=Flask(__name__)

@app.route('/api/Worker1')
def get_country_data():    
 
    query_dict={} 
    for key in ['BU']:
        arg=request.args.get(key)
        if arg:
            query_dict[key]=arg
            
    DB_CONNECT_STRING = 'mssql+pymssql://usr:pwd@msdb1:1433/DB1'
    engine = create_engine(DB_CONNECT_STRING, echo=True)
    strsql="select * from dbo.Hello "
    connection = engine.connect()
    dt=pd.read_sql_query(strsql,connection)
    dtjson=dt.to_json(orient='split')
    return dtjson 

    
if __name__=="__main__":
   app.run(port=8000,debug=True)
</code>

<code>
#API.py
import requests

services='http://127.0.0.1:8000/api/Worker1'
parmsVal={'BU':'AUO'}
reponse=requests.get(services,params=parmsVal)
ret=reponse.json()
</code>


****
背景知識<p>
+ 装饰器的返回值也是一个函数/类对象
## Reference
[Python 装饰器](https://foofish.net/python-decorator.html)<br>
