
#%%
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt


def SetChinese():
    '''尋找字型檔安裝位置, 下載自型檔微軟正黑體 命名為msj.ttf'''
    """http://cloud.ziti8.cn/fonts/weiruan/%E5%BE%AE%E8%BD%AF%E6%AD%A3%E9%BB%91%E4%BD%93.ttf"""
    #find  matplotlib default font
    from matplotlib.font_manager import findfont, FontProperties  
    strPath=findfont(FontProperties(family=FontProperties().get_family()))
    return strPath

def FindPath():
    """尋找設定檔"""
    import matplotlib 
    strPath=matplotlib.matplotlib_fname()
    """font.family  解除註解"""
    """font.sans-serif : Microsoft JhengHei 新增"""    

    return strPath

def Sample(): 
    '''設定使用自型'''   
    myfont = FontProperties(fname=r'C:\ProgramData\Anaconda3\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\msj.ttf')
    plt.plot((1,2,3),(4,3,1)) 
    plt.title("聲量圖",fontproperties=myfont) 
    plt.ylabel("文章數量",fontproperties=myfont) 
    plt.xlabel("時間",fontproperties=myfont)  
    plt.show()

def Line():

#%%
if __name__ == "__main__":
    pass

#%%
myfont = FontProperties(fname=r'C:\ProgramData\Anaconda3\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\msj.ttf')





# %%
plt.plot((1,2,3),(4,3,1)) 
plt.title("聲量圖",fontproperties=myfont) 
plt.ylabel("文章數量",fontproperties=myfont) 
plt.xlabel("時間",fontproperties=myfont)  
plt.show()

# %%
