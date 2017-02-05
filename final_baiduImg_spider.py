#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json
import itertools
import urllib
import requests
import os
import re

running = []

# 对百度图片的链接进行解码
def decode(url):
    # 映射表
    str_table = {
        '_z2C$q': ':',
        '_z&e3B': '.',
        'AzdH3F': '/'
    }

    char_table = {
        'w': 'a',
        'k': 'b',
        'v': 'c',
        '1': 'd',
        'j': 'e',
        'u': 'f',
        '2': 'g',
        'i': 'h',
        't': 'i',
        '3': 'j',
        'h': 'k',
        's': 'l',
        '4': 'm',
        'g': 'n',
        '5': 'o',
        'r': 'p',
        'q': 'q',
        '6': 'r',
        'f': 's',
        'p': 't',
        '7': 'u',
        'e': 'v',
        'o': 'w',
        '8': '1',
        'd': '2',
        'n': '3',
        '9': '4',
        'c': '5',
        'm': '6',
        '0': '7',
        'b': '8',
        'l': '9',
        'a': '0'
    }
    char_table = {ord(key): ord(value) for key, value in char_table.items()}
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)

# 批量生成包含图片的页面链接
def buildUrls(word):
    word = urllib.parse.quote(word)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls

# 解析出链接中的图片网址
def resolveImgUrl(html):
    re_url = re.compile(r'"objURL":"(.*?)"')
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls

# 将图片下载到本地
def downImg(word, file_dirc, img_num = 2):
    urls = buildUrls(word)
    for url in urls:
        print('正在下载有关'+word+'的图片')
        html = requests.get(url, timeout=10).content.decode('utf-8')
        imgUrls = resolveImgUrl(html)
        if len(imgUrls) == 0:
            continue
        index = 0
        for imgUrl in imgUrls:
            try:
                res = requests.get(imgUrl, timeout=15)
                if str(res.status_code)[0] == "4":
                    #print(str(res.status_code) + ":" + imgUrl)
                    #return False
                    continue
            except Exception as e:
                #print("抛出异常：" + imgUrl)
                #print(str(e))
                continue
            with open(file_dirc+'\\'+word+str(index+1)+'.jpg', "wb") as f:
                f.write(res.content)
            index += 1
            if index == img_num:
                break
        if index == img_num:
            break


def translate(words):
    #print(words)
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom=11pegasus11&key=273646050&type=data&doctype=json&version=1.1&q=' + words
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')
    d = json.loads(html)
    #print(html)
    result = d.get('translation')
    return result[0]
    #print(result)

with open('expMaterials.txt', 'r') as f:
    materials = []
    lines = f.readlines()
    for line in lines:
        temp = line.split()
        temp = list(temp)
        materials.append(temp)
    #print(materials)


for i in range(len(materials)):
    word = materials[i][0]
    en_word = word.replace('_',' ')
    cn_word = translate(en_word)
    file_dirc = 'words_img\\'+en_word[0].upper()
    if not os.path.exists(file_dirc):
        os.makedirs(file_dirc)
    downImg(en_word, file_dirc)
    downImg(cn_word, file_dirc)


