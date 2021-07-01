# %%
import h5py
from scipy.interpolate import griddata
import numpy as np
import mlsdata_screeming as ms
from datetime import datetime
import sys

# 抽出物理量変数
phisical_quantity = ['O3', 'GPH', 'Temperature', 'H2O']

print("好きな物理量を番号で選んでね！｛１:'O3', ２:'GPH', ３:'Temperature', ４:'H2O'｝")
inpq = input()
pq = phisical_quantity[int(inpq)-1]
print(f'君は{pq}を解析するんだね！')
print("2005から2020で好きな年を入力してね！範囲外はダメだぞ！")
inye = input()
print(f'それじゃあこれから{inye}の{pq}をグリッドデータにするよ！')
print("y or n")
run = input()
if run == "n":
    sys.exit()

# 移動平均日数
movingday_num = 3 
# 抽出年変数
# year = 2020
year = int(inye)


# ------------------------------------------
# 定数定義
start_day = datetime(year, 1, 1)
end_day = datetime(year,12,31)
day_max = (end_day - start_day).days + 1
md_1 = movingday_num-1
hmd = int((movingday_num-1) /2)

O3_3d = np.zeros((55,37,73))
O3_4d = np.zeros((day_max,55,37,73))*np.nan
O3_4d_comp = np.zeros((day_max,55,37,73))*np.nan
O3_test = np.zeros((day_max,55,37,73))
O3_4d_make = np.zeros((day_max, 55, 37, 73)) 
O3_4d_count = np.zeros((day_max, 55, 37, 73)) 
O3_4d_countsum = np.zeros((day_max, 55, 37, 73)) 
xcord = np.arange(-180, 180.1, 5)
ycord = np.arange(-90, 90.1, 5)
X, Y = np.meshgrid(xcord, ycord)

if pq == "Temperature":
    pq2 = "T"
else:
    pq2 = pq


for day in range(day_max):

    str_day = str(day+1).zfill(3)
    #データ読み込み
    file = f'D:/data/testmls/{pq2}/{year}/{year}d{str_day}.he5'
    try:    
        with h5py.File(file, 'r') as f:
            # 非推奨  data = f['HDFEOS']['SWATHS']['pq']['Data Fields']['pq'].value 
            # 推奨  data = f['HDFEOS']['SWATHS']['pq']['Data Fields']['pq'][()] 
            # 以前は[dataset].valueでdetasetの中身のリストや変数を取り出していたが、
            # 最近は[dataset][()]が推奨されており、.valueにすると、警告文が出る。だが、プログラムは回る。
            
            # datasetから取り出した配列は自動的にnumpy.ndarrayに納められる
            # Data Fields
            data = f['HDFEOS']['SWATHS'][pq]['Data Fields'][pq][()]
            data_L2gpValue = f['HDFEOS']['SWATHS'][pq]['Data Fields']['L2gpValue'][()]
            data_Convergence = f['HDFEOS']['SWATHS'][pq]['Data Fields']['Convergence'][()]               
            data_Precision = f['HDFEOS']['SWATHS'][pq]['Data Fields'][''+pq+'Precision'][()]
            data_L2gpPrecision = f['HDFEOS']['SWATHS'][pq]['Data Fields']['L2gpPrecision'][()]
            data_Quality = f['HDFEOS']['SWATHS'][pq]['Data Fields']['Quality'][()]
            data_Status = f['HDFEOS']['SWATHS'][pq]['Data Fields']['Status'][()]   
            # Geolocation Fields
            lat = f['HDFEOS']['SWATHS'][pq]['Geolocation Fields']['Latitude'][()]
            lon = f['HDFEOS']['SWATHS'][pq]['Geolocation Fields']['Longitude'][()]  
            prs = f['HDFEOS']['SWATHS'][pq]['Geolocation Fields']['Pressure'][()] 
            nLevels = f['HDFEOS']['SWATHS'][pq]['nLevels'][()]
            nTimes = f['HDFEOS']['SWATHS'][pq]['nTimes'][()]
            # print(data)

    except:
        print("error")
        # continue

    # LONの近似
    lon_origin = np.copy(lon)
    lon_near = np.arange(-180, 180.1, 5)
    for i in range(73):
        lon_origin[np.abs(lon_origin - lon_near[i]) < 2.5] = lon_near[i]

    # LATの近似
    lat_origin = np.copy(lat)
    lat_near = np.arange(-90, 90.1, 5)
    for j in range(37):
        lat_origin[np.abs(lat_origin - lat_near[j]) < 2.5] = lat_near[j]

    # データを各条件でscreeming
    ms.screeming(pq, data_L2gpValue, data_Status, data_L2gpPrecision, data_Quality, data_Convergence, prs)

    # 各時刻、各高度（等圧面）のデータを（経度5）*（緯度5）で近似したグリッドデータに入れ込む
    for n in range(len(nTimes)):
        j = int((lat_origin[n]+90)/5)
        i = int((lon_origin[n]+180)/5)
        if j >= 0 or i >= 0:
            for k in range(55):
                if not np.isnan(data_L2gpValue[n,k]):  #np.nanではない時の条件式
                    O3_4d_make[day, k, j, i] += data_L2gpValue[n, k]
                    O3_4d_count[day, k, j, i] += 1
    
    # 指定日数で移動平均
    if day >= md_1 :
        countsum = np.nansum(O3_4d_count[day-md_1:day+1],axis=0)
        countsum[countsum==0] = np.nan
        O3_4d[day-hmd] = np.nansum(O3_4d_make[day-md_1:day+1],axis=0) / countsum
        print("complete to movingmean day" + str(day-hmd).zfill(3))

        # データが欠損している部分を補完
        for k in range(55):
            O3_2d_m = np.ma.masked_invalid(O3_4d[day-hmd,k])
            if isinstance(np.mean(O3_2d_m), float):
                X_valid = X[~O3_2d_m.mask]
                Y_valid = Y[~O3_2d_m.mask]
                O3_2d_valid = O3_2d_m[~O3_2d_m.mask]
                O3_4d_comp[day-hmd,k] = griddata((X_valid, Y_valid), O3_2d_valid, (X,Y), method='cubic')
            else:
                O3_4d_comp[day-hmd,k] = np.nan
        print("complete to complement day" + str(day-hmd).zfill(3))

# 端の日付[1/1, 12/31]などが移動平均したことによって欠損扱いになっていることに注意

savefile = f'D:/data/test_MLS_griddata/move_and_complement/{pq2}/MLS-Aura_{pq2}_Mov{movingday_num}daysCom_griddata_{year}.npy'
np.save(savefile, O3_4d_comp)

print('Complete to make savefile!!!!')


