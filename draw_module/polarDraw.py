# %%
# おためし描画、polar

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.path as mpath
import numpy as np
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.util as cutil
from datetime import datetime


def polar(data, day_num, year, month, day, prsLev, pq, polar_num):   
    # ------------------このファイルの最下部にある移動平均(今は別ファイル)を行う際はこの位置で実行する----------------
    
    # if move_mean_count ==1:
        # pq_draw = data_final[day_num,prsLev,:,:]  
    # else:
        # pq_draw = data[day_num,prsLev,:,:]
    pq_draw = data[day_num,prsLev,:,:]
    
    # 10e6をかけて単位をppmvにしている
    if pq != "T" and pq == "GPH":
        pq_draw=pq_draw*10e6 #10e6をかけて単位をppmvにしている
    
    # 格子点作成
    xcord = np.arange(-180, 180.1, 5)
    ycord = np.arange(-90, 90.1, 5)
    X,Y=np.meshgrid(xcord,ycord)
    
    # 領域作成
    fig=plt.figure(figsize=(8,8))
    ax=fig.add_subplot(1,1,1)
    
    # 投影図作成
    if polar_num==0:
        ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=0)) #北半球ポーラー
    elif polar_num == 1:
        ax = plt.axes(projection=ccrs.SouthPolarStereo(central_longitude=0)) #南半球ポーラー
    ax.set_extent([-180,180,-90,-20], ccrs.PlateCarree())
    # ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=180))
    # ax.set_extent([0,359.99,30,90], ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND,fc='lightgreen')
    ax.coastlines(lw=1.0)
    gl=ax.gridlines(linestyle='-', color='gray')
    
    # グリッド調整
    gl.xlocator = mticker.FixedLocator([-180,-135,-90, -45, 0, 45,90,135, 180])
    
    # 等値線
    # cont=plt.contour(X, Y, pq_draw,locator=mticker.MultipleLocator(250), transform=ccrs.PlateCarree(),colors=['black'])
    # cont=plt.contour(X, Y, pq_draw, transform=ccrs.PlateCarree(),colors=['black'])
    # cont.clabel(fmt='%1.0f', fontsize=10)
    
    # 図の周囲を円形に切る
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)
    ax.set_boundary(circle, transform=ax.transAxes)
    
    # 陰影描写
    cyclic_data, cyclic_xcord = cutil.add_cyclic_point(pq_draw, coord=xcord)
    CF = ax.contourf(cyclic_xcord,ycord,cyclic_data, transform=ccrs.PlateCarree(),
                    clip_path=(circle, ax.transAxes) ) # clip_pathを指定して円形にする
    plt.colorbar(CF, orientation="horizontal")
    
    # 方位書き込
    # plt.text(-1, 37, "0", fontsize=20, color='k', transform=ccrs.PlateCarree())
    # plt.text(185, 39, "180", fontsize=20, color='k', transform=ccrs.PlateCarree())
    # plt.text(88, 39, "90E", fontsize=20, color='k', transform=ccrs.PlateCarree())
    # plt.text(-88, 31, "90W", fontsize=20, color='k', transform=ccrs.PlateCarree())
    
    # タイトルを付ける
    plt.title(f'{year}/{month}/{day}', fontsize=20)
    
    # プロット範囲の調整
    # plt.subplots_adjust(hspace=0.8,bottom=0.2)
    
    # ファイルへの書き出し
    # plt.savefig(fig_fname, bbox_inches='tight')
    
    plt.show()
    plt.close()