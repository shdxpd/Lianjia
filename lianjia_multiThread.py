#!/usr/bin/python
# -*- coding: <utf-8> -*-
import requests
from lxml import etree
import datetime
import time
import mydb
import random
import threading
import math
import pypinyin
from pypinyin import lazy_pinyin 

pos_urls = []      #Store ershoufang pos url  https://sh.lianjia.com/ershoufang/pudong/
sub_pos_urls = []  #Store sub pos url 
page_urls = []      #https://sh.lianjia.com/ershoufang/beicai/pg3/
id_urls=[]       #https://sh.lianjia.com/ershoufang/107100784617.html
id_urls_3w = [] #Back up id_urls every 3w

def get_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Host':'sh.lianjia.com',
                'Accept-Language':'en-US,en;q=0.5',
                'Accept-Encoding':'gzip, deflate, br',
                'Connection':'keep-alive',
                'Upgrade-Insecure=Requests':'1'
                }
    try:
        req = requests.get(url = url,headers = headers)
        res = req.content
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

def xpath_filter_6rule(url,rule1,rule2,rule3,rule4,rule5,rule6):
    res = get_url(url)
    result = etree.HTML(res)
    xpath1 = result.xpath(rule1)
    xpath2 = result.xpath(rule2)
    xpath3 = result.xpath(rule3)
    xpath4 = result.xpath(rule4)
    xpath5 = result.xpath(rule5)
    xpath6 = result.xpath(rule6)
    return(xpath1[0],xpath2[0],xpath3[0],xpath4[0],xpath5[0],xpath6[0])

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
        url = pos_urls[0]
        pos_urls.pop(0)
        sub_pos_rule = '/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a[position()<last()+1]/@href'
        sub_pos_hanzi_rule = '/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a[position()<last()+1]/text()'
        url_result = xpath_filter(url,sub_pos_rule)
        hanzi_result = xpath_filter(url,sub_pos_hanzi_rule)
#        print(url)
        for x in range(len(url_result)):                       
            temp_url = 'https://sh.lianjia.com'+ url_result[x]
            if temp_url == url:
                print(hanzi_result[x])
                temp_url = ''
                if hanzi_result[x] == '老闵行':
                    temp_url = 'https://sh.lianjia.com/ershoufang/laominhang/'
                else:
                    sub_pos = lazy_pinyin(hanzi_result[x])
                    for i in range(len(sub_pos)):
                        temp_url += str(sub_pos[i])
                    temp_url = 'https://sh.lianjia.com/ershoufang/' + temp_url
            sub_pos_urls.append(temp_url)
            lock.acquire()
            lock.release()


def get_page_url(i):
    global sub_pos_urls,page_urls,x
    while( x < int(len(sub_pos_urls))-1):
        lock.acquire()
        x = x + 1       
        page_url = sub_pos_urls[x]
        lock.release()
        house_number = '/html/body/div[4]/div[1]/div[2]/h2/span/text()'
        result = xpath_filter(page_url,house_number)
        total_page = math.ceil(int(result[0])/30)
        while(total_page > 100):
            print('There is a error url:',page_url)
            total_page = 0
        for page in range(int(total_page)+1):
            lock.acquire()
            page_urls.append(page_url+'pg'+str(page))
            lock.release()
    
def get_house_info(url):
    global id_urls_3w,id_urls
    while(len(page_urls)):
        lock.acquire()
        url = page_urls[0]
        page_urls.pop(0)
        lock.release()
        print('pages need to get info:',len(page_urls))         
        total_house_in_page = (xpath_filter(url,'/html/body/div[4]/div[1]/ul/li[last()]/a/@data-log_index'))[0]
        print(total_house_in_page)
        for i in range(1,int(total_house_in_page)+1):
            print(i)
            id = '/html/body/div[4]/div[1]/ul/li['+str(i)+']/div[1]/div[1]/a/@data-housecode'
            TotalPrice = '/html/body/div[4]/div[1]/ul/li['+str(i)+']/div[1]/div[6]/div[1]/span/text()'
            UnitPrice = '/html/body/div[4]/div[1]/ul/li['+str(i)+']/div[1]/div[6]/div[2]/span/text()'
            house_old = '/html/body/div[4]/div[1]/ul/li['+str(i)+']/div[1]/div[3]/div/text()'
            house_size = '/html/body/div[4]/div[1]/ul/li['+str(i)+']/div[1]/div[2]/div/text()'
            house_address = '/html/body/div[4]/div[1]/ul/li['+str(i)+']/div[1]/div[2]/div/a/text()'
            house_info = xpath_filter_6rule(url,id,TotalPrice,UnitPrice,house_old,house_size,house_address)
            lock.acquire()
            mydb.update_table(house_info)
            lock.release()

if __name__ == '__main__':

    url = 'https://sh.lianjia.com/ershoufang/'
    lock=threading.Lock()
    pos_urls = get_pos_url(url)
    print('Len of pos_urls',len(pos_urls))
    
    #mydb.create_db()
   # mydb.create_table()
    ts_final = []
    ts_t1 = []
    for i in range(0,10):
        t1= threading.Thread(target = get_sub_pos_url,args=(i,))
        ts_t1.append(t1)
    for t1 in ts_t1:
        t1.start()
    for t1 in ts_t1:
        t1.join()  
    print('Len of sub_pos_urls is :',len(sub_pos_urls))
    print('')
    ts_t2 = []
    x = -1
    for i in range(0,25):
        t2 = threading.Thread(target=get_page_url,args=(i,))
        ts_t2.append(t2)
    for t2 in ts_t2:
        t2.start()
    for t2 in ts_t2:
        t2.join()
    print('Len of page_urls is :',len(page_urls))
    print('')

    ts_t3 = []
    for i in range(0,1):
        t3 = threading.Thread(target=get_house_info,args = (i,))
        ts_t3.append(t3)
    for t3 in ts_t3:
        t3.start()
    for t3 in ts_t3:
        t3.join()
    print('\n')
    print('All done!!!')
    print('')


    