#%%
import pandas as pd 
import xlwings as xw 
import os
from xlwings.utils import rgb_to_int

#Excel 選取
#https://www.jianshu.com/p/de7efe591c12
#https://wenku.baidu.com/view/dad03a770166f5335a8102d276a20029bd646330.html
#格式
#https://www.dataquest.io/blog/python-excel-xlwings-tutorial/
#公式
#http://hk.voidcc.com/question/p-kqlzewkz-vg.html
#dir(xw.constants) 支援VBA

#顏色定義
FvlBlue=(0, 73, 134)
White=(255, 255, 255)
LexRed=(199, 0, 37)
LexGray=(206, 211, 217)
#格式定義
Format_Number="#,##0_);[紅色](#,##0)"
Format_Number_Date="yyyy/m/d"
Format_Number_Month="yyyy/m"

#Laset Columns
#last_column = ws.range(1,1).end('right').get_address(0,0)[0]
#ws.range('A1:{}1'.format(last_column)).api.Borders(9).LineStyle = -4119


#%%
#Excel 公式參考
# ws.range('B4:F4').formula=[['=B2-B3']]
# strFormular="=".+ws.cells(2,2).address+"-"+ws.cells(3,2).address
# ws.range('B4:F4').formula=[[strFormular]]
#ws.range("O2").get_address(arg1, arg2, arg3, arg4))
#ws.range("A2:N{row}".format(row=last_row)).api.So

#strFormular="={0}-{1}".format(ws.cells(2,2).address,ws.cells(3,2).address)

#%%
def WritSheet(sheetName,df,wb,idx=False):
    """寫入Excel 傳入 SheetName ,dataFrame, excel workbook , 
    dataframe index default diable """
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
    last_column = ws.range(1,1).end('right').get_address(0,0)[0]
    ws.range('A1:{}1'.format(last_column)).api.Borders(9).LineStyle = -4119

    return ws

def OpenExcel(app,FileName):
    '''開啟 Excel File 不存在就新增 回傳Excel WorkBook'''
    if os.path.isfile(FileName):
        wb = app.books.open(FileName)
        return wb
    else :
        wb = app.books.add()
        wb.save(FileName)
    return wb

def ChangeColor(ws,RowCel,FontColor,BakColor):
    #調整表頭顏色,背景與自行顏色
    print(RowCel)
    ws.range(ws.range(RowCel).expand('right').address).color = rgb_to_int(BakColor)
    ws.range(ws.range(RowCel).expand('right').address).api.Font.Color = rgb_to_int(FontColor)  

def ChangeCellFormat(ws,ColCell,format):
    """更換欄位Format by 欄"""
    ws.range(ws.range(ColCell).expand('down').address).number_format = format
    return ws

def AuotFillRow(ws, cell, last_row):
    'Copy cell 公式往下到最後位置 by 欄'

    rg_cell = ws.range(cell)
    to_fill = "{col}{top_row}:{col}{last_row}".format(
      col=rg_cell.get_address(0,0)[0],
      top_row=rg_cell.row,
      last_row=last_row
    )
    rg_cell.api.Autofill(ws.range(to_fill).api, 0)

def AuotFillCol(ws, cell, last_Col):
    'Copy cell 公式往下到最後位置 by row'

    rg_cell = ws.range(cell)
    to_fill = "{col}{top_row}:{col}{last_Col}".format(
      col=rg_cell.get_address(0,0)[0],
      top_row=rg_cell.row,
      last_Col=last_Col
    )
    rg_cell.api.Autofill(ws.range(to_fill).api, 0)

def ReadSheetToDataFrame(ws):

    return df   

def findCell(ws,columns,strName):
    '''回傳欄位儲存格'''

    for i, colName in enumerate(columns):
        if colName==strName:
            return ws.cells(1,i+1).address
    return 0

def GetSampleDataFrame():
    '假資料方便測試'
    data=[['BEOBA9','34109364866','-17291','WB982CS0078','2.82','2020/01/10'],
    ['BEOBA9','34109364866','-17291','WB982CS0078','2.82','2020/01/10'],
    ['BEOBA10','34109364867','-171','WB982CS0078','1.82','2020/01/11']]
    cols=['UID','NUM1','NUM2','CHAR','DIGT','DATE']

    df=pd.DataFrame(data=data,columns=cols)
    return df

#%%
#Call 聚集測試
app = xw.App(visible=True,add_book=False)
FileName="PythonExcel.xlsm"
wb=OpenExcel(app,FileName)
ws=wb.sheets[0]
myMacro=wb.macro("HelloWorld")
myMacro.run()
#wb.application.xl_app.Run()
wb.save()
wb.close()
app.kill()

#%% Demo Basic
    #https://kknews.cc/code/k6y6yxb.html
app = xw.App(visible=True,add_book=False)
FileName="Demoxlwings.xlsx"
wb=OpenExcel(app,FileName)
df=GetSampleDataFrame()
ws=WritSheet("Demo",df,wb)
ChangeColor(ws,"A1",White,FvlBlue)
wb.save()
#自動儲存格大小
#ws.autofit()
#app.kill()
#app.quit()

#%%


#%% Sheet to DataFrame
df2=ws.range('A1').options(pd.DataFrame,expand='table').value

#%%
CellAddrs=findCell(ws,df.columns,'DIGT')


#%%
ws.api.Rows(1:2).Group

# %%
#rng = sht.range('a1').expand('table') nrows = rng.rows.count

#my_values = Range('Sheet1','A1:A6').options(ndim=2).value 
#Range('Sheet2','A1:A6').value = my_values 


