'''
@File    :   main.py
@Time    :   2020-12-19 15:52:56
@Author  :   xs71
@Version :   1.0
@Contact :   liuxs0701@gmail.com
@Desc    :   Collect Bing daily wallpapers
'''
import os
import json
import time
import base64

import requests
Resolution = ['1920x1080', 'UHD']
Folder = time.strftime("%Y/%m/", time.localtime(time.time()))
token = os.environ.get("TOKEN")
repo = os.environ.get("GITHUB_REPOSITORY")
print(token,repo)


def base64Encode(content):
    return base64.b64encode(content).decode('utf-8')


def uploadToGithub(filepath, filecontent, fileinfo):
    url = "https://api.github.com/repos/{}/contents/{}".format(
        repo, filepath)
    data = {
        "message": fileinfo,
        "content": filecontent,
    }
    data = json.dumps(data)
    headers = {"Authorization": "token " + token}
    re = requests.put(url, data=data, headers=headers)


def getInfo():
    url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=' + \
        str(int(time.time()*1000))+'&pid=hp&mkt=zh-CN'
    response = requests.get(url)
    if(response.status_code == 200):
        data = response.json()['images'][0]
        return data


def getFileContent(url):
    url = "https://cn.bing.com"+url
    response = requests.get(url)
    filecontent = base64Encode(response.content)
    return filecontent


if __name__ == "__main__":
    data = getInfo()
    urlbase = data['urlbase']
    namebase = urlbase.split('=')[-1]
    fileinfo = data['startdate']+" "+data['copyright']
    for r in Resolution:
        filename = namebase + "_"+r+".jpg"
        url = urlbase+"_"+r+".jpg"
        filecontent = getFileContent(url)
        filepath = Folder+filename
        uploadToGithub(filepath, filecontent, fileinfo)
