#透過 Excel 執行 Python
#上傳器
#Download 資料
#資料整理
#Upload 資料

#%%
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from argparse import ArgumentParser
import xlwings as xw
from xlwings.utils import rgb_to_int
import requests
import json,os
import numpy as np
from pandas.io.json import json_normalize
import sys



#%%
#[2] 函數
def WiteLog(fileName,Msg):
    '''Write Log'''            
       
    with open(fileName,'a',encoding='utf-8') as fi:
        Msg=datetime.now().strftime('%Y%m%d %H:%M:%S')+","+Msg+"\n"
        fi.write(Msg)
        fi.close()  

def ArrangePo(dfPo,dfBom,dfChip):
          
    #取 OPEN PO > 0 的 PKG 料號,計算 OPEN PO 需要的 CHIP
    dfPo=dfPo[dfPo['OPEN_PO']>0]
    #Pkgs=dfPo['PART_NO'].unique()
    # 建立計算欄位
    dfPo['CHIP']='NA'
    dfPo['UNIT']=0
    dfPo['USAGE']=0

    # 計算 CHIP 需求量
    for i in range(dfBom.shape[0]):
        #print(dfParts.iloc[i,0],dfParts.iloc[i,1],dfParts.iloc[i,2])
        dfPo.loc[dfPo['PART_NO']==dfBom.iloc[i,0],'CHIP']=dfBom.iloc[i,1]
        dfPo.loc[dfPo['PART_NO']==dfBom.iloc[i,0],'UNIT']=dfBom.iloc[i,2]

    # 改公式嗎?
    dfPo['USAGE']=dfPo['UNIT']*dfPo['OPEN_PO']
    #ws=wb.sheets["OPEN PO"]
    #ws.range("A1").value=dfPo
    #可以這樣寫ws.range("O2:O{row}".format(row=last_row))
    #ws.range('R2:R43').formula = ['=O2*Q2']

    #OPEN 需要庫存
    INV=dfChip.loc[:,['PRODUCTNO','QTY']].groupby('PRODUCTNO').sum().reset_index()
    dfChipReq=dfPo.loc[dfPo['UNIT']>0,['CHIP','USAGE']].groupby('CHIP').sum().reset_index()
    dfChipReq=dfChipReq.rename(columns={'CHIP':'PRODUCTNO'}).reindex()
    dfChipReq=pd.merge(dfChipReq,INV,how='outer')
    dfChipReq=dfChipReq.fillna(0)
    dfChipReq['BALNCE']=dfChipReq['QTY']-dfChipReq['USAGE']
    dfChipReq=dfChipReq.rename(columns={'QTY':'供應商庫存','USAGE':'OPEN PO 需求'}).reindex()

    #WritSheet("CHIP調料",dfChipReq)
    #PO Summary
    dfPoSum=pd.pivot_table(dfPo,index=['MODEL_GROUP','MODEL_NAME'],columns=['MONTH'],values=['OPEN_PO',]
                          ,fill_value=0,aggfunc=np.sum,margins=True)
    dfPoSum.columns = dfPoSum.columns.droplevel()
    dfPoSum=dfPoSum.reset_index()
    dfPoSum.columns.name=None
    
    return dfChipReq,dfPoSum

def ArrangeChinInv(dfChip):
    #整理資料 供應商CHIP 庫靈
    dfChip['MONTH']=dfChip['SHIPPEDDATE'].apply(lambda x: x.month)
    dfChipAge=pd.pivot_table(dfChip,index=['PRODUCTNO'],columns=['MONTH'],values=['QTY',],fill_value=0,aggfunc=np.sum,margins=True)
    dfChipAge.columns = dfChipAge.columns.droplevel()
    dfChipAge=dfChipAge.reset_index()
    dfChipAge.columns.name=None
    return dfChipAge,dfChip

def ExcEnvInfo():
    #確認執行環境
    strCurPath=os.path.abspath(".")
    strUser=os.getlogin()
    
    return strCurPath,strUser

def GetExcFunction():
    '''取得 Excel 傳入的參數'''
    paser=ArgumentParser()
    paser.add_argument("-RptFile",help="ExcelFile",dest="ExcelFile",default="D:\\python\\外包管理\\")       
    paser.add_argument("-fun",help="Function Name",dest="Function",default="HELLO")

    args=paser.parse_args() 
    strFunName=args.Function
    strRepFile=args.ExcelFile

    return strFunName,strRepFile

def SenPostMsg(url,Parmater,df):
    ''' 發送 API 需求 Call url 接收 DataFrame POST 寫法 
    url="http://10.226.51.154:6500/api/WebApiTest/GetData"
    header={"Function":"Hello"}
    df=pd.DataFrame 上傳資料使用
    '''
    try:

        dataset=df.to_json(orient='records')
        post_data = { 'data': dataset}
        Msg="Call API url={0}, header={1}".format(url,str(Parmater))             
        WiteLog(LogFile,Msg)
        print("Prepare Message ")            

        #Send 
        r = requests.post(url,headers=Parmater,json=post_data)    
        print("Message Send")   
        #接收Json 格式資料, Server site df.to_json(orient='table')   
        data=json.loads(r.text) 
        print("Data Load")  
        result = json_normalize(data['data'])
        print("Passer Data")  
        result.drop(['index'],axis=1)

        return result

    except Exception as e:  

        Msg="SenPostMsg Err"+str(e)
        WiteLog(LogFile,Msg)   

