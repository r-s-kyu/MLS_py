# MLS_py
MLSデータのダウンロードと経度緯度データに加工する実行ファイルを置いている。

# Discription
NASAのMLSデータはダウンロード方法が少々面倒であり、またこのデータは衛星軌道であるため、研究で用いる際は緯度経度座標にグリッド化する必要がある。

以前から、自身のローカルPCでこのMLSデータをダウンロード・グリッド化するプログラムを作ってはいたが、自身しか読めないような粗末なものであったり、コードもぐちゃぐちゃであった。

そのため今回はこの面倒な一連の作業を、簡潔にまとめ、これからMLSデータを扱う人にとって分かりやすく、研究に有効的なものになることを目指す。

*物理量* O3(オゾン) H2O(水蒸気) Temperature(気温) GPH(等圧面高度)　の4つを抽出

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

6. 4つの物理量それぞれのダウンロードリストが生成されたら、あとは以下の2つのファイル'downloadOneYearMLS.py', 'downloadAnyMLS.py'のどちらかを実行すると、任意の年、期間のMLSファイル(.he5)がダウンロードされる（ダウンロード先は'D:/TestDir/mls/'以下である）。

7. 以下ー執筆中  
