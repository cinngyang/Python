"""
Web API 架構
Flask Import API_Chip.py
url="http://Server:Port/api/RPTFunction/?Call_Method=XYZ"                       
Method 所需要的參數由 上傳的DataFrame 或 Dictor 提供

"""

import pandas as pd
from LexLib import ConnectDB as cn

#%%SQL
def buInStr(L1):    
    '''SQL list 轉換為 IN'''
    #L1=['123','456','789']
    strIn="','".join(L1)+"'"
    return "('"+strIn+")"

def Get_TapeID(shipmentno):
    ''' WHMS 備貨單取得藍模清單 '''
    
    sSQL=" select b.productno_c,b.productno,b.shipmentno,b.boxid,b.state,b.qty,bd.lotno,bd.qty "
    sSQL+=" from whmsrpt.tblinvboxbasis b, "
    sSQL+=" whmsrpt.tblinvboxdetail bd "
    sSQL+=" where b.shipmentno='"+shipmentno+"'  and b.boxid=bd.boxid " 

    return sSQL

def Get_ShipDate(customerpo):
    '''WHMS 回傳 備貨單 找出貨紀錄'''
    sSQL=" select sh.shipmentno,sh.SONO,sh.customerpo,sh.shippeddate "
    sSQL+=" from whmsrpt.tblinvshipmentbasis sh "
    sSQL+=" where sh.state=3 and sh.shipmentno in "+customerpo
    return sSQL    

def Get_ShipTapeID(boxid='WB98VCS0123'):    
    """--備貨單 -> 箱號 WHMS 箱號取得藍模清單 """

    sSQL=" select b.productno_c,b.productno,b.shipmentno,b.boxid,bd.lotno "
    sSQL+=" from whmsrpt.tblinvboxbasis b, "
    sSQL+=" whmsrpt.tblinvboxdetail bd "
    sSQL+=" where  b.boxid=bd.boxid and b.boxid='"+boxid+"' "
    
    return sSQL

def GetPKG_PO(venders,creation_date='2019/01/01'):
    
    '''取得買回 PKG PO '''
    
    sSQL="select CAST(pha.vendor_id AS varchar(7)) as org,pha.vendor_id,pv.vendor_name,pha.po_header_id,"
    sSQL+="pha.segment1 po_no,TRUNC(pha.creation_date) as creation_date,msi.segment1 as part_no,plla.quantity,"
    sSQL+="plla.quantity_received,plla.quantity_cancelled,"
    sSQL+=" (plla.quantity - nvl(plla.quantity_received, 0) - nvl(plla.quantity_cancelled, 0)) open_po "     
    sSQL+=" from po.po_headers_all  pha, po.po_lines_all  pla, po.po_line_locations_all plla, "
    sSQL+=" po.po_distributions_all  pda, inv.mtl_system_items_b   msi,  inv.mtl_parameters  mp,  po.po_vendors pv"
    sSQL+=" where pha.po_header_id = pla.po_header_id "
    sSQL+=" and pla.po_header_id = plla.po_header_id and pla.po_line_id = plla.po_line_id "
    sSQL+=" and plla.ship_to_organization_id = msi.organization_id "
    sSQL+=" and pla.item_id = msi.inventory_item_id "
    sSQL+=" and pla.po_header_id = pda.po_header_id "
    sSQL+=" and pla.po_line_id = pda.po_line_id "
    sSQL+=" and plla.ship_to_organization_id = mp.organization_id "
    sSQL+=" and pha.creation_date > to_date('"+creation_date+"','yyyy/MM/dd')"
    sSQL+=" and pha.authorization_status IN ('APPROVED', 'INPROCESS', 'REQUIRES REAPPROVAL') "
    sSQL+=" and pda.wip_entity_id is null "
    sSQL+=" and pha.vendor_id in "+venders
    sSQL+=" and pha.vendor_id = pv.vendor_id "
    sSQL+=" and msi.segment1 like '95%' "
    
    return sSQL

def GetModelGroup():
    """取得 PKG Model Group"""
    sSQL=" select distinct l.model_group,l.model_name,l.part_no "
    sSQL+=" from erprpt.vsinv_itf_mtl l "
    sSQL+=" where l.part_no like '95%' "
    return sSQL

