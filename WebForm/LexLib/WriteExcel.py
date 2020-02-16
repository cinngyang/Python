

import pandas as pd
import xlsxwriter 
from xlsxwriter.utility import xl_rowcol_to_cell,xl_cell_to_rowcol
from datetime import datetime


class HtmlPnadas():
    
    Number_format='{:,.0f}'
    Pertange_format='{:.2%}'    
    
    def __init__(self):
        
        self.Number_format='{:,.0f}'
        self.Pertange_format='{:.2%}'     
        
    def magnify(self):
        '''Html 表頭紅底白字'''
        return [dict(selector="th",props=[("background-color", "red"),("font-family", "Calibri"),('color','white')])]
    
        
    def ModifyFormat(self,df,cell_chFormat={}):   
        ''' '''
        df=df.style.hide_index()
        df=df.set_properties(**{'border':'1px solid white','font-family':'Calibri',
                           'text-align': 'right',
                           'background-color': 'rgb(211, 211, 211)'})
        df=df.format(cell_chFormat).set_table_styles(magnify())
        
        return df

        

class WriteExcel():
    
    FileName='LexIT'+datetime.now().strftime('%Y%m%d')+'.xlsx'
    cell_Header=xlsxwriter.format
    cell_format_Number=xlsxwriter.format
    cell_fron=xlsxwriter.format
    workbook=xlsxwriter.Workbook()
        
    def __init__(self,FileName=""): 
        
        if FileName=="" :
            FileName='LexIT'+datetime.now().strftime('%Y%m%d')+'.xlsx'

        self.workbook = xlsxwriter.Workbook(FileName)
        self.FileName=FileName
        
        # Head Format
        self.CelHead_LexRed={'bold': True,'italic':False,'bg_color':'#C61031','font_name':'Calibri','font_color':'#FFFFFF'}
        self.CelHead_LexBlue={'bold': True,'italic':False,'bg_color':'#0E20D0','font_name':'Calibri','font_color':'#FFFFFF'}
        self.CelHead_FVLBlue={'bold': True,'italic':False,'bg_color':'#005AA0','font_name':'Calibri','font_color':'#FFFFFF'}
        
        # Raw Format
        self.cell_fron=self.workbook.add_format({'font_color':'#000000'})
        self.cell_format_Number = self.workbook.add_format({'num_format':"#,##0;[red](#,##0)"})
        self.cell_format_Pertange = self.workbook.add_format({'num_format':0x0a})        
        
        # 紅底白字
        self.cell_Date=self.workbook.add_format({'num_format':'mm/dd','bg_color':'#C61031',
                                                 'font_color':'#FFFFFF','bold': True,'italic':False})        
        #正常
        self.cell_NorDate=self.workbook.add_format({'num_format':'mm/dd','bold': True,'italic':False})     
        
        # Excel Format
       
        self.cell_Header = self.workbook.add_format(self.CelHead_LexRed)
        self.cell_Header.set_align('center')
        self.cell_Header.set_text_wrap()
        self.cell_Header.set_font_family
        self.cell_Header.set_shrink()      

    def WiteLog(self,Msg):
        """Write Log""" 
        fileName="Err_"+datetime.now().strftime('%Y%m%d')+".err"
        with open(fileName,'a',encoding='utf-8') as fi:
            Msg=datetime.now().strftime('%Y%m%d %H:%M:%S')+","+Msg+"\n"
            fi.write(Msg)  
            fi.close()

    def Chage_RawFormat(self,df,Raw=0 , cell_chFormat={}):        
        '''填入定義 Fomrat  CelHead_LexRed CelHead_LexBlue ...., '''
        
          
    
    # Default Foramt
    def AddSheet(self,df,sheetName='sheet1',cell_chFormat={}):
        """新增 Sheet  cell_chFormat default """
        # Header
        # Columns Mapping Format
        try:

            worksheet = self.workbook.add_worksheet(sheetName)       

            #Header
            for col_num, value in enumerate(df.columns.values):
            
                row=0
                cName=xl_rowcol_to_cell(row,col_num+1)
                style=self.cell_Header                
                worksheet.write(cName, value, style)

            #RawData , row=df.shape[0] ,  col=df.shape[1]
            for col in range(0,df.shape[1]):
                
                #是否要更換格式            
                if (df.columns[col] in cell_chFormat):
                    style=cell_chFormat[df.columns[col]]
                else:
                    style=self.cell_fron                
            
                for row, value in enumerate(df.iloc[:,col]):
                    cName=xl_rowcol_to_cell(col,row+1)
                    worksheet.write(row+1,col+1, value,style)
        
        except Exception as err:
            print("Add Sheet Err", str(err))
            msg="Add Sheet Err"+str(err)
            self.WiteLog(msg)
            return msg            
                
    # Change Header Foramt
    def AddSheetChForm(self,df,sheetName='sheet1',Head_chFormat={},Raw_chFormat={}):
        """表頭與表身格式不同 dic 填入需要替換的欄位名稱與格式"""
        # Header
        # Columns Mapping Format
        
        worksheet = self.workbook.add_worksheet(sheetName)

        #Header
        try :

            for col_num, value in enumerate(df.columns.values):
            
                row=0
                cName=xl_rowcol_to_cell(row,col_num+1)
            
                if (value in Head_chFormat):
                    style=Head_chFormat[value]
                else :
                    style=self.cell_Header

                worksheet.write(cName, value, style)
                

        #RawData , row=df.shape[0] ,  col=df.shape[1]
            for col in range(0,df.shape[1]):
            
                if (df.columns[col] in Raw_chFormat):
                    style=Raw_chFormat[df.columns[col]]
                else:
                    style=self.cell_fron                
            
                for row, value in enumerate(df.iloc[:,col]):
                    cName=xl_rowcol_to_cell(col,row+1)
                    worksheet.write(row+1,col+1, value,style)     
        
        except Exception as err:
            print("AddSheetChForm Header Err", str(err))
            msg="Add AddSheetChForm Header Err"+str(err)
            self.WiteLog(msg)
            return msg        
        
    def Close(self):
        self.workbook.close()
        
        
    

