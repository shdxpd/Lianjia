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

lock=threading.Lock()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Host':'sh.lianjia.com',
                'Accept-Language':'en-US,en;q=0.5',
                'Accept-Encoding':'gzip, deflate, br',
                'Upgrade-Insecure=Requests':'1'
                }

pos_rule = '/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a[position()<last()+1]/@href'

sub_pos_rule = '/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a[position()<last()+1]/@href'
sub_pos_hanzi_rule = '/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a[position()<last()+1]/text()'

house_number_rule = '/html/body/div[4]/div[1]/div[2]/h2/span/text()'



def get_url(url):  
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

def xpath_filter(res,rule):
    result = etree.HTML(res)
    xpath = result.xpath(rule)
    return xpath

def xpath_filter_6rule(res,rule1,rule2,rule3,rule4,rule5,rule6):
    result = etree.HTML(res)
    xpath1 = result.xpath(rule1)
    xpath2 = result.xpath(rule2)
    xpath3 = result.xpath(rule3)
    xpath4 = result.xpath(rule4)
    xpath5 = result.xpath(rule5)
    xpath6 = result.xpath(rule6)
    return(xpath1[0],xpath2[0],xpath3[0],xpath4[0],xpath5[0],xpath6[0])

def get_pos_url(url):
    pos_urls = []
    url_result = get_url(url)
    result = xpath_filter(url_result,pos_rule)
    for pos in result:
        pos_urls.append('https://sh.lianjia.com'+str(pos))
    return pos_urls

def get_sub_pos_url(i):
    global pos_urls,sub_pos_urls
    while(len(pos_urls)):
        lock.acquire()
        url = pos_urls[0]
        pos_urls.pop(0)
        lock.release()       
        url_result = get_url(url)
        sub_pos_temp_urls = xpath_filter(url_result,sub_pos_rule)
        hanzi_result = xpath_filter(url_result,sub_pos_hanzi_rule)
        for x in range(len(sub_pos_temp_urls)):
            if hanzi_result[x] == '老闵行':
                temp_url = 'https://sh.lianjia.com/ershoufang/laominhang/'
            if hanzi_result[x] == '莘庄':
                temp_url = 'https://sh.lianjia.com/ershoufang/xinzhuang5/'
            else:                       
                temp_url = 'https://sh.lianjia.com'+ sub_pos_temp_urls[x]
                if temp_url == url:
                    print(hanzi_result[x])
                    sub_pos = lazy_pinyin(hanzi_result[x])
                    for i in range(len(sub_pos)):
                        temp_url += str(sub_pos[i])
                        temp_url = 'https://sh.lianjia.com/ershoufang/' + temp_url
            lock.acquire()
            sub_pos_urls.append(temp_url)
            lock.release()


def get_page_url(i):
    global sub_pos_urls,page_urls
    while(len(sub_pos_urls)):
        page_urls_temp = []

        lock.acquire()
        url = sub_pos_urls[0]
        sub_pos_urls.pop(0)
        lock.release()   

        url_result = get_url(url)
        result = xpath_filter(url_result,house_number_rule)
        total_page = math.ceil(int(result[0])/30)
        while(total_page > 100):
            print('There is a error url:',url)
            total_page = 0
        for page in range(int(total_page)+1):
            page_urls_temp.append(url+'pg'+str(page))

        lock.acquire()
        page_urls.append(page_urls_temp)
        lock.release()

def get_house_info(x):
    while(len(page_urls)):
        house_infos = []
        urls = []
        lock.acquire()
        urls = page_urls[0]
        page_urls.pop(0)
        lock.release()
        for url in urls:
            print(url)
            url_result = get_url(url)
            total_house_result = xpath_filter(url_result,'/html/body/div[4]/div[1]/ul/li[last()]/a/@data-log_index')
            if len(total_house_result):         
                total_house_in_page = (total_house_result)[0]
            else:
                break
            for i in range(1,int(total_house_in_page)+1):
                id = '/html/body/div[4]/div[1]/ul/li['+str(i)+']/div[1]/div[1]/a/@href'
                TotalPrice = '/html/body/div[4]/div[1]/ul/li['+str(i)+']/div[1]/div[6]/div[1]/span/text()'
                UnitPrice = '/html/body/div[4]/div[1]/ul/li['+str(i)+']/div[1]/div[6]/div[2]/span/text()'
                house_old = '/html/body/div[4]/div[1]/ul/li['+str(i)+']/div[1]/div[3]/div/text()'
                house_size = '/html/body/div[4]/div[1]/ul/li['+str(i)+']/div[1]/div[2]/div/text()'
                house_address = '/html/body/div[4]/div[1]/ul/li['+str(i)+']/div[1]/div[2]/div/a/text()'
                house_info = xpath_filter_6rule(url_result,id,TotalPrice,UnitPrice,house_old,house_size,house_address)
                house_infos.append(house_info) 
        lock.acquire()
        mydb.update_table(house_infos)
        lock.release()

if __name__ == '__main__':

    start_url = 'https://sh.lianjia.com/ershoufang/'
    
    starttime = datetime.datetime.now()
    pos_urls = get_pos_url(start_url)
    print('Len of pos_urls',len(pos_urls))
    endtime = datetime.datetime.now()
    print(endtime-starttime)

    mydb.create_db()
    mydb.create_table()
    starttime = datetime.datetime.now()
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
    endtime = datetime.datetime.now()
    print(endtime-starttime)
    print('')

    starttime = datetime.datetime.now()
    ts_t2 = []
    x = -1
    for i in range(0,50):
        t2 = threading.Thread(target=get_page_url,args=(i,))
        ts_t2.append(t2)
    for t2 in ts_t2:
        t2.start()
    for t2 in ts_t2:
        t2.join()
    print('Len of page_urls is :',len(page_urls))
    endtime = datetime.datetime.now()
    print(endtime-starttime)
    print('')

    starttime = datetime.datetime.now()
    ts_t3 = []
    for i in range(0,50):
        t3 = threading.Thread(target=get_house_info,args=(i,))
        ts_t3.append(t3)
    for t3 in ts_t3:
        t3.start()
    for t3 in ts_t3:
        t3.join()
    print('\n')
    print('All done!!!')
    endtime = datetime.datetime.now()
    print(endtime-starttime)
    print('')


    