def GetPkg_Commit(shift_date):
    sSQL="select c.model_group,c.model_name,c.part_no,c.shift_date,c.qty "
    sSQL+=" from fabods.PKG_OUTSOUR_COMIT c "
    sSQL+=" where version = (select max(version) from fabods.PKG_OUTSOUR_COMIT) "
    sSQL+=" and c.shift_date > to_date('"+shift_date+"','yyyy/MM/dd') "
    return sSQL

#%%[2] 全域變數
dbCon=cn.OracCn()

#%%[2] 函數
def GetOspPkgPo(PO_Date='2019/01/01'):

    PO_Date='2019/01/01' 
    #Vendor Code
    vendor=['2055048', '2568082']
    vends=buInStr(vendor)
    strSql=GetPKG_PO(vends,PO_Date)
    dfPO=dbCon.Exec_OracleCommend(dbCon.LEX_PROD,strSql)  

    strSql=GetModelGroup()
    dfMG=dbCon.Exec_OracleCommend(dbCon.T01HIS1,strSql)  
    dfPO=pd.merge(dfPO,dfMG,how='left',left_on='PART_NO',right_on='PART_NO')
    dfPO['MONTH']=dfPO['CREATION_DATE'].apply(lambda x: x.month)

    col=['ORG', 'VENDOR_ID', 'VENDOR_NAME', 'PO_HEADER_ID', 'PO_NO',
       'CREATION_DATE','MONTH', 'MODEL_GROUP','MODEL_NAME','PART_NO', 'QUANTITY', 'QUANTITY_RECEIVED',
       'QUANTITY_CANCELLED', 'OPEN_PO', 'CHIP', 'UNIT', 'USAGE', ]
    
    dfPO=dfPO.reindex(columns=col)
    
    return dfPO

def GetOspPkgCommit(shift_date='2019/01/01'):
    # 取得 PKG Commit
    
    strSql=GetPkg_Commit(shift_date)
    dfCommit=dbCon.Exec_OracleCommend(dbCon.T05DEV02,strSql) 
    return dfCommit

def GetChinInv(df1):
    
    # 供應商原始表頭處理
    df1=df1.drop(df1.index[0])
    colName={"膜片号":"TypeID","批次号":"Lot","品号":"CPN","数量":"QTY","袋号":'boxid',"采购订单号":'customerpo'}
    df1=df1.rename(columns=colName)

    """ User Upload BlueTape ID"""
    lBoxid=df1['boxid'].unique()
    dfShipNO=pd.DataFrame()
    dbCon=cn.OracCn()

    for i in range(0,len(lBoxid)):
        strSql=Get_ShipTapeID(lBoxid[i])
        dfTemp=dbCon.Exec_OracleCommend(dbCon.C01HIS01,strSql)    
        dfShipNO=dfShipNO.append(dfTemp,ignore_index=True)

    # 備貨單回串目前庫存 - 合併
    df2=pd.merge(df1,dfShipNO,how='left',left_on='TypeID',right_on='LOTNO')  

    columns=['TypeID', 'Lot', 'CPN', 'QTY', '工厂', 'boxid','customerpo', '创建时间', '创建人', 'PRODUCTNO_C','PRODUCTNO', 'SHIPMENTNO','VFMin','VFMax','VFAvg','VFStd','WLDAvg','WLDStd']
    df2=df2[columns]
    # 取得出貨時間 Merge 
    # Call - API
    lpo=df2['SHIPMENTNO'].unique()
    strPo=buInStr(lpo)
    strSql=Get_ShipDate(strPo)
    dfShipDate=dbCon.Exec_OracleCommend(dbCon.C01HIS01,strSql)
    df2=pd.merge(df2,dfShipDate,how='left',left_on='SHIPMENTNO',right_on='SHIPMENTNO') 

    return  df2

def main():    
    pass

def ApiProcess(funName,dfParm=pd.DataFrame()):
    
    """API 傳入funName 參數為 DataFrame"""
    if funName=="GetPkgOspo":
        df=GetOspPkgPo()
        return df
    
    if funName=="GetOspPkgCommit":
        shift_date='2019/01/01'
        df=GetOspPkgCommit(shift_date)
        return df

    if funName=="OspChipInv":
        df=GetChinInv(dfParm)
        return df

    if funName=="UploadOspPkgCommit":
        #待處理
        df=GetChinInv(dfParm)
        return df



if __name__ == "__main__":
    print("RunPyFile")
    main()
else:
    print("Import Modlue")    

#轉譯測試
#Js=dfSour.to_json(orient='table')
#data=json.loads(Js)   
#df = json_normalize(data['data'])
#df.head(2)