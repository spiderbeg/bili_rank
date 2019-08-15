from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages # 弹窗
from django.shortcuts import render

# Create your views here.
from .models import User_info, User, Submits
def rank(request):
	"""知乎粉丝数前100排行"""
	users = User_info.objects.all().order_by('-modify', '-followerCount')[:100]
	return render(request, 'zhihu_rank/zhihu_rank.html', {'users':users})

def save_submit(request):
    '''用户提交知乎数据存储'''
    if request.method == "POST":
        obj, created = Submits.objects.update_or_create(
        url=request.POST['url'], # get
        defaults={'url':request.POST['url']} # update
    )
    return redirect('zhihu_rank:rank')