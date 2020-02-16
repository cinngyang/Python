#%%
from LexLib import ConnectDB
import pandas as pd 
from flask import Flask, render_template, flash, redirect, url_for,Markup,request,jsonify
from flask_wtf import FlaskForm
from wtforms import SelectField
from flask_cors import CORS
import os

#%%
class City():
    id=[1,2,3]
    state=['CA','NV']
    name=['California','Nevada']

class Form(FlaskForm):

    state=SelectField(label='state',choices=[('CA','California'),('NV','Nevada')]) 
    city=SelectField(label='city',choices=[])


app=Flask(__name__)
CORS(app)
app.config['SECRET_KEY']='secret'


@app.route('/',methods=['Get','POST'])
def index():
    form=Form()    
    citys=pd.DataFrame(data=[[1,'Las Vegas'],[2,'Reno'],[3,'Log Angeles'],[4,'San Diego']],columns=['id','name']) 
    val=list(zip(citys.id, citys.name))
    form.city.choices=val
    
    if request.method == 'POST':
        return '<h1>state:{0} city{1}'.format(form.state.data,form.city.data)

    return render_template('app_form.html',form=form)

@app.route('/city/<state>',methods=['Get'])
def city(state):

    citys=pd.DataFrame(data=[[1,'CA','Las Vegas'],
    [2,'CA','Reno'],[3,'NV','Log Angeles'],
    [4,'NV','San Diego']],columns=['id','state','name'])
    
    citys=citys.loc[citys['state']==state]   
    citys=citys.reset_index(drop=True)  
     
    citArray=[]
    for i in range(citys.shape[0]):
        cityobj={}
        cityobj['id']= str(citys.loc[i,'id'])
        cityobj['name']= citys.loc[i,'name']
        citArray.append(cityobj)

    return jsonify({'cities':citArray})


if __name__=='__main__':
    app.run(port=8000,debug=True)




