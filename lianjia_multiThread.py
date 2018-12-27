#!/usr/bin/python
# -*- coding: <utf-8> -*-
import requests
from lxml import etree
import datetime
import time
import mydb
import random
import threading

sem=threading.Semaphore(10) 

threads  = []

pos_urls = []      #Store ershoufang pos url  https://sh.lianjia.com/ershoufang/pudong/
sub_pos_urls = []  #Store sub pos url 
page_urls = []      #https://sh.lianjia.com/ershoufang/beicai/pg3/
id_urls=[]       #https://sh.lianjia.com/ershoufang/107100784617.html

def get_url(url):
    headers = headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    try:
        req = requests.get(url = url,headers = headers)
        res = req.content
        time.sleep(random.random())
        return res
    except requests.exceptions.HTTPError as e:
        print('HTTP Error :'+str(e))
        return get_url
    except requests.exceptions.ConnectionError as e:
        print('Connect error:' + str(e))
        return get_url
    except requests.exceptions.ConnectTimeout:
        print('Connect Timeout')
        return get_url
    except:
        print('Unknown error')
        return get_url

def xpath_filter(url,rule):
    res = get_url(url)
    result = etree.HTML(res)
    xpath = result.xpath(rule)
    return xpath

def xpath_filter_8rule(url,rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8):
    res = get_url(url)
    result = etree.HTML(res)
    xpath1 = result.xpath(rule1)
    xpath2 = result.xpath(rule2)
    xpath3 = result.xpath(rule3)
    xpath4 = result.xpath(rule4)
    xpath5 = result.xpath(rule5)
    xpath6 = result.xpath(rule6)
    xpath7 = result.xpath(rule7)
    xpath8 = result.xpath(rule8)
    return(xpath1[0],xpath2[0],xpath3[0],xpath4[0],xpath5[0],xpath6[0],xpath7[0],xpath8[0])

def get_pos_url(pos_url):
    pos_urls = []
    pos_rule = '/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a[position()<last()+1]/@href'
    result = xpath_filter(pos_url,pos_rule)
    for pos in result:
        pos_urls.append('https://sh.lianjia.com'+str(pos))
    return pos_urls

def get_sub_pos_url(i):
    global pos_urls,sub_pos_urls
    while(len(pos_urls)):
        lock.acquire
        url = pos_urls[0]
        pos_urls.pop(0)
        print('Get_sub_pos_url left url :',len(pos_urls),end='\r')
        time.sleep(0.01)
        lock.release
        sub_pos_rule = '/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a[position()<last()+1]/@href'
        result = xpath_filter(url,sub_pos_rule)
        
        lock.acquire()
        for sub_pos in result:
            sub_pos_urls.append('https://sh.lianjia.com'+str(sub_pos))
        lock.release()
        time.sleep(0.01)

def get_page_url(i):
    global sub_pos_urls,page_urls
    while(len(sub_pos_urls)):
        lock.acquire()
        url = sub_pos_urls[0]
        sub_pos_urls.pop(0)
        print('Get_sub_pos_url left url :',len(sub_pos_urls),end='\r')
        time.sleep(0.01)
        lock.release()
        page_rule = '/html/body/div[4]/div[1]/div[8]/div[2]/div/@page-data'
        result = xpath_filter(url,page_rule)
        while(len(result)):
            total_page = str(result).split(',')[0].split(':')[1]
            lock.acquire()       
            for page in range(1,int(total_page)+1):
                page_urls.append(url+'pg'+str(page))
            lock.release()
            break
        else:
            lock.acquire()
            page_urls.append(url)
            lock.release()
    
def get_id_url(i):
    global page_urls,id_urls
    while(len(page_urls)):
        lock.acquire()
        url = page_urls[0]
        page_urls.pop(0)
        print('Get_id_url left url :',len(page_urls),end='\r')
        time.sleep(0.01)
        lock.release()
        id_rule = '/html/body/div[4]/div[1]/ul/li[position()<last()+1]/a/@href'
        result = xpath_filter(url,id_rule)
        lock.acquire()
        for id in result:
            id_urls.append(id)
        lock.release()
    
def get_house_info(url):
    id = '/html/body/div[5]/div[2]/div[1]/@log-mod'
    TotalPrice = '/html/body/div[5]/div[2]/div[2]/span[1]/text()'
    UnitPrice = '/html/body/div[5]/div[2]/div[2]/div[1]/div[1]/span/text()'
    Rom_mainInfo = '//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[1]/text()'
    Rom_subInfo = '//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[2]/text()'
    Area_mainInfo = '//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[3]/text()'
    Area_subInfo = '/html/body/div[5]/div[2]/div[3]/div[3]/div[2]/text()'
    label = '/html/body/div[5]/div[2]/div[4]/div[1]/a[1]/text()'
    house_info = xpath_filter_8rule(url,id,TotalPrice,UnitPrice,Rom_mainInfo,Rom_subInfo,Area_mainInfo,Area_subInfo,label)
 #   mydb.update_table(house_info)
    thread  = []


if __name__ == '__main__':

    url = 'https://sh.lianjia.com/ershoufang/'
    lock=threading.Lock()
    pos_urls = get_pos_url(url)
    print('Len of pos_urls',len(pos_urls))
    
    for i in range(0,10):
        t1= threading.Thread(target = get_sub_pos_url,args=(i,))
        t1.start()
    t1.join()  
    print('Len of sub_pos_urls is :',len(sub_pos_urls))
    print('')
    
    for i in range(0,10):
        t2 = threading.Thread(target=get_page_url,args=(i,))
        t2.start()
    t2.join()
    print('Len of page_urls is :',len(page_urls))
    print('')

    for i in range(0,10):
        t3 = threading.Thread(target=get_id_url,args = (i,))
        t3.start()
    t3.join()
    print('Len of id_urls is:',len(id_urls))
    print('')

        
        
