# coding:utf8
# 知乎现有前 100，数据更新
# 知乎 粉丝前一百
import requests
import time
import datetime
import copy
from bs4 import BeautifulSoup
import json
import logging
logging.basicConfig(level=logging.DEBUG)
# 外部启动django脚本-----------------------------------------------------
import os 
import sys
import django

# 将django项目根目录加入环境变量
# sys.path.extend([r'E:\CS\CS_Projects\pythonv\Web_Projects\rank',])# python 的环境变量
# 引入django配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE","rank.settings-server") # 系统 的环境变量
django.setup()# 项目外启动Django

from zhihu_rank import models # 启动项目后导入模块----------

def updatedata(send_count):
    """更新排名"""
    used = {1,}
    # 第一步 更新已有排名
    for i in send_count: 
        used.add(i[0]) # 前 100 uid
        url = 'https://www.zhihu.com/people/'+ i[0] + '/activities'
        r = requests.get(url, headers={'user-agent':'chrome'})
        time.sleep(2.5)
        soup = BeautifulSoup(r.text)
        res6 = soup.find_all(id='js-initialData')[0]
        total = json.loads(res6.string) # 反序列化为 dict
        user_info = total['initialState']['entities']['users']
        followercount = user_info[i[0]]['followerCount'] # 粉丝数
        name = user_info[i[0]]['name'] # 昵称
        i[1][0] = followercount # 更新粉丝数
        i[1][1] = name # 更新昵称

    send_count = sorted(send_count, key=lambda item:item[1][0],reverse=True) # 再次降序排布排序
    # 第二步查找是否有新的排名
    for i in send_count: # id 查找，
        off,nums = 0,500
        while True: # 翻页
            url2 = 'https://www.zhihu.com/api/v4/members/' + i[0] + '/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=' + str(off) + '&limit=' + str(nums)
            r2 = requests.get(url2, headers={'user-agent':'chrome'})
            time.sleep(0.5)
            if 'error' in r2.json():
                if r2.json()['error']['code']in {310000, 310001}:
                    break
                else:
                    raise NameError('页面错误')
            for d in r2.json()['data']:
                cuid = d['url_token']
                cname = d['name']
                cfollowercount = d['follower_count']
                if cuid not in used and cfollowercount > send_count[-1][1][0]:
                    used.add(cuid)
                    se = (cuid, [cfollowercount,cname,0])
                    send_count.pop(-1) # 删除最小
                    send_count.append(se) # 添加新元素
                    send_count = sorted(send_count, key=lambda item:item[1],reverse=True) # 降序排列
            if r2.json()["paging"]['is_end'] == False:
                nums+=500
                off+=500
            elif r2.json()["paging"]['is_end'] == True:
                break
            else:
                break

    newz = {}
    for i,u in enumerate(send_count): # 更新排名及生成新的前100字典
        u[1][2] = i+1
        newz[u[0]] = u[1]
    return newz
# 旧排名
users = models.User_info.objects.all().order_by('-modify', '-followerCount')[:100] # 最近的前100位
oldz = {}
for u in users:
    oldz[u.user.uid] = [u.followerCount,u.user.name,u.rank]
logging.debug('之前的 oldz 字典%s', oldz)
send_count = sorted(oldz.items(), key=lambda item:item[1][0],reverse=True)
send_count = copy.deepcopy(send_count) # 深复制
logging.debug('输入的send_count%s', send_count)
# 返回新的前100排名
start = time.time()
newz = updatedata(send_count)
end = time.time()
times = end-start # 更新时间
logging.debug('返回的 newz 字典%s', newz)
# 添加排名变化及粉丝变化
usez = copy.deepcopy(newz) # 使用的更新字典
for i in newz:
    if i in oldz: # 新上榜已默认值为准,模型中设置为 字符串
        cfollower = newz[i][0] if oldz[i][0] == -10000000 else newz[i][0] - oldz[i][0]
        crank = newz[i][2] if oldz[i][2] == -200 else newz[i][2] - oldz[i][2]
    else:
        cfollower = -10000000
        crank = -200
    usez[i].extend([cfollower,crank])
logging.debug('时间：%s; 所用时长: %s 分钟; 最终情况：%s', datetime.datetime.now(),times//60,usez)
# 更新数据库信息
for z in usez:
    u, created = models.User.objects.update_or_create(
            uid=z, # get
            defaults={'name':usez[z][1]} # update
        )
    u = models.User_info.objects.create(user=u,followerCount=usez[z][0],rank=usez[z][2],followerchange=usez[z][3],rankchange=usez[z][4])