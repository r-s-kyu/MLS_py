# MLS_py
MLSデータのダウンロードと簡単な図示
## ダウンロード前準備
1. NASAのEARTHDATAのHP https://urs.earthdata.nasa.gov/users/new でアカウントを作る
2. 作成したアカウント名・パスワード (例)name:Taro passward:12345 を忘れずに記録し次の手順で使用。
3. ローカルPCのユーザーのホームディレクトリ下 (例)C:/Users/Taro に.netrc という名前のファイルを作成。
4. .netrc内に先ほど作成したアカウント名とパスワードを用いて以下を入力し、保存。
```
machine urs.earthdata.nasa.gov login Taro password 12345
```
