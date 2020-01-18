#基本操作
#https://www.twblogs.net/a/5b8285fb2b717766a1e8aca8
#lwings 可使用 pywin32 功能
#https://www.kancloud.cn/gnefnuy/xlwings-docs/1127474

#%%
import xlwings as xw
from xlwings.utils import rgb_to_int
import pandas as pd 
import numpy as np

# %%

app = xw.App(visible=True,add_book=True)
wb = xw.books.add() #新建一张workbook
sht = wb.sheets.add(name="Data")  #新建一张sheet
wb.app.visible=True

# %%
sht.range('A1').value=1
sht.range('A1').value=2
sht.range('C1').formula="=A1+C1"
sht.range('C1').formula="=A1+C1"

# %%
xw.sheets[0].range('A1:A5').value = [[i] for i in range(5)]
xw.sheets[0].range('B1:C5').formula = [['=A1+1','=B1*10']]
xw.sheets[0].range('A1:C5').value
#Cell Color
xw.sheets[0].range('A1:C5').api.Font.Color = rgb_to_int((20, 20, 255))
xw.sheets[0].range('B1:C1').color = rgb_to_int((20, 20, 255))

#%%
# formula
ws=xw.sheets[0]
rng_to_paste = ws.range('C1').options(ndim=1).formula
ws.range('D1').options(ndim=1).formula = rng_to_paste

# %%
# 加入超鏈接
sht=xw.sheets[1]
sht.range('A1').value = [[1,2], [3,4]]
rng1 = sht.range('A1').options(expand='table', transpose=True).value
rng1 = sht.range('B1')
rng1.add_hyperlink('www.baidu.com','百度','提示：點擊即鏈接到百度')

# %%
type(xw.sheets[0].range('A:B').api.Group)
#xw.sheets[0].range('A:B').api.OutlineLevel = 2

# %%
df = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
ax = df.plot(kind='bar')
fig = ax.get_figure()
xw.sheets[2].pictures.add(fig, name='MyPlot', update=True,
left=xw.sheets[2].range('B5').left, top=xw.sheets[2].range('B5').top)

# %%
