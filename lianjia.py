import requests
from bs4 import BeautifulSoup
import xlwt
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

#url = 'https://sh.lianjia.com/ershoufang/pudong/PG'+str(j)+'P2/'

Cells = {}
TotalP = {}
UnitP = {}
High = {}
TotalH = {}
HouseYear = {}
HousePos = {}
HouseUrl = {}
HouseType = {}
HouseSize = {}
HouseDirect = {}
HouseInter = {}
HouseEle = {}

def getdata(price,page):

    for j in range(0,page):
        print(j)
        url = 'https://sh.lianjia.com/ershoufang/pudong/PG' + str(j) + price+'/'
        res = requests.get(url,headers = headers)
        soup = BeautifulSoup(res.content,features="html.parser")

        houseInfo = soup.select('div.houseInfo a')
        houseSize = soup.select('div.houseInfo')
        houseTitle = soup.select('div.title a')
        totalPrice = soup.select('div.totalPrice span')
        unitPrice = soup.select('div.unitPrice span')
        position = soup.select('div.positionInfo')

        for i in range(0, 30):
            HousePos[i +30*j] = position[i].getText().split('-')[1]
            HouseYear[i+30*j] = position[i].getText().split(')')[1][0:4]
            TotalH[i+30*j] = position[i].getText().split(')')[0][5:-1]
            High[i+30*j] = position[i].getText().split('(')[0]
            Cells[i+30*j] = houseSize[i].getText().split('|')[0]
            HouseType[i+30*j] = houseSize[i].getText().split('|')[1]
            HouseSize[i+30*j] = houseSize[i].getText().split('|')[2][:-3]
            HouseDirect[i+30*j] = houseSize[i].getText().split('|')[3]
            HouseInter[i+30*j] = houseSize[i].getText().split('|')[4]
            #HouseEle[i+30*j] = houseSize[i].getText().split('|')[5]
            TotalP[i+30*j] = totalPrice[i].getText()
            UnitP[i+30*j] = unitPrice[i].getText()[2:-4]
            HouseUrl[i+30*j] = houseTitle[i].get('href')
        time.sleep(1)

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
    table.write(row, col + 7, '朝向')
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

def main():
    getdata('P3',page)
    write_data(page)

page = 20
main()