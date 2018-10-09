使用 Flask 建立 RESTful API

<pre><code>
#service.py
#取得工作路徑
import os
wPath=os.path.abspath('.')
os.chdir(wPath)

from flask import Flask,request,abort
from bson.json_util import dumps, default
import ConnectDB as cn
import pandas as pd


app=Flask(__name__)

@app.route('/api/winners')
def get_country_data():    
 
    BU=request.args.get('BU')
    version=request.args.get('version')
    
    dbcon=cn.OracCn()    
    strsql="select  *  from dbo.Table H where H.version='"+version+"' and BU='"+BU+"' "
    dt=dbcon.ExecMSSql_Commend(dbcon.lexmsdb1,'BUDataCenter',strsql)
    return dt.to_json(orient='index')    

    
if __name__=="__main__":
   app.run(port=8000,debug=True)
   
</code><pre>

<pre><code>
#API.py
import os
wPath=os.path.abspath('.')
os.chdir(wPath)
import requests
import pandas as pd

services='http://127.0.0.1:8000/api/winners'
parmsVal={'version':'20181006BEF','BU':'BU1'}
reponse=requests.get(services,params=parmsVal)
ret=reponse.json()
dt=pd.DataFrame.from_dict(ret, orient='index')

</code></pre>






****
背景知識<p>
+ 装饰器的返回值也是一个函数/类对象
## Reference
[Python 装饰器](https://foofish.net/python-decorator.html)<br>
[使用 Flask-RESTful 设计 RESTful API](http://www.pythondoc.com/Flask-RESTful/quickstart.html)<br>
[透過 curl、Python、Postman 來 Request API](https://jzchangmark.wordpress.com/2016/06/12/%E9%80%8F%E9%81%8E-curl%E3%80%81python%E3%80%81postman-%E4%BE%86-request-api/)<br>
