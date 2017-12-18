#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Wenbin Chen


import re
from urllib import request
import time
import random

def download(url):
    try:
        html = request.urlopen(url)
    except request.URLError as e:
        print("下载失败：", e.reason)
        html = None
    return html


def scraper(url, file):
    # 该网页有特殊字符，需要用gb18030字符集才能解码
    html = download(url).read().decode("utf-8")
    # 获取小说名
    title = "龙符"
    print("开始下载《%s》" % title)
    file.write((title + "\n").encode())
    # 循环抓取每一章，直到末尾
    while True:
        #休息5-8秒
        sleeptime=random.randint(15,20)
        time.sleep(sleeptime)
        # 获取章节名
        chapter = re.findall(r'<h1>(.*)</h1>', html)[0]
        print("正在下载：《%s》" % chapter)
        chapter = "\n" + chapter + "\n"
        # 写入文件
        file.write(chapter.encode())
        # 删除无用的<BR>标签
        html = re.sub(r"<br/>", "\n", html)
        #html = re.sub(r"</p>", "", html)
        # 获取小说正文。re.S很关键，跨行匹配模式。
        text = re.findall(r'<div class="bookcontent clearfix" id="BookText">(.*)<div id="p_ad_t3">', html, re.S)
        file.write(text[0].encode())
        # 获取下一章的地址
        base_url = re.findall(r'\)</span></a> <a href="(.*)"><span>下一页', html)
        if not base_url:
            print("下载完毕！")
            break
        # 组合下一章的URI
        next_url = base_url[0]
        html=download(next_url).read().decode("utf-8")

if __name__ == '__main__':
    # 指定第一章的url地址
    start_url = "http://www.longfu8.com/246.html"
    # 指定保存的文件地址
    file_name = "/Users/chenwenbin/Downloads/longfu.doc"
    # 打开文件，爬取小说，写入文件。
    with open(file_name, "ab") as f:
        scraper(start_url, f)


