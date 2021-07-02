# MLS_py
MLSデータのダウンロードと経度緯度データに加工する実行ファイルを置いている。

# Discription
NASAのMLSデータはダウンロード方法が少々面倒であり、またこのデータは衛星軌道であるため、研究で用いる際は緯度経度座標にグリッド化する必要がある。  
以前から、自身のローカルPCでこのMLSデータをダウンロード・グリッド化するプログラムを作ってはいたが、自身しか読めないような粗末なものであったり、コードもぐちゃぐちゃであった。  
そのため今回はこの面倒な一連の作業を、簡潔にまとめ、これからMLSデータを扱う人にとって分かりやすく、研究に有効的なものになることを目指す。  

**物理量**：O3(オゾン) H2O(水蒸気) Temperature(気温) GPH(等圧面高度)

# Requirement
- python3.8.5
＊これよりバージョンが古くてもある程度は動く
```
$ pip install numpy
$ pip install bs4
$ pip install pandas
$ pip install requests
$ pip install import h5py
$ pip install import scipy
```

# Usage
## ダウンロード前準備
1. NASAのEARTHDATAのHP https://urs.earthdata.nasa.gov/users/new でアカウントを作る
2. 作成したアカウント名・パスワード (例)name:Taro passward:12345 を忘れずに記録し次の手順で使用。
3. ローカルPCのユーザーのホームディレクトリ下 (例)C:/Users/Taro に.netrc という名前のファイルを作成。
4. .netrc内に先ほど作成したアカウント名とパスワードを用いて以下を入力し、保存。
```
machine urs.earthdata.nasa.gov login Taro password 12345
```

## ダウンロードURLリストを作成
5. makeDownloadFile.pyを実行すると、自動的に'D:/TestDir/downloadFile'というディレクトリが作られ、この中にダウンロードURLリストが生成される。
　観測結果のある最初の日付(2004/8/2)から最新の日付までのファイルのダウンロード先のURLが古い順に1行ずる羅列されている。

## MLS衛星軌道データファイル(.he5)をダウンロード
6. 4つの物理量それぞれのダウンロードリストが生成されたら、あとは以下の2つのファイル  
'downloadOneYearMLS.py' (任意の年 or 任意の年数)  
'downloadAnyMLS.py' (任意の期間)  
のどちらかを実行すると、任意の年、期間のMLSファイル(.he5)がダウンロードされる（ダウンロード先は 'D:/TestDir/mls/' と設定している）。

## 衛星軌道→緯度経度へグリッド化
7. 以下のようにファイルを実行し、実行プログラムの指示通りに物理量や年を入力するとグリッド化が行われる。
```
$ python transform_MLSgriddata_move_complement.py 
```
グリッド化したデータは一年分を1つの.npyファイルに保存している。  
＊各データは精度や信頼性によって条件を設ける必要があり、物理量によってその条件が違うため、詳しく知りたい方はこちらのURLを参照。
<https://acdisc.gesdisc.eosdis.nasa.gov/data/Aura_MLS_Level2/ML2O3.005/doc/Aura-MLS_DataQuality_v5-0x-revA.pdf>

### グリッド化詳細
1. 衛星軌道データを緯度経度を5度ずつで分割した領域に入れ込み、そのエリアに入ったデータを平均し、この領域中心の緯度経度の値のデータとして近似する。
2. しかし、1日のデータ量だとデータが一つもない5°×5°の領域が全体の50％以上となるため、三日分のデータで移動平均を行い、中間の日付のデータとみなしている。
3. その後、観測値がない領域に関しては、2次元補完を行い、加工後のデータ[days(365 or 365) × prs(55) × latitude(37) × longitude(73)]を.npyファイルに保存している。

## グリッド化したデータの図示
8. -以下は現在執筆中-
