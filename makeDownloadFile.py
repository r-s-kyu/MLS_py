# %%
# このファイルでは、ダウンロードリストファイルに記載のない最新の日付のMLSファイルを自動で取得する。

import sys
import requests
from bs4 import BeautifulSoup
import os
from myModule import my_func as mf

# 抽出物理量変数
# print("どの物理量のダウンロードリストを作る？ ｛１:'O3', ２:'GPH', ３:'Temperature', ４:'H2O'｝")
# pq_num = int(input())
phisical_quantity = ['O3', 'GPH', 'T', 'H2O']
# pq = phisical_quantity[pq_num-1]

for pq in phisical_quantity:
    # ダウンロードリストファイル名
    newDir = f'D:/TestDir/downloadFile'
    downloadFile = newDir + f'/downloadList_mls_{pq}_20040802-.txt'
    
    # while os.path.exists(downloadFile):
        # print("すでにダウンロードファイルあるけどもう一回作るのね？ { y or n }")
        # ans = input()
        # if ans == 'y':
            # break
        # else:
            # sys.exit()
        
    # ディレクトリの作成
    if not os.path.exists(newDir[:10]):
        os.mkdir(newDir[:10])
    if not os.path.exists(newDir):
        os.mkdir(newDir)
    
    f = open(downloadFile, "w", encoding="utf-8")
    f.close()
    
    pqPath = f'https://acdisc.gesdisc.eosdis.nasa.gov/data/Aura_MLS_Level2/ML2{pq}.005/'
    res = requests.get(pqPath)
    soup = BeautifulSoup(res.content, 'lxml')
    ele = soup.select('table td[valign] a[href]')
    
    # f = open(downloadFile, "at", encoding="utf-8")
    year_count = 1
    while True:
        try:
            line = ele[year_count].get('href')
            year = int(line[:-1])
            url = pqPath + f'{year}/'
            mf.getURL_year(year, downloadFile, url)
            year_count += 1
        except:
            print("ループ終了")
            break
    
    
    f.close()
    print(f"finish program")
