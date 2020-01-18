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

#%%[1]
#全域變數
#使用者
userName=os.getlogin()
#Web API Server
ApiUrl="http://10.226.51.154:6500/api/RPTFunction/"
Folder=os.path.abspath(".")
#作業File
RptFile="外包CHIP庫存.xlsm"
LogFile="Log_"+datetime.now().strftime("%Y%M%d")+".log"
StFlag=True
LogMsg=""

#Config File
dfCon=pd.DataFrame()

#Active Excel
app = xw.App(visible=False)
wb = xw.Book(Folder+"\\"+RptFile)

#%%
#[2] 函數
def WiteLog(fileName,Msg):
    '''Write Log'''            
       
    with open(fileName,'a',encoding='utf-8') as fi:
        Msg=datetime.now().strftime('%Y%m%d %H:%M:%S')+","+Msg+"\n"
        fi.write(Msg)
        fi.close()  

def LoadConfig_1():

    """init"""
    #當成DataFrame 讀入
    dfCon=pd.read_excel(RptFile,sheet_name="Config")
    
    ChipFile=dfCon.iloc[0,1] 
    PoFile=dfCon.iloc[1,1] 
    BomFile=dfCon.iloc[2,1] 
    CommitFile=dfCon.iloc[3,1] 

    dfChip=pd.read_excel(ChipFile)
    dfPo=pd.read_excel(PoFile)
    dfBom=pd.read_excel(BomFile)
    dfCommit=pd.read_excel(CommitFile)
    
    return dfChip,dfPo,dfBom,dfCommit

def WritSheet(sheetName,df,index=False):
    """寫入Excel"""
    #檢查Sheet 是否存在
    flag=False
    for i in range(wb.sheets.count):
        if wb.sheets[i].name==sheetName:
            flag=True
            break

    if not flag :
        ws=wb.sheets.add(sheetName)       
    
    ws=wb.sheets[sheetName]
    ws.range("A1").options(index=False).value=df
    
    #調整表頭顏色
    ws.range(ws.range('A1').expand('right').address).color = rgb_to_int((0, 73, 134))
    ws.range(ws.range('A1').expand('right').address).api.Font.Color = rgb_to_int((255, 255, 255))
 
def WriteSoure(dfChip,dfPo,dfBom,dfCommit):
    "寫入原始資料到Excel 活頁"
    WritSheet("CHIP庫存",dfChip)
    WritSheet("OPEN PO",dfPo)
    WritSheet("外包 BOM",dfBom)
    WritSheet("Commit",dfCommit)

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

def ArrangeChip(dfCommit,dfBom):
    # Commit 對應 CHIP 
    # Commit 計算每日CHIP 需求
    dfCommitSum=pd.merge(dfCommit,dfBom,how='right',left_on='PART_NO',right_on='PKG')
    dfCommitSum=dfCommitSum[dfCommitSum['QTY']>0]
    dfCommitSum['CHIP_QTY']=dfCommitSum['QTY']*dfCommitSum['USAGE']
    cols=['CHIP','PKG','SHIFT_DATE','CHIP_QTY']
    dfCommitSum=dfCommitSum.loc[:,cols].groupby(['CHIP','SHIFT_DATE']).sum().reset_index()

    return dfCommitSum

def PreProcess(dfChip,dfPo,dfBom,dfCommit):
    """ 資料前置處理"""

    #原始資料
    #WriteSoure(dfChip,dfPo,dfBom,dfCommit)

    #Open PO CHIP 需求與 PO 彙整 
    dfChipReq,dfPoSum=ArrangePo(dfPo,dfBom,dfChip)

    #Chip 庫齡
    dfChipAge,dfChip=ArrangeChinInv(dfChip)

    #Chip Commit 需要的Chip 日期
    dfCommitSum=ArrangeChip(dfCommit,dfBom)
    # 輸出Excel 結果

    WritSheet('Chip 庫齡',dfChipAge)
    WritSheet('OPEN PO Sum',dfPoSum)
    WritSheet('Commit',dfCommitSum)
    
    return dfChipAge,dfPoSum,dfCommitSum

def ExcelFormatProcess():
    # 調整Format
    ws=wb.sheets['OPEN PO Sum']
    ws.range(ws.range("C2").expand().address).number_format = '#,##0;(0,000)'
    ws=wb.sheets['Chip 庫齡']
    ws.range(ws.range("B2").expand().address).number_format = '#,##0;(0,000)'
    ws=wb.sheets['Commit']
    ws.range(ws.range("C2").expand().address).number_format = '#,##0;(0,000)'


