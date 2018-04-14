# Python
Python 學習<br>
Django (Django 2.0.4/SQLite)<br>
pip install django<br>
Step 1: PS C:\Data\Web> easy_install django (using winfown+x & chaned to file path) <br>
step 2: django-admin --version (testing) <br>
step 3: django-admin startproject mysite <br>
step 4: change to user website dir <br>
step 4.1 modify time zone (settings.py / LANGUAGE_CODE = 'zh-hant' TIME_ZONE = 'Asia/Taipei' ) <p>
  
step 5: C:\Data\Web\mysite> python manage.py runserver <p>
step 6: create app<br>
C:\Data\Web\mysite>python manage.py startapp polls <br>
step 7: Write View  polls/views.py<br>
step 8: setup url link to view polls/url.py<br>
step 9: setup url link mysite/url.py <br> 
