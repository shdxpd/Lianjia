import requests
from lxml import etree
import datetime
import lianjia
import mydb


headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

url = 'https://sh.lianjia.com/ershoufang/'

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
        print ((get_pos_url_endtime - get_pos_url_starttime).seconds)

def get_sub_pos_url():
        print("Enter get_sub_pos_url")
        get_sub_pos_url_starttime = datetime.datetime.now()
        for sub_url in pos_url:
                sub_res = requests.get(url = sub_url,headers = headers)
                sub_result = etree.HTML(sub_res.text)
                time.sleep(random.randint(0, 300))
                sub_pos_xpath = sub_result.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a[position()<last()+1]/@href')
        for sub_pos in sub_pos_xpath:
                sub_pos_url.append('https://sh.lianjia.com'+str(sub_pos))
        print("Finish get_sub_pos_url")
        get_sub_pos_url_endtime = datetime.datetime.now()
        print ((get_sub_pos_url_endtime - get_sub_pos_url_starttime).seconds)

def get_page_url():
        global page_urls
        print("Enter get_page_url")
        get_sub_pos_url_starttime = datetime.datetime.now()
        for sub_page_url in sub_pos_url:
                time.sleep(random.randint(0, 300))
                sub_page_res = requests.get(url = sub_page_url,headers = headers)
                sub_page_result = etree.HTML(sub_page_res.text)
                sub_page_xpah = sub_page_result.xpath('/html/body/div[4]/div[1]/div[8]/div[2]/div/a[position()<last()]/@href')
        for page_url in sub_page_xpah:
                page_urls.append('https://sh.lianjia.com'+str(page_url))
                print(page_url)
        print("Finish get_page_url")
        get_sub_pos_url_endtime = datetime.datetime.now()
        print ((get_sub_pos_url_endtime - get_sub_pos_url_starttime).seconds)

