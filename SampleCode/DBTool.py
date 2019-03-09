#from sqlalchemy import create_engine
import pymssql 
import cx_Oracle
import pandas as pd
import sys
import os
import csv

class OracCn():
    os.environ["NLS_LANG"] = "German_Germany.UTF8"
    dtConf=pd.DataFrame 
    
    def __init__(self):
        self.T01HIS1='T01HIS1'             
        self.T05HIS01='T05HIS01'
        self.S01HIS01='S01HIS01'
        self.C01HIS01='C01HIS01'
        self.T01MES1='T01MES1'
        self.T05MES01='T05MES01'         
        self.LEX_PROD='LEX_PROD'      
        self.T05DEV02='T05DEV02'
        self.T01DEV2='T01DEV2'
        self.lexmsdb1='lexmsdb1'
        self.lexmsdb2='lexmsdb2'
        self.lexmsdb9='lexmsdb9'
        self.lexmsdb6='lexmsdb6\dw'
        
    
    def GetConn(self,severName):
        usr,pwd=self.__getPwd(severName)
        conn = cx_Oracle.connect(usr,pwd, severName,encoding='UTF-8', nencoding='UTF-8')       
        return conn
      
    
    def __getPwd(self,severName):        
        try:
            dtConf= pd.read_csv('SqlCon.csv')         
            usr=dtConf.loc[dtConf['Server']==severName,'USR']  
            pwd=dtConf.loc[dtConf['Server']==severName,'PWD']
            usr=usr.values[len(usr.values)-1]
            pwd=pwd.values[len(pwd.values)-1]
        except:
            print("Unexpected error: function __getPwd", sys.exc_info()[0])
        return usr,pwd 
    
    def Exec_OracleCommend(self,severName,strsql):
        try:          
            connection = self.GetConn(severName)          
            df=pd.read_sql_query(strsql,con=connection)
            connection.close()
            return df
        except Exception as err:
            print("Unexpected error: Exec_Commend", str(err))
    
    def Ins_OracleCommend(self,severName,df,tableName=''):
        try:
            connection = self.GetConn(severName)
            cursor = cx_Oracle.Cursor(connection)
            # Insert SQL
            cols=df.columns.tolist()
            strsql="INSERT INTO "+ tableName +"("+','.join(cols)+") VALUES ( :"+",:".join(cols)+")"                      
           
            for ix in df.index:
                data=df.iloc[ix,:].tolist()
                #rt={strsql:data}
                cursor.execute(strsql, data)
            connection.commit()
            #return  rt   
        except Exception as err:
            print("Unexpected error: Ins_OracleCommend", str(err))
     
    def GetMSConn(self,dbName,severName):
        usr,pwd=self.__getPwd(severName)
        DB_CONNECT_STRING = 'mssql+pymssql://'+usr+':'+pwd+'@'+severName+':1433/'+dbName
        #engine = create_engine(DB_CONNECT_STRING, echo=True)
        #connection = engine.connect()
        return DB_CONNECT_STRING
        #connection
    

    
    def ExecMSSql_Commend(self,severName,dbName,strsql):
        try:
            usr,pwd=self.__getPwd(severName)            
            connection=pymssql.connect(server=severName, user=usr, password=pwd, database=dbName)            
            dt=pd.read_sql_query(strsql,connection)   
            connection.close()
            return dt   
        except  Exception as err:
             print("ExecMSSql_Commend", str(err))
                
class FileProcss():
    
    def DelFile(self,myfile):
        ## If file exists, delete it ##
        if os.path.isfile(myfile):
            os.remove(myfile)
            return True
        return False
    
    def WriteLog(path):
        os.chdir(path)
        
        return False
            