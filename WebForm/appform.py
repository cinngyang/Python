#%%
from flask import Flask, render_template,flash, redirect, url_for
from flask_cors import CORS
from LexLib import ConnectDB
import forms
import os

#%%
app=Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
CORS(app)

@app.route('/')
def basic():
    form = forms.BaseForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        print(username)
        return redirect(url_for('index'))
    return render_template('SampleForm.html', form=form)

@app.route('/Form')
def SelectForm():
    form = forms.SelectForm()    
    
    if form.validate_on_submit():
        #summit 處理
        modelGroup=form.modelGroup.values
        print()
        return redirect(url_for('index'))




if __name__=='__main__':
    app.run(port=8000,debug=True)

