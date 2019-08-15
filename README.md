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
## 详细流程

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
## 一些建议
* django 是一个大型框架，学习周期相对长一些，但是 django 优点之一就是网上的资料很齐全。这里推荐两个入门教程,官方入门<https://docs.djangoproject.com/zh-hans/2.2/intro/tutorial01/>，django girl<https://tutorial.djangogirls.org/zh/>。
* scrapy 是一个优秀的数据爬取框架，
