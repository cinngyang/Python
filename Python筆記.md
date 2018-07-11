基本演算法

+ 線性迴歸
  + Sample-linear Regression
+ Logistic 迴歸
+ 貝氏分類器
+ 降維

seaborn 熱力圖
+ plt.subplots(figsize=(9, 9))
+ sns.heatmap(dtCor, annot=True, vmax=1, square=True, cmap="Blues")

+ Pandas
  + P3806[['WDD', 'PRODUCT_NO']] = P3806[['WDD', 'PRODUCT_NO']].astype(str)
  + MixWT.groupby('PRODUCTNO').size().sort_values(ascending=False).head(1)
  + MixWT.loc[lambda MixWT: MixWT.CIE_Y_AVG > 0.2 ,['CIE_X_AVG','CIE_Y_AVG']]
  + P3806=pd.merge(P3806,MONO,left_on = 'MONO',right_on = 'MONO',how="left")
  + P3806=P3806.dropna(axis='rows')
  + pd.DataFrame.from_records(y_pred,columns=['y_pred'])
  + X_test.reset_index()
  + pd.concat([X_test,y_test,y_pred],axis=1,ignore_index=True)

參考資料<br>[Keras深度學習簡介-林大貴](http://tensorflowkeras.blogspot.tw/2017/08/keras.html)<br>
[pandas](https://pandas.pydata.org/pandas-docs/stable/tutorials.html)<br>[Pandas-join](https://hk.saowen.com/a/13653e06de99e095fc9e1a4d2bba43489e16033380dd00b6dad9b25748eb2ce1)<br>[python_ggplot](http://ggplot.yhathq.com/)<br>
