from django.shortcuts import render,redirect
from django.http import HttpResponse #
from .models import Post #自己定義的資料表
from datetime import datetime

# Create your views here.

def homepage(request):
    posts=Post.objects.all() #讀資料表所有資料
    now=datetime.now()
    return render(request,'index.html',locals()) #locals() 打包所有記憶體變數


def showpost(request,slug):
    try:
        post=Post.objects.get(slug = slug)
        if post !=None:
            #return HttpResponse(slug)
            return render(request,'post.html',locals())
    except:
        return HttpResponse("Err")
        #return redirect('/')
