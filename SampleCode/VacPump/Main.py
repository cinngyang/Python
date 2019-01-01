#%%
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from bokeh.io import output_file, show
from bokeh.plotting import figure
from scipy.fftpack import fft,ifft

#%%
raw=pd.read_csv('K00.csv')


p = figure(title="simple line example", 
              x_axis_label='x', 
              y_axis_label='y')

p.line(range(13000),raw[['PREASSURE']].head(13000),
 legend="PREASSURE", line_width=2)
output_file("lines.html")
show(p)

#%%
y=raw['PREASSURE'].values

yy=fft(y)                     #快速傅里叶变换
yreal = yy.real               # 获取实数部分
yimag = yy.imag               # 获取虚数部分

plt.scatter(data=raw,x=range(65535),y=yimag)

