# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import xlwt
import time
import mydb
import random

from lxml import etree
import datetime


url = 'https://sh.lianjia.com/ershoufang/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

Cells = []
TotalP = []
UnitP = []
High = []
TotalH = []
HouseYear = []
HousePos = []
HouseUrl = []
HouseType = []
HouseSize = []
HouseInter = []

pos_url = []      #Store ershoufang pos url
sub_pos_url = []  #Store sub pos url
page_urls = []


def get_pos_url():
    print("Enter get_pos_url")
    get_pos_url_starttime = datetime.datetime.now()
    res = requests.get(url = url , headers = headers)
    result = etree.HTML(res.text)
    pos_result = result.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a[position()<last()+1]/@href')
    for pos in pos_result:
        pos_url.append('https://sh.lianjia.com'+str(pos))
    print("Finish get_pos_url")
    get_pos_url_endtime = datetime.datetime.now()
    print ('Get_pos_url time is',(get_pos_url_endtime - get_pos_url_starttime).seconds)

def get_sub_pos_url():
    get_sub_pos_url_starttime = datetime.datetime.now()
    for sub_url in pos_url:
        print("Start get_sub_pos_url",sub_url)
        sub_res = requests.get(url = sub_url,headers = headers)
        sub_result = etree.HTML(sub_res.text)
        time.sleep(random.random())
        sub_pos_xpath = sub_result.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a[position()<last()+1]/@href')
        for sub_pos in sub_pos_xpath:
            sub_pos_url.append('https://sh.lianjia.com'+str(sub_pos))
        print("Finish get_sub_pos_url",sub_url)
    get_sub_pos_url_endtime = datetime.datetime.now()
    print ('Total get_sub_pos_url time is',(get_sub_pos_url_endtime - get_sub_pos_url_starttime).seconds)

def get_page_url():
    get_sub_pos_url_starttime = datetime.datetime.now()
    for sub_page_url in sub_pos_url:
        print("Start get_page_url",sub_page_url)
        time.sleep(random.random())
        sub_page_res = requests.get(url = sub_page_url,headers = headers)
        sub_page_result = etree.HTML(sub_page_res.text)
        xpath_result = str(sub_page_result.xpath('/html/body/div[4]/div[1]/div[8]/div[2]/div/@page-data'))
        if(xpath_result == '[]'):
            total_page = 1
            print("Total number in this URL less than 30")
        else:
            total_page = xpath_result.split(',')[0].split(':')[1]
        for i in range(1,int(total_page)+1):
            page_urls.append(sub_page_url+'pg'+str(i))
        print("Finish get_page_url",sub_page_url)
    get_sub_pos_url_endtime = datetime.datetime.now()
    print ('Total get_page_url times is :',(get_sub_pos_url_endtime - get_sub_pos_url_starttime).seconds)

def getdata(getdata_url):
    print('Begain to get data for url :',getdata_url)
    time.sleep(random.random())
    res = requests.get(user = getdata_url,headers = headers)
    soup = BeautifulSoup(res.content,features="html.parser")
    houseInfo = soup.select('div.houseInfo a')
    houseSize = soup.select('div.houseInfo')
    houseTitle = soup.select('div.title a')
    totalPrice = soup.select('div.totalPrice span')
    unitPrice = soup.select('div.unitPrice span')
    position = soup.select('div.positionInfo')

    for i in range(0, len(houseInfo)):
        print(i)
        HousePos.append(position[i].getText().split('-')[1])
        HouseYear.append(position[i].getText().split(')')[1][0:4]) 
        TotalH.append(position[i].getText().split(')')[0][5:-1])
        High.append(position[i].getText().split('(')[0])
        Cells.append(houseSize[i].getText().split('|')[0]) 
        HouseType.append(houseSize[i].getText().split('|')[1]) 
        HouseSize.append(houseSize[i].getText().split('|')[2][:-3]) 
        HouseInter.append(houseSize[i].getText().split('|')[4]) 
        TotalP.append(totalPrice[i].getText())
        UnitP.append(unitPrice[i].getText()[2:-4]) 
        HouseUrl.append(houseTitle[i].get('href')) 

def data_to_db():
    for i in range (0,len(Cells)):
        mydb.update_table(HousePos[i],Cells[i],High[i],TotalH[i],HouseYear[i],HouseType[i],HouseSize[i],TotalP[i],UnitP[i],HouseInter[i],HouseUrl[i])
        print("Update infor of ",i)

def main():
    get_pos_url()
    get_sub_pos_url()
    get_page_url()
#    mydb.create_db()
#    mydb.create_table()
    for page_url in page_urls:
        print(page_url)
#        getdata(page_url)
#        data_to_db()
main()
