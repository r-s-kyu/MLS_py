from datetime import date , timedelta
import numpy as np
import pandas as pd
import requests
import calendar
from bs4 import BeautifulSoup
import os
import sys



def allDayChangeToDate(year, day_count):
    month = 1
    sumDay2 = (date(year, month, calendar.monthrange(year, month)[1])-date(year, 1, 1)).days + 1
    while sumDay2<day_count:
        month +=1
        sumDay2 = (date(year, month, calendar.monthrange(year, month)[1])-date(year, 1, 1)).days + 1
    
    day = 1
    sumDay3 = (date(year, month, day)-date(year, month, 1)).days + 1
    while sumDay3 < day_count:
        day += 1
        sumDay3 = (date(year, month, day)-date(year, 1, 1)).days + 1
    return month, day


def outputLatestDate(URL):
    year = int(URL[-2].get('href')[-12:-8])
    sumDay = int(URL[-2].get('href')[-7:-4])   
    month, day = allDayChangeToDate(year, sumDay)
    return year, month, day

def downloadListLatestDay(file):
    # 定数定義：ダウンロードリストにある最新の日付
    f = open(file, "r", encoding="utf-8")
    text = f.readlines()
    f.close()
    
    lLine = text[len(text)-1].rstrip('\n')
    lyear = int(lLine[-12:-8])
    dcount = int(lLine[-7:-4])
    lmonth, lday = allDayChangeToDate(lyear, dcount)
    return lyear, lmonth, lday


def dismiss_counter(file):

    lyear, lmonth, lday = downloadListLatestDay(file)
    f = open(file, "r", encoding="utf-8")

    misslist=np.array([])
    start_year = 2004

    for year in range(start_year, lyear+1):
        
        count = 0
        endDay = date(year, 12, 31)
        if year == 2004:
            startDay = date(2004,8,2)
        else:
            startDay = date(year,1,1)

        dayNum = (endDay - startDay).days + 1
        day = (startDay-date(year,1,1)).days + 1
        if year == lyear:
            dayNum = (date(lyear, lmonth, lday)-date(lyear, 1, 1)).days + 1

        while count < dayNum:
            line = f.readline().rstrip('\n')
            if int(line[-7:-4])==day:
                day +=1
            else:
                while int(line[-7:-4])>day:
                    misslist = np.append(misslist,[f'{year}' + str(day).zfill(3)])
                    day += 1
                    dayNum -= 1
                    if int(line[-7:-4])==day:
                        day += 1
                        break
            count += 1  
    return misslist
    

def download_mls_year(year, misslist, file, pq):
    lyear, lmonth, lday = downloadListLatestDay(file)
    f = open(file, "r", encoding="utf-8")

    start_day = date(year, 1, 1)
    eday = date(year, 12, 31)
    start_2004_year = date(2004, 8, 2)
    start_day_minus1 = date(year-1, 12, 31)
    end_latest_year = date(lyear, lmonth, lday)
    day_year = (eday - start_day).days + 1
    day_2004_year = (date(2004,12,31) - start_2004_year).days +1
    day_latest_year = (end_latest_year - date(lyear, 1, 1)).days +1
    day_before = (start_day_minus1 - start_2004_year).days +1
          
    missF = pd.Series(np.zeros((lyear+1-2004),np.int32) ,
                        index=[str(i) for i in range(2004,lyear+1)])

    for i in misslist:
        missF[i[0:4]] += 1
    syear = 2004
    cskip = 0
    while syear < year:   
        cskip += missF[str(syear)]
        syear += 1

    if year == 2004:
        day_before = 0
        day_year = day_2004_year
    elif year == lyear:
        day_year = day_latest_year

    day_skip = day_before - cskip
    for i in range(day_skip):
        URL = f.readline().rstrip('\n')   
    
    dirname = f'D:/TestDir/mls/{pq}/{year}'
    if not os.path.exists(dirname[:10]):
        os.mkdir(dirname[:10])
    if not os.path.exists(dirname[:14]):
        os.mkdir(dirname[:14])
    if not os.path.exists(f'D:/TestDir/mls/{pq}'):
        os.mkdir(f'D:/TestDir/mls/{pq}')
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    
    for i in range(day_year-missF[str(year)]):       
        # 行末の改行を削除
        URL = f.readline().rstrip('\n')
        # print(URL)
        # # 保存ファイル名
        savename = dirname + f'/{year}d{URL[-7:-4]}.he5'        
        # # ファイルダウンロード
        result = requests.get(URL)
        try:
            result.raise_for_status()
            ff = open(savename,'wb')
            ff.write(result.content)
            ff.close()
            print('contents of URL written to '+ f'{URL[-12:-4]}')
        except:
            print('requests.get() returned an error code '+str(result.status_code))
            sys.exit()
    f.close()
    print(f'complete to download MLS_{pq} files in {year}!!')
    return

