Django 1.10 環境設定

***

環境設定

+ conda create --name MyDjangoEnv python=3.6
+ conda activate MyDjangoEnv
+ conda install Django=1.10

Django 設定

+ Change Direction
  + C:\Data\GitHub\Python\My_Django_Stuff
+ Add Atom Project Folder
+ Activate conda & setup Project & App
  + conda activate MyDjangoEnv
  + Django-admin startproject first_project
  + python manage.py startapp first_app
  + python manage.py runserver (路徑)

![DjangoStruct](img\DJStruct.jpg)

![FileStruct](img\DjangoFolder.jpg)

+ settingg.py
+ urls.py
+ wsgi.py(Web Server Getway Interface)
  + deploy web app
+ + midify setting.py INSTALLED_APPS  add 'first_app'
+ Add Views

