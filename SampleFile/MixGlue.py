import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ggplot import *
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression


dtmono=pd.read_csv("D:\AP\PythonLen\MixGule\MONO.csv")
dtMixGlue=pd.read_csv("D:\AP\PythonLen\MixGule\GlueD.csv")

# 半年內前側資料
dtmono=pd.DataFrame(dtmono)
dtMixGlue=pd.DataFrame(dtMixGlue)
dtMixGlue.info()
dtMixGlue.groupby('PRODUCTNO').size().sort_values(ascending=False).head(2)
#PRODUCTNO
#95.S3806.W0A0C8Z    1200

dtSiVi=dtMixGlue[dtMixGlue['PRODUCTNO']=='95.S3806.W0A0C8Z']
dtSiVi=dtSiVi[['MONO','WT','SPC_VALUE','SPC_RANGE','PRE_CIE_X_AVG','PRE_CIE_Y_AVG','CIE_X_AVG','CIE_Y_AVG']]
dtSiVi=dtSiVi.dropna()
dtSiVi=dtSiVi.merge(dtmono,how='left',left_on='MONO',right_on='MONO')
dtSiVi.groupby('WDD').size()

dtSiVi[['WDD','MONO']] = dtSiVi[['WDD','MONO']].astype('str')
dtSiVi[['PRE_CIE_Y_AVG']] =dtSiVi[['PRE_CIE_Y_AVG']].astype('float64')
dtSiVi.info()

ggplot(aes(x='PRE_CIE_X_AVG', y='PRE_CIE_Y_AVG'), data=dtSiVi) +\
geom_point() +\
geom_point(aes(x='CIE_X_AVG', y='CIE_Y_AVG'), data=dtSiVi) +\
ggtitle('95.S3806.W0A0C8Z')

ggplot(aes(x='CIE_X_AVG', y='CIE_Y_AVG',color='WDD'), data=dtSiVi) +\
geom_point() +\
ggtitle('95.S3806.W0A0C8Z')
dtSiVi['CIE_X_GAP']=dtSiVi['CIE_X_AVG']-dtSiVi['PRE_CIE_X_AVG']
dtSiVi['CIE_Y_GAP']=dtSiVi['CIE_Y_AVG']-dtSiVi['PRE_CIE_Y_AVG']
dtCor=dtSiVi[dtSiVi['WDD']=='452.5-450']
dtSiVi=dtSiVi[dtSiVi['WDD']=='452.5-450']
dtCor.shape
dtCor=dtCor[['WT','SPC_VALUE','SPC_RANGE','PRE_CIE_X_AVG','PRE_CIE_Y_AVG','CIE_X_AVG','CIE_Y_AVG','CIE_X_GAP','CIE_Y_GAP']].corr()
dtCor

plt.subplots(figsize=(9, 9))
sns.heatmap(dtCor, annot=True, vmax=1, square=True, cmap="Blues")

dtSiVi.describe()



ggplot(aes(x='WT',y='CIE_X_AVG'),data=dtSiVi)+\
geom_point()+ \
theme(axis_text_x = element_text(angle = 90, hjust = 1))


ggplot(aes(x='CIE_X_AVG',y='CIE_Y_AVG'),data=dtSiVi)+\
geom_point()+ \
theme(axis_text_x = element_text(angle = 90, hjust = 1))


X=dtSiVi[['CIE_X_AVG']]
y=dtSiVi[['CIE_Y_AVG']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 0)
regressor = LinearRegression()
regressor.fit(X_train, y_train)
y_pred= regressor.predict(X_test)
RSquare=regressor.score(y_pred,y_test)
RSquare
y_pred=pd.DataFrame.from_records(y_pred,columns=['y_pred'])
X_test=X_test.reset_index()
X_test.drop('index', axis=1, inplace=True)
y_test=y_test.reset_index()
y_test.drop('index', axis=1, inplace=True)

dtResult=pd.concat([X_test,y_test,y_pred],axis=1,ignore_index=True)
dtResult.shape
dtResult.columns=['X_test','y_test','y_pred']

ggplot(aes(x='X_test',y='y_test'),data=dtResult)+\
geom_point(aes(color='blue'))+\
geom_point(aes(x='X_test',y='y_pred',color='red'))

dtSiVi.shape
X=dtSiVi[['WT']]
y=dtSiVi[['CIE_X_AVG']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 0)
regressor = LinearRegression()
regressor.fit(X_train, y_train)
y_pred= regressor.predict(X_test)
RSquare=regressor.score(y_pred,y_test)
RSquare
y_pred=pd.DataFrame.from_records(y_pred,columns=['y_pred'])
X_test=X_test.reset_index()
X_test.drop('index', axis=1, inplace=True)
y_test=y_test.reset_index()
y_test.drop('index', axis=1, inplace=True)

dtResult=pd.concat([X_test,y_test,y_pred],axis=1,ignore_index=True)
dtResult.shape
dtResult.columns=['X_test','y_test','y_pred']

ggplot(aes(x='X_test',y='y_test'),data=dtResult)+\
geom_point(aes(color='blue'))+\
geom_line(aes(x='X_test',y='y_pred',color='red'))
