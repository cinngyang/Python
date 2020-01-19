#%%
from LexLib import ConnectDB
import pandas as pd 


#定義全域變數
dbCon=ConnectDB.OracCn()

#定義SQL或由 File 輸入

def sqlGetModelGroup(Part='95%'):
    """取得 PKG Model Group"""
    
    sSQL=" select distinct l.model_group,l.model_name,l.part_no "
    sSQL+=" from erprpt.vsinv_itf_mtl l "
    sSQL+=" where l.part_no like '"+Part+"'"

    return sSQL


def GetPkgModelGroup():
    Part='95%'   
    strSql=sqlGetModelGroup(Part='95%')
    dfMG=dbCon.Exec_OracleCommend(dbCon.T01HIS1,strSql) 
    return dfMG


def main():
    pass


def ApiProcess(strfun):
    print(strfun)
    if strfun=="GetModelName":
        df=GetPkgModelGroup()
        return df
    





#%%
# 一般SQL 讀取資料
# Call StoreProcesude
# Web API
# Web Service

#寫入資料
#File


if __name__ == "__main__":
    print("RunPyFile")
    main()
else:
    print("Import Modlue")    

'''

#%%
df=ApiProcess("GetModelName")
df



# %%
'''