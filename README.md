# 哔哩哔哩及知乎大 V 排行榜
## 项目内容
* 分别抓取哔哩哔哩及知乎粉丝数前 100 的用户，并按照粉丝数数量进行排名；保证抓取用户排行代码的可更新，定时更新排行榜。最后部署在服务器上，将排名数据用网页的形式展现出来。
## 项目思路
1. 分别分析哔哩哔哩及知乎用户页面，使用 **scrapy** 获取尽可能全的用户粉丝数信息（1、本次用户数据参考我的另外两个关于哔哩哔哩及知乎的数据分析的项目；2、哔哩哔哩抓取2019年六月前播放数超 50w 视频UP主信息3755位；3、知乎从大v张佳玮开始抓取关注用户粉丝数过 1w 的用户共计9385人），使用**mongodb** 储存数据。将各站（后面用各站分别表示哔哩哔哩及知乎两个网站）粉丝数前 100 的用户进行排名；
2. 在获取到可信的各站前 100 排名信息后，就可以根据各站排名信息，来对前 100 用户排名更新，更新时：在不考虑高精度的及时性
的情况下（数据库使用 **mysql** ，数据更新时使用 django 自带的 **queyset API**），在更新中选择了更新前 100 用户信息并对各前 100 用户关注用户粉丝数抓取比较（哔哩哔哩限定只显示关注用户**前5页**），来对各站排行榜的用户信息进行更新。定时更新使用 Linux 的 **crontab** 命令。
3. 使用 django 创建网站并部署到服务器上，前端页面排名使用表格的形式展示出来的，使用了 Datatables（一款基于jQuery的表格插件），使用很方便。 
## 运行环境
* python3.7
* Windows/Linux
* jupyter notebook
* mongodb/mysql
## 运行依赖包
* requests
* scrapy
* pymongo
* pymysql
* django
## 如何跑起来
1. 这里展示本地如何跑起来，确定好放置项目位置

        git clone https://github.com/spiderbeg/bili_rank.git
2. 打开控制台，进入与 **manage.py 同级目录**，注意这里需要自己先在 **rank/settings.py**文件中配置一下MySQL，注意**数据库名，用户名，密码**要使用自己的。并且在MySQL中创建数据库；
        
        # 1 settings.py 配置MySQL
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'bili', # 数据库名
                'USER': 'root', # 用户名
                'PASSWORD': 'pythonbegin1', # 密码
                'HOST': 'localhost',
                'PORT': '3306',
                'OPTIONS':{
                'charset':'utf8mb4',
                }
            }
        }
        # 2 命令行中执行
        python manage.py migrate # 为应用创建数据表
3. 将初始各站粉丝数前 100 用户数据导入 MySQL 数据库, 文件名 bili_rakn.sql 及 zhihu.sql

        # root：用户名，bili：数据库名，database.sql：数据库文件名(文件名 bili_rakn.sql 及 zhihu.sql)
        mysql -u root -p -d bili < database.sql
4. 开始运行排行项目, 进入 manage.py 同级项目
        
        # 打开浏览器输入 http://127.0.0.1:8000/bili_rank/ 就可以查看网页了
        python manage.py runserver
5. 数据定时更新
* 在 linux 中操作参照：<https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html>

        # 每周六，13点20运行
        20 13 * * 6 你的命令
* Windows 中使用计划任务参考文章<https://mp.weixin.qq.com/s/JKFvnmtlEqaE8GxbX6Fpyw>。
        
## 文件说明
* 整个文件为 Django 项目文件
### bili_rank 及 zhihu_rank
* 这是 django 中的两个应用文件夹，**bili_rank** 为哔哩哔哩应用，**zhihu_rank** 为知乎应用，两个文件夹大致相同因此着重介绍一个即可；
* **models.py** 应用模型文件，网站的数据库设计；
* **urls.py** 网站的路径设置；
* **views.py** 网站的方法设置；
* **admin.py**  可注册用户模型到 admin 管理员页面方便管理；
* **apps.py** 应用配置；
* **tests.py** 测试文件；
* **migrations** 文件夹内为用户数据迁移的记录文件；
* **templates** 网站的网页模板文件夹。
### get_rank.py 及 zhihu_rank.py
* **get_rank.py** 哔哩哔哩粉丝数前 100 用户排名更新文件，排名更新时定时跑这个文件。
* **zhihu_rank.py** 知乎粉丝数排名的更新文件。
### bili_rakn.sql 及 zhihu.sql
* bili_rakn.sql 及 zhihu.sql 分别为从数据库中导出的各站排名初始数据。
## 一些建议及说明
* 如何安装 git 见 <https://mp.weixin.qq.com/mp/appmsg/show?__biz=MjM5MDEyMDk4Mw==&appmsgid=10000361&itemidx=1&sign=f88b420f70c30c106697f54f00cf2a95>。
* django 是一个大型框架，学习周期相对长一些，但是 django 优点之一就是网上的资料很齐全。这里推荐两个入门教程,官方入门<https://docs.djangoproject.com/zh-hans/2.2/intro/tutorial01/>，django girl<https://tutorial.djangogirls.org/zh/>。
* 关于 django 项目 **除get_rank.py、zhihu_rank.py、bili_rakn.sql 及 zhihu.sql** 的详细说明可参考提供的 django 教程第一个链接。 
* scrapy 是一个优秀的数据爬取框架，官方新手教程 <https://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/tutorial.html>。
* 前端使用的 Datatables ，简单使用参考这里就行了 <https://datatables.club/manual/install.html>。 
* MongoDB 安装：<http://mongoing.com/archives/25650> ；使用：<https://juejin.im/post/5addbd0e518825671f2f62ee>。
* Linux 中 crontab 使用 <https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html>。里面有具体的使用实例。
      
      # 每小时的第3和第15分钟执行
      3,15 * * * * myCommand 
* Windows 中使用计划任务，使用方法参考文章<https://mp.weixin.qq.com/s/JKFvnmtlEqaE8GxbX6Fpyw>。
      
* 关于 get_rank.py 及 zhihu_rank.py 放置在 **django 项目文件夹内**，调用 django queryset 的办法；
    
      import os 
      import sys
      import django
      # 引入django配置文件
      os.environ.setdefault("DJANGO_SETTINGS_MODULE","rank.settings-server") # 系统 的环境变量
      django.setup()# 启动 Django
      from zhihu_rank import models # 启动项目后导入模块，就可以正常调用 queryset 存取数据了
      
   



