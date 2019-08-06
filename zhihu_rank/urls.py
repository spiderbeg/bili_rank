from django.urls import path
from . import views

app_name = 'zhihu_rank' # 你的应用名

urlpatterns = [
    path('', views.rank, name='rank'),
    path('submits/', views.save_submit, name='save_submit'),
    ]