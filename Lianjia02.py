import requests
from lxml import etree
import math
import mydb02
import sqlite3

start_url = 'https://sh.lianjia.com/ershoufang/'
page_urls = []
house_info = []

cout = 0

def get_url(url):
    global cout
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    req = requests.get(url,headers = {'User-Agent':UA})
    cout = cout + 1
    return req

num_rule = '/html/body/div[4]/div[1]/div[2]/h2/span/text()'
ershoufang_rule = '/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a[position()<last()+1]/@href'
ershoufang_p_rule = '/html/body/div[3]/div/div[2]/dl[1]/dd/a[position()<last()+1]/span[3]/text()'

def get_page_url(url):
    Total_request = get_url(url)
    Total_etree = etree.HTML(Total_request.content)
    Total_num = Total_etree.xpath(num_rule)
    print('Total num is',Total_num)
    ershoufang_url = Total_etree.xpath(ershoufang_rule)
    mydb02.create_db()
    mydb02.create_table()
    for url in ershoufang_url:
        url = 'https://sh.lianjia.com'+str(url)
        ershoufang_request = get_url(url)
        ershoufang_etree = etree.HTML(ershoufang_request.content)
        ershoufang_num = ershoufang_etree.xpath(num_rule)[0]
        print('Num in ' +str(url) + ' is' + str(ershoufang_num))
        if(int(ershoufang_num) > 3000):
            ershoufang_p_nums = ershoufang_etree.xpath(ershoufang_p_rule)
            for i in range(len(ershoufang_p_nums)):
                ershoufang_p_num = ershoufang_p_nums[i]
                ershoufang_p_num = ershoufang_p_num.split('(')[1].split(')')[0]
                ershoufang_p_page = math.ceil(int(ershoufang_p_num)/30)
                for j in range(int(ershoufang_p_page)):
                    page_url = url + 'pg' + str(j+1)+ 'p' + str(i+1)
                    page_urls.append([page_url,url.split('/')[-2]])
        else:
            ershoufang_P_total_page = math.ceil(int(ershoufang_num)/30)
            for page in range(int(ershoufang_P_total_page)+1):
                page_url = url + 'pg' + str(page)
                page_urls.append([page_url,url.split('/')[-2]])
    mydb02.update_table(page_urls)
    mydb02.close_table()

def get_house_info():
    house_url_rule = '/html/body/div[4]/div[1]/ul/li[position()<last()+1]/div[1]/div[1]/a/@href'
    house_1st_line_info_rule = '/html/body/div[4]/div[1]/ul/li[position()<last()+1]/div[1]/div[2]/div/text()'
    house_2nd_line_info_rule = '/html/body/div[4]/div[1]/ul/li[position()<last()+1]/div[1]/div[3]/div/text()'
    house_3rd_line_info_rule = '/html/body/div[4]/div[1]/ul/li[position()<last()+1]/div[1]/div[4]/text()'
    house_total_price_rule = '/html/body/div[4]/div[1]/ul/li[position()<last()+1]/div[1]/div[6]/div[1]/span/text()'
    house_unit_price_rule = '/html/body/div[4]/div[1]/ul/li[position()<last()+1]/div[1]/div[6]/div[2]/span/text()'
    for page_url in pages:
        page_request = get_url(page_url[0])
        print('Get page data for URL ' + page_url[0])
        page_etree = etree.HTML(page_request.content)
        house_urls = page_etree.xpath(house_url_rule)
        house_1st_line_info = page_etree.xpath(house_1st_line_info_rule)
        house_2nd_line_info = page_etree.xpath(house_2nd_line_info_rule)
        house_3rd_line_info = page_etree.xpath(house_3rd_line_info_rule)
        house_total_price_info = page_etree.xpath(house_total_price_rule)
        house_unit_price_info = page_etree.xpath(house_unit_price_rule)
        for i in range(len(house_urls)):
            try:
                url = house_urls[i]
                huxing = house_1st_line_info[i].split('|')[1]
                mianji = house_1st_line_info[i].split('|')[2]
                chaoxiang = house_1st_line_info[i].split('|')[3]
                zhuangxiu = house_1st_line_info[i].split('|')[4]
                dianti = house_1st_line_info[i].split('|')[5]
                louceng = house_2nd_line_info[i].split('(')[0]
                zonglouceng = house_2nd_line_info[i].split('(')[1].split(')')[0]
                nianling = house_2nd_line_info[i].split(')')[1].split('年')[0]
                fabushijian = house_3rd_line_info[i].split('/')[2]
                total_price = house_total_price_info[i]
                unit_price = house_unit_price_info[i].split('单价')[1].split('元')[0]
            except:
                dianti = '无电梯'
            house_info.append([page_url[1],url,huxing,mianji,chaoxiang,zhuangxiu,dianti,louceng,zonglouceng,nianling,fabushijian,total_price,unit_price])
        print('')

if __name__ == '__main__':
    #get_page_url(start_url)
    pages = mydb02.get_data()
    get_house_info()
    print('')  