def download_mls_between_time(slist, elist, misslist, file, pq):
    syear, smonth, sday = slist
    eyear, emonth, eday = elist
    f = open(file, "r", encoding="utf-8")
    td = timedelta(days = 1)
    sdate = date(syear, smonth, sday)
    edate = date(eyear, emonth, eday)
    start_2004_year = date(2004, 8, 2)
    start_day_minus1 = sdate - td
    sy_from0101 = (sdate - date(syear,1,1)).days + 1
    ey_from0101 = (edate - date(eyear,1,1)).days + 1
    sumDay = (edate - sdate).days + 1
    day_before = (start_day_minus1 - start_2004_year).days +1
    ml_int = misslist.astype(np.int32)
    ml_befere = ml_int[ml_int<syear*1000+sy_from0101]
    ml_cut = ml_int[ml_int>=syear*1000+sy_from0101]
    ml_cut = ml_cut[ml_cut<=eyear*1000+ey_from0101]
    bskip =len(ml_befere)
    cskip =len(ml_cut)

    day_skip = day_before - bskip
    for i in range(day_skip):
        URL = f.readline().rstrip('\n')   
    
    # ディレクトリの作成
    dirname = f'D:/TestDir/mls/{pq}'
    if not os.path.exists(dirname[:10]):
        os.mkdir(dirname[:10])
    if not os.path.exists(dirname[:14]):
        os.mkdir(dirname[:14])
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for year in range(syear, eyear+1):
        dirname2 = dirname + f'/{year}'
        if not os.path.exists(dirname2):
            os.mkdir(dirname2)
    
    count = 1
    while count <= sumDay-cskip:       
        # 行末の改行を削除
        URL = f.readline().rstrip('\n')
        # print(URL)
        # # 保存ファイル名
        savename = dirname + f'/{URL[-12:-8]}/{URL[-12:]}'

        if not os.path.exists(savename):  
            # ファイルダウンロード
            result = requests.get(URL)
            try:
                result.raise_for_status()
                ff = open(savename,'wb')
                ff.write(result.content)
                ff.close()
                print('contents of URL written to '+ f'{URL[-12:-4]}')
            except:
                print('requests.get() returned an error code '+str(result.status_code))
                print('Error!! Uncomplete all days you choose.')
                sys.exit()
        count += 1  

    f.close()
    print('finish all download!')
    return


def download_mls_OneFile(URL, pq):
    year = URL[-12:-8]
    # # 保存ファイル名
    dirname = f'D:/TestDir/mls/{pq}/{year}'
    
    if not os.path.exists(dirname[:10]):
        os.mkdir(dirname[:10])
    if not os.path.exists(dirname[:14]):
        os.mkdir(dirname[:14])
    if not os.path.exists(f'D:/TestDir/mls/{pq}'):
        os.mkdir(f'D:/TestDir/mls/{pq}')
    if not os.path.exists(dirname):
        os.mkdir(dirname)
                
    savename = dirname + f'/{year}d{URL[-7:-4]}.he5'


    # # ファイルダウンロード
    result = requests.get(URL)
    try:
        result.raise_for_status()
        ff = open(savename,'wb')
        ff.write(result.content)
        ff.close()
        print('contents of URL written to '+ f'{URL[-12:-4]}')
    except:
        print('requests.get() returned an error code '+str(result.status_code))

    return


def getURL_year(year, file, url):
    # HPから各日付のファイルをダウンロードするURLを取得
    f = open(file, "at", encoding="utf-8")
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    ele = soup.select('table td[valign] a[href]')
    day_count = 2    
    url_list = np.array([])
    url_day = np.array([],dtype = np.int32)

    while day_count<len(ele):
        file_name = ele[day_count-1].get('href')
        dlurl = url + file_name
        url_list = np.append(url_list,[dlurl])
        url_day = np.append(url_day,[int(dlurl[-7:-4])])
        day_count += 2
    
    url_series = pd.Series(data=url_list, index=url_day)
    url_series = url_series.sort_index()
    # url_frame = pd.DataFrame({'url':url_list,'day':url_day})
    # url_frame = url_frame.sort_values('day')

    for url in url_series.values:
        f.write(url + '\n')
    
    print(f"complete {year}")
    f.close()

    return

# HP上にディレクトリが存在している最新の年を確認
def checkLatestYear(pq):
    pqPath = f'https://acdisc.gesdisc.eosdis.nasa.gov/data/Aura_MLS_Level2/ML2{pq}.005/'
    res = requests.get(pqPath)
    soup = BeautifulSoup(res.content, 'lxml')
    ele = soup.select('table td[valign] a[href]')
    year_count = 1

    while True:
        try:
            line = ele[year_count].get('href')
            year = int(line[:-1])
            year_count += 1
        except:
            break
    return year        
