import pymssql 
import cx_Oracle
import pandas as pd
import sys
import os
from datetime import datetime
import csv

#20190520 Modify configFile
#20191227 重整架構

class OracCn():   
    
    dtConf=pd.DataFrame       
    
    def __init__(self):
        #MES
        self.T01HIS1='T01HIS1'             
        self.T05HIS01='T05HIS01'
        self.S01HIS01='S01HIS01'
        self.C01HIS01='C01HIS01'
        self.T01MES1='T01MES1'       
        self.T05MES01='T05MES01' 
        self.C01SMT='C01SMT'
        
        #MIS        
        self.LEX_PROD='LEX_PROD'    
        self.LEX_DEV='LEX_DEV'    
        self.T05DEV02='T05DEV02'
        self.T01DEV2='T01DEV2'
        self.lexmsdb1='lexmsdb1'
        self.lexmsdb2='lexmsdb2'
        self.lexmsdb9='lexmsdb9'
        self.lexdev09='lexdev09'
        self.lexmsdb6=r'lexmsdb6\dw'
        
    def WiteLog(self,Msg):
        """Write Log""" 
        fileName="Err_"+datetime.now().strftime('%Y%m%d')+".err"
        with open(fileName,'a',encoding='utf-8') as fi:
            Msg=datetime.now().strftime('%Y%m%d %H:%M:%S')+","+Msg+"\n"
            fi.write(Msg)  
            fi.close()

    def GeVersion(self):
        """回傳版本"""
        Ver={}
        Ver["pymssql"]=pymssql.__version__ 
        Ver["cx_Oracle"]=cx_Oracle.__version__
        Ver["pandas"]=pd.__version__        
        return Ver
    
    def GetFilePath(self):
        """取得當前目錄"""
        path=os.path.abspath('.')+"\\LexLib\\"
        return path    

    def __getPwd(self,severName):
        """傳入serverName 取得帳號密碼"""       
        try:
            fileName=self.GetFilePath()
            dtConf= pd.read_csv(fileName+'SqlCon.csv')         
            usr=dtConf.loc[dtConf['Server']==severName,'USR']  
            pwd=dtConf.loc[dtConf['Server']==severName,'PWD']
            usr=usr.values[len(usr.values)-1]
            pwd=pwd.values[len(pwd.values)-1]
        except:
            print("Unexpected error: function __getPwd", sys.exc_info()[0])
            msg="__getPwd Err"+sys.exc_info()[0]
            self.WiteLog(msg)
        return usr,pwd 

    def GetOrConn(self,severName):
        """serverName return oracle connection"""     
        usr,pwd=self.__getPwd(severName)        
        try :
            conn = cx_Oracle.connect(usr,pwd, severName,encoding='UTF-8', nencoding='UTF-8')       
            return conn        
        
        except:
            msg="GetOrConn Err"+"usr="+usr+" pwd="+pwd+" "+sys.exc_info()[0]             
            self.WiteLog(msg)            
            

        
    
    def Exec_OracleCommend(self,severName,strsql):
        """SrverName & sql retrun dataFrame"""
        try:          
            connection = self.GetOrConn(severName)          
            df=pd.read_sql_query(strsql,con=connection)
            connection.close()
            return df

        except Exception as err:
            print("Unexpected error: Exec_Commend", str(err))
            msg="GetOrConn Err"+str(err)
            self.WiteLog(msg)  

    
    def Ins_OracleCommend(self,severName,df,tableName=''):
        """serveranme , dataFrame , TableName"""
        
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
            msg="Ins_OracleCommend Err"+err+"\r\n"
            msg+=strsql+"\r\n"
            msg+=data
            self.WiteLog(msg)
            return  msg         
    
     
    def GetMSConn(self,dbName,severName):
        """Port 1433"""
        try :
            usr,pwd=self.__getPwd(severName)
            DB_CONNECT_STRING = 'mssql+pymssql://'+usr+':'+pwd+'@'+severName+':1433/'+dbName      
            return DB_CONNECT_STRING
        
        except Exception as err:
            msg="GetMSConn Err"+err+"\r\n"
            msg+="usr="+usr+"pwd="+pwd+"\r\n"
            self.WiteLog(msg)
            return  msg  
        
    
    
    #Change User & PWD
    def InsertMSSQL(self,df,severName='Lexmsdb2',usr='BinCntrlAP',pwd='BinCntrlAP@admin',dbName='Planning',
                tableNmae='[Planning].[dbo].[STOCK_BINCODE_RECORD]'):
        
        try:           

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
            
        except  Exception as err:

            print("InsertMSSQL", str(err))
            msg="InsertMSSQL"+err+"\r\n"
            msg+=strsql+"\r\n"
            self.WiteLog(msg)
            return  msg      

    
    def ExecMSSql_Commend(self,severName,dbName,strsql):
        """severName,dbName,strsql"""
        try:
            usr,pwd=self.__getPwd(severName)            
            connection=pymssql.connect(server=severName, user=usr, password=pwd, database=dbName)            
            dt=pd.read_sql_query(strsql,connection)   
            connection.close()
            return dt   
        except  Exception as err:

            print("ExecMSSql_Commend", str(err))
            msg="ExecMSSql_Commend"+err+"\r\n"
            msg+="usr="+usr+"pwd="+pwd+"\r\n"
            self.WiteLog(msg)
            return  msg  
                
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
            
            