import pandas as pd
import matplotlib.pyplot as plt
from ggplot import *
import seaborn as sns

MONO=pd.read_csv("C:/Data/GitHub/Python/SampleFile/MONO.csv")
MixWT=pd.read_csv("C:/Data/GitHub/Python/SampleFile/MixWT.csv")
MONO.info()
MixWT.info()
MixWT.groupby('PRODUCTNO').size().sort_values(ascending=False).head(1)
MixWT.loc[lambda MixWT: MixWT.CIE_Y_AVG > 0.2 ,['CIE_X_AVG','CIE_Y_AVG']].head(2)

P3806=MixWT[MixWT["PRODUCTNO"]=="95.S3806.W0A0C8Z"]
P3806.columns
P3806.shape
MONO.shape
MONO.columns

MONO.set_index('MONO')
P3806.set_index('MONO')

P3806=pd.DataFrame(P3806)
P3806.info()

P3806[['WDD', 'PRODUCT_NO']] = P3806[['WDD', 'PRODUCT_NO']].astype(str)
plt.scatter(P3806["CIE_X_AVG"],P3806["CIE_Y_AVG"],c='r')
plt.show()

P3806.groupby('WDD').count()

ggplot(aes(x='CIE_X_AVG',y='CIE_Y_AVG',color='WDD'),data=P3806) +\
geom_point() +\
scale_color_brewer(type='diverging', palette=4)
P3806.columns
#Index('RUN_SEQ', 'WT', 'GR','SPC_VALUE', 'SPC_RANGE', 'PRE_CIE_X_AVG', 'PRE_CIE_Y_AVG', 'CIE_X_AVG','CIE_Y_AVG',

P3806=P3806[P3806["WDD"]=="452.5-450"]
P3806.shape
P3806=P3806[['WT',,'SPC_VALUE', 'SPC_RANGE', 'PRE_CIE_X_AVG', 'PRE_CIE_Y_AVG', 'CIE_X_AVG','CIE_Y_AVG']]
P3806Cor=P3806.corr()
P3806Cor.shape
plt.subplots(figsize=(7, 7))
sns.heatmap(P3806Cor, annot=True, vmax=1, square=True, cmap="Blues")
