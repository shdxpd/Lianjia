import requests
from bs4 import BeautifulSoup
import xlwt
import time
import ershoufang
import mydb

ershoufang.get_pos_url()
ershoufang.get_sub_pos_url()
ershoufang.get_page_url()

#url = 'https://sh.lianjia.com/ershoufang/'

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

def getdata(url):
    print(url)
    res = requests.get(url,headers = headers)
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

def main(url):
    print(url)
    getdata(url)
    data_to_db()

main(url)