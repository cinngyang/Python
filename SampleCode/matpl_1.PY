#%%
import pandas as  pd 
import matplotlib.pyplot as plt
import seaborn as sns

#%%
fileNmae="HitRateSummary.xlsx"
dfPkg=pd.read_excel(fileNmae)
dfPkg.columns

#%%
'找中文字型檔安裝位置'
#https://medium.com/marketingdatascience/%E8%A7%A3%E6%B1%BApython-3-matplotlib%E8%88%87seaborn%E8%A6%96%E8%A6%BA%E5%8C%96%E5%A5%97%E4%BB%B6%E4%B8%AD%E6%96%87%E9%A1%AF%E7%A4%BA%E5%95%8F%E9%A1%8C-f7b3773a889b
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
'圖檔參數'

nyc_chart = sns.lineplot(x="Month",y="Rev",hue="Item",data=dfPkg)
nyc_chart.set_title('營收')
#nyc_chart.savefig("Rev.jpg")
fig= nyc_chart.get_figure()
fig.savefig('Rev.jpg')
#%%

#%%
'多圖'
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
'圖檔參數'
fig , axex=plt.subplots(1,2)
axex[0].hist(data=dfPkg,x="Rev")
axex[0].set_title('營收')
axex[1]=sns.lineplot(x="Month",y="Rev",hue="Item",data=dfPkg)
axex[1].set_title('營收')


#%%
sns.lineplot(x="Month",y="Rev",hue="Item",data=dfPkg)

#%%
