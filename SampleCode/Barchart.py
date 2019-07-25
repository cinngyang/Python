#%%
import pandas as pd 
import numpy  as np 
import matplotlib.pyplot as plt
import seaborn as sns




#%%
df=pd.read_excel('Data.xlsx')
df

#%%
ax = df.plot.bar(x='CATEGORY', y='S1', rot=0)

#%%
Commit = [0.1, 17.5, 40, 48, 52, 69, 88]
SO = [2, 8, 70, 1.5, 25, 12, 28]
index = ['6', '7', '8','9', '10', '11', '12']
df2 = pd.DataFrame({'Commit': Commit,'SO': SO}, index=index)
df2
ax = df2.plot.bar(rot=0)


#%%
A1 = [0.1, 17.5, 40, 48, 52, 69, 88]
A2 = [2, 8, 70, 1.5, 25, 12, 28]
index = ['6', '7', '8','9', '10', '11', '12']
df3 = pd.DataFrame({'A1': A1,'A2': A2}, index=index)
df3
ax = df3.plot.bar(stacked=True)


#%%
df2


#%%
