# %%
# このファイルでは、ダウンロードリストファイルに記載のない最新の日付のMLSファイルを自動で取得する。

from pandas.core.indexing import check_bool_indexer
import requests
from bs4 import BeautifulSoup
from myModule import my_func as mf
import numpy as np


# 最新年
# year = 2021
# 抽出物理量変数
phisical_quantity = ['O3', 'GPH', 'T', 'H2O']
pq = phisical_quantity[1]
# ダウンロードリストファイル名
downloadFile = f'D:/TestDir/downloadFile/downloadList_mls_{pq}_20040802-.txt'
dfr = open(downloadFile, "r", encoding="utf-8")

# 現「ダウンロードリストファイル」の最新日を抽出
allText = dfr.readlines()
dfr.close()
ld_line = allText[len(allText)-1].rstrip('\n')
ld_num = ld_line[-7:-4]
year = int(ld_line[-12:-8])

while True:
    # MLSファイルの置き場
    url = f'https://acdisc.gesdisc.eosdis.nasa.gov/data/Aura_MLS_Level2/ML2{pq}.005/{year}/'
    
    
    # 2004年から現在までで、ファイルが存在していない日付をリストにまとめる
    fmonth, fday = mf.allDayChangeToDate(year, int(ld_num))
    missList = mf.dismiss_counter(downloadFile)
    
    # 任意年の不在日付リスト作成
    missList_int = missList.astype(np.int32)
    ml_year = missList_int[missList_int>(year*1000)]
    ml_year = ml_year[ml_year < (year+1)*1000]
    
    
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    ele = soup.select('table td[valign] a[href]')
    
    
    start_num = int(ld_num) - len(ml_year) + 1
    double_sn = start_num*2
    
    
    f = open(downloadFile, "at", encoding="utf-8")
    day_count = double_sn
    
    while day_count<len(ele):
        file_name = ele[day_count-1].get('href')
        dlurl = url + file_name
        f.write(dlurl + '\n')
        mf.download_mls_OneFile(dlurl, pq)
    
        day_count += 2

    f.close()

    if mf.checkLatestYear(pq) == year:
        break
    elif mf.checkLatestYear(pq) > year:
        year += 1
    else:
        print("error!")


m, d = mf.allDayChangeToDate(year, int(dlurl[-7:-4]))
print(f'complete to add latest file at {str(m).zfill(2)}/{str(d).zfill(2)}/{year}!')
