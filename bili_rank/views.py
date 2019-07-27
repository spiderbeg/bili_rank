from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages # 弹窗
from .models import User_info, Submits # 模型导入
import time

# Create your views here.

def rank(request):
    '''哔哩哔哩粉丝数前 100 名排行'''
    users = User_info.objects.all().order_by('-lastmodify', '-follower_count')[:100]
    return render(request, 'bili_rank/rank.html', {'users':users})

def save_submit(request):
    '''用户提交 up主 数据存储'''
    if request.method == "POST":
        obj, created = Submits.objects.update_or_create(
        url=request.POST['url'], # get
        defaults={'url':request.POST['url']} # update
    )
    return redirect('bili_rank:rank')