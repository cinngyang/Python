
***
<pre><code>
from sqlalchemy import create_engine

#engine = create_engine('oracle+cx_oracle://scott:tiger@tnsname')
#engine = create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')

DB_CONNECT_STRING = 'mssql+pymssql://usr:pwd@msdb1:1433/servername'
engine = create_engine(DB_CONNECT_STRING, echo=True)
connection = engine.connect()
result = connection.execute("select * from dbo.win ")
for row in result:
    print("bu:", row['winner'])
connection.close()    



DB_CONNECT_STRING = 'mssql+pymssql://usr:pwd@msdb1:1433/servername'
engine = create_engine(DB_CONNECT_STRING, echo=True)
strsql="select * from dbo.win"
connection = engine.connect()
dt=pd.read_sql_query(strsql,connection)

</code></pre>

strSql="select {0} from {1}"
strSql=strSql.format('emp_no','emp_data')

## Reference
[sqlalchemy学习笔记](https://segmentfault.com/a/1190000006949536)<br>
[Engine Configuration](https://docs.sqlalchemy.org/en/latest/core/engines.html?highlight=create_engine#database-urls)<br>
[Python Web Flask 實戰開發教學](https://blog.techbridge.cc/2017/08/12/python-web-flask101-tutorial-sqlalchemy-orm-database-models/)<br>
