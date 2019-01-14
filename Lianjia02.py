import requests
from lxml import etree
import math
import json
import mydb
import sqlite3

start_url = 'https://sh.lianjia.com/ershoufang/'
page_urls = []
house_info = []

cout = 0

def get_url(url):
    global cout
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    req = requests.get(url = url,headers = {'User-Agent':UA})
    cout = cout + 1
    return req

num_rule = '/html/body/div[4]/div[1]/div[2]/h2/span/text()'
ershoufang_rule = '/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a[position()<last()+1]/@href'

def get_page_url():
    Total_request = get_url(start_url)
    Total_etree = etree.HTML(Total_request.content)
    Total_num = Total_etree.xpath(num_rule)
    print('Total num is',Total_num)
    ershoufang_url = Total_etree.xpath(ershoufang_rule)
    mydb.create_db()
    mydb.create_table()
    for url in ershoufang_url:
        url = 'https://sh.lianjia.com'+str(url)
        ershoufang_request = get_url(url)
        ershoufang_etree = etree.HTML(ershoufang_request.content)
        ershoufang_num = ershoufang_etree.xpath(num_rule)[0]
        print('Num in ' +str(url) + ' is' + str(ershoufang_num))
        if(int(ershoufang_num) > 3000):
            for i in range(1,8):
                url_P = url + 'p' + str(i)
                ershoufang_P_requests = get_url(url_P)
                ershoufang_P_etree = etree.HTML(ershoufang_P_requests.content)
                ershoufang_P_num = ershoufang_P_etree.xpath(num_rule)[0]
                if(int(ershoufang_P_num)>3000):
                    print(url_P)
                print('Num in ' +str(url_P) + ' is' + str(ershoufang_P_num))
                ershoufang_P_total_page = math.ceil(int(ershoufang_P_num)/30)
                for page in range(1,int(ershoufang_P_total_page)+1):
                    page_url = url + 'pg' + str(page) + 'p' + str(i)
                    page_urls.append([page_url,url])
        else:
            ershoufang_P_total_page = math.ceil(int(ershoufang_num)/30)
            for page in range(int(ershoufang_P_total_page)+1):
                page_url = url + 'pg' + str(page)
                page_urls.append([page_url,url])
    mydb.update_table(page_urls)
    mydb.close_table()

conn = sqlite3.connect('URL.db')
cu = conn.cursor()
cu.execute('select * from url_total')
pages = cu.fetchall()
conn.close()

house_url_rule = '/html/body/div[4]/div[1]/ul/li[position()<last()+1]/div[1]/div[1]/a/@href'
house_info_rule = '/html/body/div[4]/div[1]/ul/li[position()<last()+1]/'
house_1st_line_info_rule = '/html/body/div[4]/div[1]/ul/li[position()<last()+1]/div[1]/div[2]/div/text()'
house_2nd_line_info_rule = '/html/body/div[4]/div[1]/ul/li[position()<last()+1]/div[1]/div[3]/div/text()'
house_3rd_line_info_rule = '/html/body/div[4]/div[1]/ul/li[position()<last()+1]/div[1]/div[4]/text()'
house_total_price_rule = '/html/body/div[4]/div[1]/ul/li[position()<last()+1]/div[1]/div[6]/div[1]/span/text()'
house_unit_price_rule = '/html/body/div[4]/div[1]/ul/li[position()<last()+1]/div[1]/div[6]/div[2]/span/text()'
for page_url in pages:
    page_request = get_url(page_url[0])
    page_etree = etree.HTML(page_request.content)
    house_urls = page_etree.xpath(house_url_rule)
    house_1st_line_info = page_etree.xpath(house_1st_line_info_rule)
    house_2nd_line_info = page_etree.xpath(house_2nd_line_info_rule)
    house_3rd_line_info = page_etree.xpath(house_3rd_line_info_rule)
    house_total_price_info = page_etree.xpath(house_total_price_rule)
    house_unit_price_info = page_etree.xpath(house_unit_price_rule)
    print('')

    