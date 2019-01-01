# Python
Python 學習
+ [Class](/SampleCode/ClassMethod.ipynb) 
+ [基本資料操作](/SampleCode/Python資料結構.ipynb)
+ [Pandas](/Python-Pandas.ipynb/)
+ [LinearRegressor](LinearRegressor1.ipynb)
+ [matplotlib](/matplotlib.ipynb/)

***

當發現也有 python ggplot真的很高興<br>
$conda install -c conda-forge ggplot<br>

atom 使用不同conda 環境
source activate thisenv
python -m ipykernel install --user --name thisenv

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
step 9: setup url link mysite/url.py <p>

setup database<br>
C:\Data\Web\mysite>python manage.py migrate<br>
C:\Data\Web\mysite>python manage.py createsuperuser<br>
Create dataTable(Create model comment)
C:\Data\Web\mysite>python manage.py makemigrations
C:\Data\Web\mysite>python manage.py migrate
