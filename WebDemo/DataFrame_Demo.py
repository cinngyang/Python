#DataFrame 操作


#%%
import pandas as pd 
import xlwings as xw 
import numpy as np 
from datetime import datetime 



# %%
data = [['95.C3528.HAB00MZ','INV',100], ['95.C3528.UAD002Z', 'BOH',20]] 
data2 = [['95.C3014.HBB037Z','Commit',60], ['95.C3528.UAD002Z', 'Summary',10]] 

dfS=pd.DataFrame(data,columns = ['PartNo', 'Parameters','Values'])
dfM2=pd.DataFrame(data2,columns = ['PartNo', 'Parameters','Values'])

dfRes=pd.concat([dfS, dfM2], ignore_index=True)
dfRes
# %%
Part=dfRes['PartNo'].unique()
Parameters=dfRes['Parameters'].unique()


# %%
cols=["PartNo", "Parameters", "Flag"]
dfRes2=pd.DataFrame(columns = cols)

for i in Part:
    for j in Parameters:
        dfRes2=dfRes2.append(pd.DataFrame(data=[[i,j,1]]
        ,columns=cols),ignore_index=True)
    
    print(i,j)

# %%
dfRes3=pd.concat([dfRes2, dfRes], ignore_index=True)
dfRes3

# %%
