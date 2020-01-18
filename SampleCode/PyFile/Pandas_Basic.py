#%%
import pandas as pd 

#%%
FiExcel='C:/Data/GitHub/Python/SampleFile/Bintable.xlsx'
dfExcel=pd.read_excel(FiExcel)
#%%
# 觀察資料
# 觀察資料 
print('列出有幾筆資料與幾欄',dfExcel.shape) 
print('列出所有欄位',dfExcel.columns)
print('列出所有欄位',dfExcel.info())
print('列出所有欄位',dfExcel.describe())






#%%
