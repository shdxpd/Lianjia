import requests
from lxml import etree

headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

url = 'https://sh.lianjia.com/ershoufang/'

res = requests.get(url = url , headers = headers)
result = etree.HTML(res.text)

pos_result = result.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a[position()<last()+1]/@href')

pos_url = []      #Store ershoufang pos url

for pos in pos_result:
    pos_url.append('https://sh.lianjia.com'+str(pos))

#Get sub pos URL
sub_pos_url = []  #Store sub pos url
for sub_url in pos_url:
    sub_res = requests.get(url = sub_url,headers = headers)
    sub_result = etree.HTML(sub_res.text)
    sub_pos_xpath = sub_result.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a[position()<last()+1]/@href')

    for sub_pos in sub_pos_xpath:
        sub_pos_url.append('https://sh.lianjia.com'+str(sub_pos))

#Get page URL
page_urls = []
for sub_page_url in sub_pos_url:
    sub_page_res = requests.get(url = sub_page_url,headers = headers)
    sub_page_result = etree.HTML(sub_page_res.text)
    sub_page_xpah = sub_page_result.xpath('/html/body/div[4]/div[1]/div[8]/div[2]/div/a[position()<last()]/@href')

    for page_url in sub_page_xpah:
        page_urls.append('https://sh.lianjia.com'+str(page_url))
        print(page_url)

#for url in page_urls:
#    print(url)

    
    