def WritSheet(sheetName,df,wb,idx=False):
    """寫入Excel"""
    #檢查Sheet 是否存在
    flag=False
    for i in range(wb.sheets.count):
        if wb.sheets[i].name==sheetName:
            flag=True
            wb.sheets[i].clear()
            break

    if not flag :
        ws=wb.sheets.add(sheetName)       
    
    ws=wb.sheets[sheetName]
    ws.range("A1").options(index=idx).value=df
    
    #調整表頭顏色
    ws.range(ws.range('A1').expand('right').address).color = rgb_to_int((0, 73, 134))
    ws.range(ws.range('A1').expand('right').address).api.Font.Color = rgb_to_int((255, 255, 255))    

def LoadChipInv(FileName):
    """讀取原始供應商提供 CHIP"""    
    df1=pd.read_excel(FileName,sheet_name="外包庫存")
    # ReName Columns
    colimns=df1.iloc[0,:].to_list()
    df1.columns=colimns

    # 刪除表頭
    df1=df1.drop(df1.index[0])
    colName={"膜片号":"TypeID","批次号":"Lot","品号":"CPN","数量":"QTY","袋号":'boxid',"采购订单号":'customerpo'}
    df1=df1.rename(columns=colName)
    
    return df1



# 全域變數

#全域變數
#使用者
userName=""
#Web API Server
ApiUrl="http://10.226.51.154:6500/api/RptFunction/pkgOutSoring"
#Excele 檔名
Folder=os.path.abspath(".")
RptFile="D:\\python\\外包管理\\外包CHIP庫存.xlsm"
DirPath="D:\\python\\外包管理\\"
LogFile="Log_"+datetime.now().strftime("%Y%m%d")+".log"
StFlag=True
LogMsg=""
debug=True



def main():
    
    #環境變數
    strCurPath,strUser=ExcEnvInfo()    
    #接收執行參數
    strFunName,strRepFile=GetExcFunction()
    Msg="Program Start ,User={0} ,Path={1}  ,FunName={2}  ,RepFile={3}".format(strUser,strCurPath,strFunName,strRepFile)
    WiteLog(LogFile,Msg)
    
    app = xw.App(visible=False)
    os.chdir(DirPath)

        

    dfResult=pd.DataFrame()        
    if strFunName=="GetPkgOspo":

        header={"Function":"GetPkgOspo",'User':strUser}
        
        df = pd.DataFrame([['GetPkgOspo']],                  
                  columns=['Fucntion'])
        
        dfResult=SenPostMsg(ApiUrl,header,df)       
        
        wb = xw.Book(RptFile)
        WritSheet('外包 OPEN PO',dfResult,wb)   
        wb.save()   
        wb.close()     
    
    if strFunName=="OspChipInv":      
        #上傳CHIP 庫存 
       header={"Function":"OspChipInv",'User':strUser} 
       df=LoadChipInv(RptFile)
       dfResult=SenPostMsg(ApiUrl,header,df)  

    if strFunName=="GetOspPkgCommit":
        #取得commit
        header={"Function":"GetOspPkgCommit",'User':strUser}    
        print("ExcelFileName=",RptFile)
        df=LoadChipInv(RptFile)
        dfResult=SenPostMsg(ApiUrl,header,df) 


    
    app.quit()
#%%
if __name__ == "__main__":
    print("RunPyFile")
    main()
else:
    print("Import Modlue")


#%%


#發送 POST Data 測試
try:

    url="http://10.226.51.154:6500/api/RptFunction/pkgOutSoring"    
    Parmater={"Function":"OspChipInv","user":os.getlogin()}

    df = LoadChipInv(RptFile)    
    Msg="Call API url={0}, header={1}".format(url,str(Parmater))             
    #print(Msg)
    dataset=df.to_json(orient='records')
    post_data = { 'data': dataset}         
    print(dataset)    
    WiteLog(LogFile,Msg)
    print("Prepare Message ")            

    #Send 
    r = requests.post(url,headers=Parmater,json=post_data)    
    print("Message Send")   
    #接收Json 格式資料, Server site df.to_json(orient='table')   
    data=json.loads(r.text) 
    #result=SenPostMsg(url,Parmater,df)
    #print(result.head(2))
  

except Exception as e:
    print(str(e))




# #%%
# # 測試 API Function
# import API_Chip
# import importlib
# importlib.reload(API_Chip)

# df = pd.DataFrame([['GetPkgOspo']],                  
#                   columns=['Fucntion'])

# df=API_Chip.ApiProcess("GetPkgOspo",dfParm=df)
# df
#%%


# %%
