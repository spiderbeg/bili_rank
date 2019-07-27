# -*- coding:utf8 -*-
# blbl 粉丝前一百检查
import requests
import time
import copy
#外部启动django脚本-----------------------------------------------------
import os 
import sys
import django
import logging
logging.basicConfig(filename='rank.log', filemode='w', level=logging.DEBUG)

# 将django项目根目录加入环境变量 # 当在 django 文件夹下时，就已经有了 python 的环境变量。不在 django 文件夹下使用这句
# sys.path.extend([r'E:\CS\CS_Projects\pythonv\Web_Projects\rank',])# python 的环境变量 # 
#引入django配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE","rank.settings-server") # 系统 的环境变量
django.setup()#项目外启动Django

from bili_rank import models#启动项目后导入模块------------------------------

def get_new(send_count):
    '''获取新的排名'''
    allid, qiid = {1,}, {1,}
    headers = {
        'Referer': 'https://www.bilibili.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    for i,s in enumerate(send_count):
        allid.add(s[0])  # 0 更新去重使用
        qiid.add(s[0]) # 爬取去重使用
        # 1、粉丝数更新
        urlm = 'https://api.bilibili.com/x/relation/stat?vmid=' + str(s[0]) + '&jsonp=jsonp' 
        try:
            rm = requests.get(urlm, headers=headers) # 粉丝数、关注数
        except requests.exceptions.RequestException as e:
            logging.warning('粉丝数更新处%s',e)
        resm = rm.json()
        time.sleep(1)
        mid = resm['data']['mid']
        followerm = resm['data']['follower']
        s[1][0] = followerm
    send_count = sorted(send_count, key=lambda item:item[1][0]) # 排序
    
    for i,s in enumerate(send_count):
        if i>=0:
            # 1.1 关注数搜寻
            logging.info('起始 id%s, 个数%d', s[0], i)
            uc = 1
            while True:
                url = 'https://api.bilibili.com/x/relation/followings?vmid=' + str(s[0]) + '&pn=' + str(uc) + '&ps=50&order=desc&jsonp=jsonp'
                try:
                    r = requests.get(url, headers=headers) # 关注人数
                except requests.exceptions.RequestException as e:
                    logging.warning('关注人数处%s', e)
                    break
                res = r.json()
                if 'data' in res and  res['code']==0:
                    uc+=1
                else:
                    break
                for i2,u in enumerate(res['data']['list']): 
                    if u['mid'] in qiid:
                        continue
                    qiid.add(u['mid']) # 爬取去重
                    # 2、粉丝数
                    url2 = 'https://api.bilibili.com/x/relation/stat?vmid=' + str(u['mid']) + '&jsonp=jsonp'
                    try:
                        r2 = requests.get(url2, headers=headers) # 粉丝数、关注数
                    except requests.exceptions.RequestException as e:
                        logging.warning('粉丝数处%s',e)
                        break
                    res2 = r2.json()
                    time.sleep(1)
                    name = u['uname']
                    mid = res2['data']['mid']
                    follower = res2['data']['follower']

                    if mid not in allid and follower>send_count[0][1][0]:
                        '''更新前100队列'''
                        allid.add(mid) # 去重
                        se = (mid,[follower,name,0]) # 排名默认为0
                        send_count.pop(0) # 删除
                        send_count.append(se) # 添加元素
                        send_count = sorted(send_count, key=lambda item:item[1]) # 排序

    logging.debug('更新后元组%s',send_count)
    newz = {} # 新的排名
    for i,send in enumerate(send_count):
        send[1][2] = 100-i   # 加排名
        newz[send[0]] = send[1] # 新的字典数据
    return newz

# 1、更新排名数据
al = models.User_info.objects.order_by('-lastmodify','-follower_count')[:100]
oldz = {}
for a in al:
    oldz[int(a.uid)] = [a.follower_count,a.name,a.rank] # 旧的排名

send_count = sorted(oldz.items(), key=lambda item:item[1][0]) # 生成元组中的列表还是字典中的列表
send_count = copy.deepcopy(send_count) # 深复制
logging.debug('输入的send_count%s',send_count)
start = time.time()
newz = get_new(send_count)
end = time.time()
use = end - start
logging.debug('原来的排名情况%s', oldz)
logging.debug('此次更新花费时间/分%s', use/60)
logging.debug('新的排名情况%s', newz)

# 2、 将排名数据更新至数据库
usez = copy.deepcopy(newz)
for i in newz:
    if i in oldz: # 新上榜已默认值为准,模型中设置为 字符串
        cfollower = newz[i][0] if oldz[i][0] == -10000000 else newz[i][0] - oldz[i][0]
        crank = newz[i][2] if oldz[i][2] == -200 else newz[i][2] - oldz[i][2]
    else:
        cfollower = -10000000
        crank = -200
    usez[i].extend([cfollower,crank])
        
logging.debug('最后储存的排名情况%s', usez)
for z in usez:
    obj = models.User_info.objects.create(uid=z, name=usez[z][1], follower_count=usez[z][0], rank=usez[z][2], addfollower=usez[z][3], lastrank=usez[z][4]) # update
