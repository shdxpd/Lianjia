import requests
from lxml import etree
import datetime
import time
import mydb
import random

url = 'https://sh.lianjia.com/ershoufang/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

pos_url = []      #Store ershoufang pos url
sub_pos_url = []  #Store sub pos url
page_urls = []
house_urls=[]


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

def get_house_url():
    for house_url in page_urls:
        print("Start get_house_url",house_url)
        time.sleep(random.random())
        hose_req = requests.get(url = house_url,headers = headers)
        hose_result = etree.HTML(hose_req.text)
        xpath_result = hose_result.xpath('/html/body/div[4]/div[1]/ul/li[position()<last()+1]/a/@href')
        for url in xpath_result:
            print(url)
            house_urls.append(url)
    print('Finish get_houss_url',house_url)
    
def get_house_info(url):
    print('Begain to get_house_info for url :',url)
    time.sleep(random.random())
    req = requests.get(url = url,headers = headers)
    result = etree.HTML(req.text)
    TotalPrice = result.xpath('/html/body/div[5]/div[2]/div[2]/span[1]/text()')[0]
    UnitPrice = result.xpath('/html/body/div[5]/div[2]/div[2]/div[1]/div[1]/span/text()')[0]
    Rom_mainInfo = result.xpath('/html/body/div[5]/div[2]/div[3]/div[1]/div[1]/text()')[0]       #2室两厅
    Rom_subInfo = result.xpath('/html/body/div[5]/div[2]/div[3]/div[1]/div[2]/text()')[0]        #低楼层/共12层
    Area_mainInfo = result.xpath('/html/body/div[5]/div[2]/div[3]/div[3]/div[1]/text()')[0]       #112.1平米
    Area_subInfo = result.xpath('/html/body/div[5]/div[2]/div[3]/div[3]/div[2]/text()')[0]        #2008年建/板楼
    areaName = result.xpath('/html/body/div[5]/div[2]/div[4]/div[2]/span[2]/text()')[0]          #浦东 金杨 内环至中环
    return(TotalPrice,UnitPrice,Rom_mainInfo,Rom_subInfo,Area_mainInfo,Area_subInfo,areaName)
    
    
def data_to_db():
    for i in range (0,len(Cells)):
        mydb.update_table(HousePos[i],Cells[i],High[i],TotalH[i],HouseYear[i],HouseType[i],HouseSize[i],TotalP[i],UnitP[i],HouseInter[i],HouseUrl[i])
        print("Update infor of ",i)

def main():
#    get_pos_url()'ascii' codec can't encode character u'\u5ba4' in position 1: ordinal not in range(128)
#    get_sub_pos_url()
#    get_page_url()
#    get_house_url()
    print(get_house_info('https://sh.lianjia.com/ershoufang/107100503895.html'))
#    mydb.create_db()
#    mydb.create_table()
#    for url in house_urls:
#        print(url)
#        getdata(page_url)
#        data_to_db()
main()
