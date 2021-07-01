import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

def callPcord():
    pcord = [1.0000000e+03, 8.2540417e+02, 6.8129205e+02, 5.6234131e+02, 4.6415887e+02,
                3.8311868e+02, 3.1622775e+02, 2.6101572e+02, 2.1544347e+02, 1.7782794e+02,
                1.4677992e+02, 1.2115276e+02, 1.0000000e+02, 8.2540421e+01, 6.8129204e+01,
                5.6234131e+01, 4.6415890e+01, 3.8311867e+01, 3.1622776e+01, 2.6101572e+01,
                2.1544348e+01, 1.7782795e+01, 1.4677993e+01, 1.2115276e+01, 1.0000000e+01,
                8.2540417e+00, 6.8129206e+00, 5.6234131e+00, 4.6415887e+00, 3.8311868e+00,
                3.1622777e+00, 2.6101573e+00, 2.1544347e+00, 1.7782794e+00, 1.4677993e+00,
                1.2115277e+00, 1.0000000e+00, 6.8129206e-01, 4.6415889e-01, 3.1622776e-01,
                2.1544346e-01, 1.4677992e-01, 1.0000000e-01, 4.6415888e-02, 2.1544347e-02,
                9.9999998e-03, 4.6415888e-03, 2.1544348e-03, 1.0000000e-03, 4.6415889e-04,
                2.1544346e-04, 9.9999997e-05, 4.6415887e-05, 2.1544347e-05, 9.9999997e-06,]
    return pcord

def Lat_Prs_draw(data, day_num, year, month, day, pq, min_value, max_value):
    pcord = callPcord()

# 格子点作成
    xcord = np.arange(-90, 90.1, 5)
    pcord = np.array(pcord)
    pcord = pcord[pcord>0.00045]
    pcord_len = len(pcord)

    pq_draw = data[day_num, :pcord_len, :, :]

    if pq != "T" and pq == "GPH":
        pq_draw=pq_draw*10e6 #10e6をかけて単位をppmvにしている

    # 帯状平均
    pq_draw = np.ma.masked_invalid(pq_draw)
    zonalMean = np.mean(pq_draw, axis=2)
    zonalMean[zonalMean.mask] = np.nan
    X,Y=np.meshgrid(xcord,pcord)

    # 領域作成
    fig=plt.figure(figsize=(8,8))
    ax=fig.add_subplot(1,1,1)

    # カラー設定
    div=100.0                    #図を描くのに何色用いるか
    delta=(max_value-min_value)/div
    interval=np.arange(min_value,abs(max_value)*2+delta,delta)[0:int(div)+1]

    # 描画
    plt.rcParams['image.cmap'] = 'jet' #カラーマップ設定
    cont = ax.contourf(X, Y, zonalMean, interval, antialiased=True)
    # cont = ax.contour(X, Y, zonalMean, locator=ticker.MultipleLocator(10), colors=['black'])
    # cont.clabel(fmt='%1.0f', fontsize=10)

    fig.colorbar(cont, orientation= "vertical")

    # # title
    ax.set_title('', fontsize=20)

    # 軸範囲設定
    ax.set_yscale("log")
    ax.set_ylim(1.0e+3,1.0e-3)
    ax.set_xlim(-90, 90)

    # # 軸ラベル設定
    ax.set_xlabel('LAT', fontsize=12)
    ax.set_ylabel('Pressure(hPa)', fontsize=12)

    # x軸目盛り設定
    xvar=np.arange(-90,91,20)

    a = [str(i)+"S" for i in range(-90,-9,20)]
    b = [str(i)+"N" for i in range(10,91,20)]
    xlab = a + b
    ax.set_xticks(xvar)
    ax.set_xticklabels(xlab)

    # y軸目盛
    ylon=([1000, 500, 100, 50, 10, 5, 1])
    chei=(["1000", "500", "100", "50", "10", "5", "1"])
    ax.set_yticks(ylon)
    ax.set_yticklabels(chei)
    plt.title(f'{pq}  Latitude-Pressure {year}/{month}/{day}', fontsize=20)


    # # ファイルへの書き出し
    # fig_fname=r"ファイル名"
    # plt.savefig(fig_fname, bbox_inches='tight')

    plt.show()
    plt.close()