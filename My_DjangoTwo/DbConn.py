import pandas as pd

class MyConn:
       __T01HIS1='T01HIS'
       __T01cn=''
    def __init__(self):
        dbconf=pd.read_csv("C:\Data\GitHub\Python\SampleFile\dbconf.csv")
        dbconf=pd.DataFrame(dbconf)
        sleft.__T01cn=dbconf[dbconf['Server']==__T01HIS1]

    def T01HisCn(selft):
        return sleft.__T01cn

    orc=MyConn()

    orc.T01HisCn