#%%[4] 主程式Debug
dfCon=pd.read_excel(RptFile,sheet_name="Config")
dfChip,dfPo,dfBom,dfCommit=LoadConfig_1()

#原始資料讀取
dfChipAge,dfPoSum,dfCommitSum=PreProcess(dfChip,dfPo,dfBom,dfCommit)
# Excel Format 調整
ExcelFormatProcess()

#%%[6]
# Commit 處理
dfCommitSum['Parm']='CHIP_REQ'
dfCommitSum=dfCommitSum.rename(columns={'CHIP_QTY':'QTY'})
dfCommitSum.head(2)

dfTemp=dfChipAge.loc[:,['PRODUCTNO','All']].reindex()
dfTemp=dfTemp.drop(dfTemp[dfTemp['PRODUCTNO']=='All'].index, axis=0)
dfTemp['Parm']='CHIP_INV'
dfTemp['SHIFT_DATE']=datetime(datetime.now().year, datetime.now().month, 1)
dfTemp=dfTemp.rename(columns={'PRODUCTNO':'CHIP','All':'QTY'})
dfTemp=dfTemp.append(dfCommitSum)

#生管樞紐格式與公式 缺Item 問題
dfTemp=dfTemp.pivot_table(index=['CHIP','Parm'],
columns='SHIFT_DATE',values='QTY',fill_value=0, aggfunc=np.sum)
#dfTemp.columns = dfTemp.columns.droplevel()
dfTemp=dfTemp.reset_index()
dfTemp.columns.name=None
WritSheet('CommitBlance',dfTemp)

#存檔
wb.save()
#wb.close()
#%%
def LoadExcel(FileName):
    """讀取原始檔"""    
    df1=pd.read_excel(FileName)
    # ReName Columns
    colimns=df1.iloc[0,:].to_list()
    df1.columns=colimns

    # 刪除表頭
    df1=df1.drop(df1.index[0])
    colName={"膜片号":"TypeID","批次号":"Lot","品号":"CPN","数量":"QTY","袋号":'boxid',"采购订单号":'customerpo'}
    df1=df1.rename(columns=colName)
    
    return df1

def CallApi_OpenPO():
    # Download     
    url=ApiUrl+"/?Function=GetPkgOspo" 
    r = requests.post(url)  
    df=pd.read_json(r.text,orient='table')
    #寫檔
    df.to_excel("2_OPEN_PO.xlsx")
    return df

def CallApi_OSPCommit():
    # Download 測試
    url=ApiUrl+"?Function=GetPkgOspCommit" 
    r=requests.post(url)
    df=pd.read_json(r.text,orient='table')
    #寫檔
    df.to_excel("4_外包_Commit.xlsx")
    return df

def CallApi_OspChipInv(dfChip):
    """ 取得外包CHIP 庫存 先供應商提供在回串出貨月份"""
    url=ApiUrl+"/?Function=OspChipInv" 
    r = requests.post(url, data=dfChip.to_json(orient='table'))
    df=pd.read_json(r.text,orient='table')
    #寫檔
    df.to_excel("1_外包庫存.xlsx")
    return df

def CallApi_Upload(dfBOM):
    """ 上傳外包 BOM"""
    url="http://10.226.51.154:6500/api/RPTFunction/?Function=OspChipInv" 
    r = requests.post(url, data=dfChip.to_json(orient='table'))
    df=pd.read_json(r.text,orient='table')
    #寫檔
    df.to_excel("1_外包庫存.xlsx")
    return df





#%%
# 上傳DataFrame
#url="http://10.226.51.154:6500/api/RPTFunction/?Function=XYZ"
#r = requests.post(url, data=dfSour.to_json(orient='table'))

#轉譯測試
#Js=dfSour.to_json(orient='table')
#data=json.loads(Js)   
#df = json_normalize(data['data'])
#df.head(2)


#%%
#測試傳送資料 & 取得資料
#Function  - 參數 - 利用 DataFrame

#%%
#debug




#%%
def main():    
    paser=ArgumentParser()
    
    # 非固定要數入
    #paser.add_argument("Name",help="一定要輸入")
    # 非固定要數入 , 有輸入則為 True
    paser.add_argument("-fun1",help="Function1",dest="Function1",default="HELLO")

    #取得輸入的參數
    args=paser.parse_args()

    print("傳入的參數",args)
    print("Name",args.Name)    
    print("Function1",args.Function1)
  

#%%
if __name__ == "__main__":
    print("RunPyFile")
    main()
else:
    print("Import Modlue")