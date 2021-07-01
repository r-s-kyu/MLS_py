# %%
# 一年分or数年分まとめてダウンロード
# MLSデータが格納されているHDF-EOS5ファイルをWebホームページからダウンロード
from myModule import my_func as mf

# 抽出物理量変数
# pq_num = 1
print("Which data do you need? ｛１:'O3', ２:'GPH', ３:'Temperature', ４:'H2O'｝")
pq_num = int(input())
phisical_quantity = ['O3', 'GPH', 'T', 'H2O']
pq = phisical_quantity[pq_num-1]

# 抽出年変数
# year = 2020
print("input year or periods to get MLS data (ex1):'2020', (ex2):'2010 2012'")
year = list(map(int,input().split()))

file=f'D:/TestDir/downloadFile/downloadList_mls_{pq}_20040802-.txt'

# 欠損ファイルリスト収集
misslist = mf.dismiss_counter(file)

if len(year)==1:
    # 抽出した物理量、年のファイルを1年分ダウンロード
    mf.download_mls_year(year[0], misslist, file, pq)
elif len(year) == 2:
    for ye in range(year[0],year[1]):
        mf.download_mls_year(ye, misslist, file, pq)

print('finish program!')
