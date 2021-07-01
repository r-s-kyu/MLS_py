# %%
# MLSデータが格納されているHDF-EOS5ファイルをWebホームページからダウンロード
from myModule import my_func as mf

# 抽出物理量変数
print("Which data do you need? ｛１:'O3', ２:'GPH', ３:'Temperature', ４:'H2O'｝")
pq_num = int(input())
phisical_quantity = ['O3', 'GPH', 'T', 'H2O']
pq = phisical_quantity[pq_num]

# 抽出年変数
print("ダウンロード期間の設定")
print("範囲初日（半角スペースを空けて）例：'2010 4 3'")
slist = list(map(int,input().split()))
print("範囲末日（半角スペースを空けて）例：'2012 12 31'")
elist = list(map(int,input().split()))
print(f'{slist[0]}/{slist[1]}/{slist[2]}～{elist[0]}/{elist[1]}/{elist[2]}　この範囲でダウンロードを行いますか？　ｙ or n')
y = input()

if y == 'y':
    file=f'D:/TestDir/downloadFile/downloadList_mls_{pq}_20040802-.txt'
    
    # 欠損ファイルリスト収集
    misslist = mf.dismiss_counter(file)
    
    # 任意の期間のファイルをダウンロード 
    mf.download_mls_between_time(slist, elist, misslist, file, pq)