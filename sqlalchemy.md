
***
<pre><code>
from sqlalchemy import create_engine

#engine = create_engine('oracle+cx_oracle://scott:tiger@tnsname')
#engine = create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')

DB_CONNECT_STRING = 'mssql+pymssql://Viewer:ShiningQI@lexmsdb1:1433/BUDataCenter'

engine = create_engine(DB_CONNECT_STRING, echo=True)

connection = engine.connect()
result = connection.execute("select * from dbo.win ")
for row in result:
    print("bu:", row['winner'])
connection.close()    

</code></pre>

##Reference
[sqlalchemy学习笔记](https://segmentfault.com/a/1190000006949536)<br>
[Engine Configuration](https://docs.sqlalchemy.org/en/latest/core/engines.html?highlight=create_engine#database-urls)<br>
