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
        sub_page_xpah = sub_page_result.xpath('/html/body/div[4]/div[1]/div[8]/div[2]/div/@page-data')
        #pages = sub_page_xpah[0].extract()[0]  error here                                   
        print(type(sub_page_xpah))
        print(sub_page_xpah)
        '''
        for page_url in sub_page_xpah:
            page_urls.append('https://sh.lianjia.com'+str(page_url))
            print(page_url)
        '''
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

    for i in range(0, 30):
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
'''
def write_data(page):
    data = xlwt.Workbook()
    table=data.add_sheet('Lianjia')
    row = 0
    col = 0

    table.write(row, col, '地区')
    table.write(row, col + 1, '小区')
    table.write(row, col + 2, '楼层')
    table.write(row, col + 3, '总楼高')
    table.write(row, col + 4, '房龄')
    table.write(row, col + 5, '户型')
    table.write(row, col + 6, '面积')
    table.write(row, col + 8, '总价')
    table.write(row, col + 9, '单价')
    table.write(row, col + 10,'装修')
    table.write(row, col + 11,'链接')

    row = row+1
    for i in range (0,29+30*(page-1)):
        table.write(row,col,HousePos[i])
        table.write(row, col+1, Cells[i])
        table.write(row, col+2, High[i])
        table.write(row, col+3, TotalH[i])
        table.write(row, col+4, HouseYear[i])
        table.write(row, col+5, HouseType[i])
        table.write(row, col+6, HouseSize[i])
        table.write(row, col+7, HouseDirect[i])
        table.write(row, col+8, TotalP[i])
        table.write(row, col+9, UnitP[i])
        table.write(row, col+10, HouseInter[i])
        table.write(row, col+11, HouseUrl[i])
        row=row+1
        col=0
    data.save('Pudong300_400.xls')
'''
def data_to_db():
    for i in range (0,len(Cells)):
        mydb.update_table(HousePos[i],Cells[i],High[i],TotalH[i],HouseYear[i],HouseType[i],HouseSize[i],TotalP[i],UnitP[i],HouseInter[i],HouseUrl[i])
        print("Update infor of ",i)

def main():
    get_pos_url()
    get_sub_pos_url()
    get_page_url()
    mydb.create_db()
    mydb.create_table()
    for page_url in page_urls:
        print(page_url)
        getdata(page_url)
        data_to_db()
main()