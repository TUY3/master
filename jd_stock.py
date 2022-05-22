from decimal import InvalidOperation
from email import message
import json
import requests
import sys
import os
from os import path
import re

#读取库存
if 'stock_Ids' in os.environ:
    Ids= os.environ["stock_Ids"]
else:
    Ids= '100014352545'
skuIds =Ids.split('&')

#读取地址精度
if 'stock_area_flag' in os.environ:
    flag=os.environ["stock_area_flag"]
else:
    flag=2

area_Id={'1_2805_34545':'北京'}
message=''
commoditiesStock = {}
commoditiesName = {}


def load_send():
    global send
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/sendNotify.py"):
        try:
            from sendNotify import send
        except:
            send=False
            print("加载通知服务失败~")
    else:
        send=False
        print("加载通知服务失败~")




#获取地区
def getArea_Id(url):
    file  = os.listdir(url)
    for f in file:
        real_url = path.join (url , f)
        if path.isfile(real_url):
            print(path.abspath(real_url))
            with open(path.abspath(real_url),'r',encoding='utf8') as fp:#path为json文件路径
                json_data = json.load(fp)
                for province,citys in json_data.items():
                    for city,towns in citys.items():  
                        for town,unknows in towns.items():
                                if isinstance(unknows,dict):
                                    for add,id in unknows.items():
                                        break
                                else:
                                    id= unknows
                                    break 
                        if flag==1:  #详细到市区   
                            address=province+city
                            line = address.strip()  
                            p2 = re.compile('[^\u4e00-\u9fa5]')  # 中文的编码范围是：\u4e00到\u9fa5
                            zh = " ".join(p2.split(line)).strip()
                            zh = ",".join(zh.split())
                            area_Id[id]=zh
                            p2=''
                            zh=''
       
                    if flag==2:
                        address=province
                        area_Id[id]=address
                        line = address.strip()  
                        p2 = re.compile('[^\u4e00-\u9fa5]')  # 中文的编码范围是：\u4e00到\u9fa5
                        zh = " ".join(p2.split(line)).strip()
                        zh = ",".join(zh.split())
                        area_Id[id]=zh
                        p2=''
                        zh=''
                    
    return area_Id

# 库存状态
def getStockState(skuId,areaId):
    url='http://c0.3.cn/stocks?type=getstocks&skuIds='+skuId+'&area='+areaId
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-cn",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    return  requests.post(url=url, headers=headers).json()
    
# 商品详细名称
def getCommoditiesName(skuId):
    url='https://yx.3.cn/service/info.action?ids='+skuId
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-cn",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    return  requests.post(url=url, headers=headers).json()


if __name__ == '__main__':
    load_send()
    area_Id=getArea_Id('.\\area')
    for i in range(len(skuIds)):
        for areaId in area_Id:
          commoditiesStock= getStockState(skuIds[i],areaId)
          commoditiesName = getCommoditiesName(skuIds[i])
          message.join(str(commoditiesName[skuIds[i]]['name'])+'     '+str(area_Id[areaId])+'    '+str(commoditiesStock[skuIds[i]]['StockStateName'])+'\n')
          print(commoditiesName[skuIds[i]]['name']+'     '+str(area_Id[areaId])+'    '+commoditiesStock[skuIds[i]]['StockStateName'] )
        message.join('商品链接：https://item.jd.com/'+skuIds[i]+'.html\n')
        print('商品链接：https://item.jd.com/'+skuIds[i]+'.html\n')
    send('🔔京东库存, 开始!',message)
