import pymssql 
import cx_Oracle
import pandas as pd
import sys
import os
import csv

#20190520 Modify configFile

class OracCn():   
    
    dtConf=pd.DataFrame   
    
    
    def __init__(self):
        self.T01HIS1='T01HIS1'             
        self.T05HIS01='T05HIS01'
        self.S01HIS01='S01HIS01'
        self.C01HIS01='C01HIS01'
        self.T01MES1='T01MES1'       
        self.T05MES01='T05MES01'         
        self.LEX_PROD='LEX_PROD'    
        self.LEX_DEV='LEX_DEV'    
        self.T05DEV02='T05DEV02'
        self.T01DEV2='T01DEV2'
        self.lexmsdb1='lexmsdb1'
        self.lexmsdb2='lexmsdb2'
        self.lexmsdb9='lexmsdb9'
        self.lexdev09='lexdev09'
        self.lexmsdb6=r'lexmsdb6\dw'
        self.C01SMT='C01SMT'
        
    
    def GetFilePath(self):
        '取得當前目錄'
        path=os.path.abspath('.')+("\\Lexlib\\")
        return path    

    def __getPwd(self,severName):
        '傳入serverName 取得帳號密碼'        
        try:
            fileName=self.GetFilePath()
            dtConf= pd.read_csv(fileName+'SqlCon.csv')         
            usr=dtConf.loc[dtConf['Server']==severName,'USR']  
            pwd=dtConf.loc[dtConf['Server']==severName,'PWD']
            usr=usr.values[len(usr.values)-1]
            pwd=pwd.values[len(pwd.values)-1]
        except:
            print("Unexpected error: function __getPwd", sys.exc_info()[0])
        return usr,pwd 

    def GetOrConn(self,severName):
        'serverName return oracle connection'
        usr,pwd=self.__getPwd(severName)
        conn = cx_Oracle.connect(usr,pwd, severName,encoding='UTF-8', nencoding='UTF-8')       
        return conn
     
        
    
    def Exec_OracleCommend(self,severName,strsql):
        'SrverName & sql retrun dataFrame'
        try:          
            connection = self.GetOrConn(severName)          
            df=pd.read_sql_query(strsql,con=connection)
            connection.close()
            return df
        except Exception as err:
            print("Unexpected error: Exec_Commend", str(err))
    
    def Ins_OracleCommend(self,severName,df,tableName=''):
        'serveranme , dataFrame , TableName'
        try:
            connection = self.GetOrConn(severName)
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
        'Port 1433'
        usr,pwd=self.__getPwd(severName)
        DB_CONNECT_STRING = 'mssql+pymssql://'+usr+':'+pwd+'@'+severName+':1433/'+dbName      
        return DB_CONNECT_STRING
        
    
    
    #Change User & PWD
    def InsertMSSQL(self,df,severName='Lexmsdb2',usr='BinCntrlAP',pwd='BinCntrlAP@admin',dbName='Planning',
                tableNmae='[Planning].[dbo].[STOCK_BINCODE_RECORD]'):
        
        connection=pymssql.connect(server=severName, user=usr, password=pwd, database=dbName)
        cur = connection.cursor()     
        cols=df.columns.tolist()
        
        for ix in df.index:
            data=df.iloc[ix,:].tolist()        
            strsql="INSERT INTO "+tableNmae+"("+','.join(cols)+") VALUES ("        
        
            for i in data:
                strsql+="'"+str(i)+"',"         
            strsql=strsql[:len(strsql)-1]
            strsql+=")"  
        
            cur.execute(strsql)
            connection.commit()
            
        cur.close()
        connection.close()
        
        return True

    
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
    
    def WriteLog(self,path):
        os.chdir(path)
        
        return False
            
            