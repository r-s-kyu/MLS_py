# %%
from draw_module.dimention2_draw import Lat_Prs_draw
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

phisical_quantity = ['O3', 'GPH', 'T', 'H2O']


# 変数定義
year=2020 
month=12
day=30
pq = phisical_quantity[2]

# 読み込み
mn = 3
savefile = f'D:/data/test_MLS_griddata/move_and_complement/{pq}/MLS-Aura_{pq}_Mov{mn}daysCom_griddata_2020.npy'
a = np.load(savefile)
data_final = np.zeros((366,55,37,73))
move_mean_count = 0

print("complete to read file!")

# 1月1日からの日数
start_day = datetime(year, 1, 1)
today = datetime(year, month, day)
day_num = (today-start_day).days + 1



Lat_Prs_draw(a, day_num, year, month, day, pq, 180, 300)

