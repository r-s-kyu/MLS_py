#-*- using:utf-8 -*-
import urllib.request

def checkURL(url):
    try:
        f = urllib.request.urlopen(url)
        ans = True
        f.close()
    except:
        ans = False
    return ans

# if __name__ == '__main__':
#     url = "http://qiita.com/"
#     checkURL(url)