#透過 Excel 執行 Python
#上傳器
#Download 資料
#資料整理
#Upload 資料

#%%
import pandas as pd
from pandas.io.json import json_normalize
from datetime import datetime
from dateutil.relativedelta import relativedelta
from argparse import ArgumentParser
import xlwings as xw
from xlwings.utils import rgb_to_int
import requests,json,os
import numpy as np
import sys



#%%
#[2] 函數
def WiteLog(fileName,Msg):
    '''Write Log'''            
       
    with open(fileName,'a',encoding='utf-8') as fi:
        Msg=datetime.now().strftime('%Y%m%d %H:%M:%S')+","+Msg+"\n"
        fi.write(Msg)
        fi.close()  

def LoadConfig_1(FunName="NA"):

    """init"""
    
    #當成DataFrame 讀入
    if (debug):

        msg="路徑位址="+os.path.abspath(".")+"\r"
        msg+="RPTFile="+RptFile+"\r"    
        msg+="Who Call LoadConfig_1="+FunName
        WiteLog(LogFile,msg)


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

def WritSheet(sheetName,df,idx=False):
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
    
    return dfChipAge,dfPoSum,dfCommitSum

def ExcelFormatProcess():
    # 調整Format
    ws=wb.sheets['OPEN PO Sum']
    ws.range(ws.range("C2").expand().address).number_format = '#,##0;(0,000)'
    ws=wb.sheets['Chip 庫齡']
    ws.range(ws.range("B2").expand().address).number_format = '#,##0;(0,000)'
    ws=wb.sheets['Commit']
    ws.range(ws.range("C2").expand().address).number_format = '#,##0;(0,000)'
    ws=wb.sheets['CommitBalance']
    ws.range(ws.range("C2").expand().address).number_format = '#,##0;(0,000)'

def ArrangeCommitBlance(dfCommitSum,dfChipAge):    
    # Commit 處理 , #產生空白 DataFrame
    Parameters=['1_BOH','2_QTY','3_ComuCons','4_Blance']
    # 聯集Commit 與 庫存 CHIP
    Part1=dfCommitSum['CHIP'].unique()
    Part2=dfChipAge['PRODUCTNO'].unique()
    Part=np.append(Part1,Part2)
    Part=np.unique(Part)
    Part=np.delete(Part,-1)
    del Part1,Part2

    cols=['CHIP','Parameters','Flag']
    dfRes1=pd.DataFrame(columns=cols)
    for i in Part:
        for j in Parameters:
            dfRes1=dfRes1.append(pd.DataFrame(data=[[i,j,1]]
            ,columns=cols),ignore_index=True)

    dateVal=datetime(datetime.now().year, datetime.now().month, 1)

    #結合主表
    dfCommitSum['Parameters']='2_QTY'
    dfCommitSum=dfCommitSum.rename(columns={'CHIP_QTY':'QTY'})
    dfRes1=pd.concat([dfRes1, dfCommitSum], ignore_index=True,sort=False)
    # 庫存
    dfTemp=dfChipAge.loc[:,['PRODUCTNO','All']].reindex()
    dfTemp=dfTemp.drop(dfTemp[dfTemp['PRODUCTNO']=='All'].index, axis=0)
    dfTemp['Parameters']='1_BOH'
    dfTemp['SHIFT_DATE']=dateVal
    dfTemp=dfTemp.rename(columns={'PRODUCTNO':'CHIP','All':'QTY'})
    dfRes1=pd.concat([dfRes1, dfTemp.copy()], ignore_index=True,sort=True)
    del dfTemp

    #補值在樞紐, Qty 補0 , 日期補 當月 1 日
    dfRes1.loc[dfRes1['QTY'].isna(),'QTY']=0
    dfRes1.loc[dfRes1['SHIFT_DATE'].isna(),'SHIFT_DATE']=dateVal
    dfRes1.drop(['Flag'], axis=1)
 
    # 改字串'SHIFT_DATE' 
    dfRes1['SHIFT_DATE'] = dfRes1['SHIFT_DATE'].apply(lambda x: x.strftime('%Y/%m/%d'))

    #生管樞紐格式與公式
    dfRes1=dfRes1.pivot_table(index=['CHIP','Parameters'],
        columns='SHIFT_DATE',values='QTY',fill_value=0, aggfunc=np.sum)
    dfRes1=dfRes1.reset_index()
    dfRes1.columns.name=None
    return dfRes1

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

def init():
    os.chdir("D:\\python\\外包管理\\")

#%%[1]
#全域變數
#使用者
userName=os.getlogin()
#Web API Server
ApiUrl="http://10.226.51.154:6500/api/RPTFunction/"
Folder=os.path.abspath(".")
#Excele 檔名

RptFile="外包CHIP庫存.xlsm"
LogFile="Log_"+datetime.now().strftime("%Y%m%d")+".log"
StFlag=True
LogMsg=""
debug=True

#Config File
dfCon=pd.DataFrame()

msg="Init 路徑位址="+os.path.abspath(".")+"\r"
msg+="RPTFile="+Folder+"\\"+RptFile+"\r"
msg+="userName="+userName+"\n"

#Active Excel
app = xw.App(visible=False)
os.chdir("D:\\python\\外包管理\\")
wb = xw.Book("D:\\python\\外包管理\\外包CHIP庫存.xlsm")
WiteLog(LogFile,msg)

#%%
def main():    

    paser=ArgumentParser()
    paser.add_argument("-RptFile",help="ExcelFile",dest="ExcelFile",default="D:\\python\\外包管理\\")       
    paser.add_argument("-fun",help="Function1",dest="Function1",default="HELLO")
    

    #取得輸入的參數
    try :

        args=paser.parse_args()
         
        print(args.ExcelFile)
        FunName=args.Function1
        Excel=args.ExcelFile
    
        
        # 測試
        #ws=wb.sheets[0]
        #ws.range("A1").value="Hello"
    
        msg="路徑位址="+os.path.abspath(".")+"\r"
        msg+="RPTFile="+Folder+"\\"+RptFile+"\r"
        msg+="userName="+userName+"\n"
        msg+="FunName="+FunName

        WiteLog(LogFile,msg)

        if FunName=="main":             
    
            #主程式Debug
            dfCon=pd.read_excel(RptFile,sheet_name="Config")
    
            #LoadConfig_1 取得檔案清單
            dfChip,dfPo,dfBom,dfCommit=LoadConfig_1()

            #原始資料讀取
            dfChipAge,dfPoSum,dfCommitSum=PreProcess(dfChip,dfPo,dfBom,dfCommit)
    
            #計算Commit
            dfRes1=ArrangeCommitBlance(dfCommitSum,dfChipAge)
    
            # 輸出Excel 結果
            WritSheet('Chip 庫齡',dfChipAge)
            WritSheet('OPEN PO Sum',dfPoSum)
            WritSheet('Commit',dfCommitSum)
            WritSheet('CommitBalance',dfRes1)

            # Excel Format 調整
            ExcelFormatProcess()
         

        if FunName=="GetPkgOspo":
            #取得 OpenPO       
           
                   
    
    except:
        print("Err")
        msg=str(sys.exc_info()[0])
        WiteLog(LogFile,msg)

    #存檔
    finally:
        wb.save()  
        #wb.close()
        app.quit() 


#%%
if __name__ == "__main__":
    print("RunPyFile")
    main()
else:
    print("Import Modlue")



