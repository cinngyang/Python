#%%
import pandas as pd
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

#%%
def plot_clustered_stacked(dfall, labels=None, title="BU Summary",  H="/", **kwargs):
    """Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot. 
labels is a list of the names of the dataframe, used for the legend
title is a string for the title of the plot
H is the hatch used for identification of the different dataframe"""

    n_df = len(dfall)
    n_col = len(dfall[0].columns) 
    n_ind = len(dfall[0].index)
    axe = plt.subplot(111)

    for df in dfall : # for each data frame
        axe = df.plot(kind="bar",
                      linewidth=0,
                      stacked=True,
                      ax=axe,
                      legend=False,
                      grid=True,
                      **kwargs)  # make bar plots

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                rect.set_hatch(H * int(i / n_col)) #edited part     
                rect.set_width(1 / float(n_df + 1))

    axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
    axe.set_xticklabels(df.index, rotation = 0)
    axe.set_title(title)
    #plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places
    axe.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places


    # Add invisible data to add another legend
    n=[]        
    for i in range(n_df):
        n.append(axe.bar(0, 0, color="gray", hatch=H * i))

    l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5])
    if labels is not None:
        l2 = plt.legend(n, labels, loc=[1.01, 0.1]) 
    axe.add_artist(l1)
    return axe

#%%
'Load Excel'

xls=pd.ExcelFile('LB_Summary.xlsx')
FCST=pd.read_excel(xls,'FCST')
SO=pd.read_excel(xls,'SO')
Commit=pd.read_excel(xls,'Commit')
Shipped=pd.read_excel(xls,'Shipped')

FCST=FCST.set_index('MONTH')
SO=SO.set_index('MONTH')
Commit=Commit.set_index('MONTH')
Shipped=Shipped.set_index('MONTH')


#%%
'Monthly'
plt.style.use('ggplot')
plot_clustered_stacked([FCST,SO, Commit,Shipped],['FCST', 'SO', 'Commit','Shipped'],title="LB BU Summary")


#%%
FCST_W=pd.read_excel(xls,'FCST_W')
SO_W=pd.read_excel(xls,'SO_W')
Commit_W=pd.read_excel(xls,'Commit_W')
Shipped_W=pd.read_excel(xls,'Shipped_W')


#%%

#%%

fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot( 'Weekly', 'FCST', data=FCST_W, marker='', markerfacecolor='blue', markersize=1, color='skyblue', linestyle='dashed',linewidth=2)
ax.plot( 'Weekly', 'SO', data=SO_W, marker='', color='olive', linewidth=2)
ax.plot( 'Weekly', 'Commit', data=Commit_W, marker='', color='indigo', linewidth=2, linestyle='dashed' )
ax.plot( 'Weekly', 'Shipped', data=Shipped_W, marker='o', color='red',markerfacecolor='red', linewidth=2  )
ax.set_ylabel('Rev')
ax.legend(loc='best')
plt.grid(True)
plt.title("Jul LB Summary")
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places


#%%


#%%
