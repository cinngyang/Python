import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
#load file
MONO=pd.read_csv("C:/Data/GitHub/Python/SampleFile/MONO.csv")
MixWT=pd.read_csv("C:/Data/GitHub/Python/SampleFile/MixWT.csv")

P3806=MixWT[MixWT["PRODUCTNO"]=="95.S3806.W0A0C8Z"]
MONO.set_index('MONO')
P3806.set_index('MONO')
MONO=pd.DataFrame(MONO)
P3806=pd.DataFrame(P3806)
P3806=pd.merge(P3806,MONO,how='left',left_on='MONO',right_on='MONO')
P3806.shape
P3806.groupby('WDD').size()
P3806=P3806[P3806['WDD']=='452.5-450']
P3806.to_csv("C:/Data/GitHub/Python/SampleFile/SideView.csv")

SiV=pd.read_csv("C:/Data/GitHub/Python/SampleFile/SideView.csv")
DataSet=SiV[["WT","SPC_VALUE", "SPC_RANGE", "PRE_CIE_X_AVG", "PRE_CIE_Y_AVG", "CIE_X_AVG", "CIE_Y_AVG"]]
X=SiV.loc[:,"WT"]
Y=SiV.loc[:,"CIE_X_AVG"]
X_Train,X_Test,Y_Train,Y_Test=train_test_split(X,Y,test_size=0.2,random_state=0)
#feature select
#
regressor=LinearRegression()
regressor=regressor.fit(X=X_Train,y=Y_Train)
y_pred=regressor.predict(X=X_Test)

plt.scatter(X_Train, Y_Train, color = 'red')
plt.plot(X_Train, regressor.predict(X_Train), color = 'blue')
plt.title('Salary vs Experience (Training set)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()
