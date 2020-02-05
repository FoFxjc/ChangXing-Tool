#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

# 默认请求头(QQ浏览器)
headers_default = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5221.400 QQBrowser/10.0.1125.400"
}
# 默认请求头(手机默认浏览器)
headers_mobile = {
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; HUAWEI MLA-AL10 Build/HUAWEIMLA-AL10; wv) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
                  "Chrome/74.0.3729.136 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
              "q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "X-Requested-With": "com.android.browser",
}


def request(url, headers=None, proxy=None, verify=None, decode="UTF-8"):
    """ 执行Url请求(利用request包)
    :param url: <str> 要请求的目标url
    :param headers: <dict> 请求使用的请求头,默认为默认请求头
    :param proxy: <str/None> 请求使用的代理服务器,默认为None,例如: 127.0.0.1:1080
    :param verify: <bool> 是否开启SSL证书验证
    :param decode: <str> 请求返回结果的解码用编码格式,默认为"UTF-8"
    :return: <str> 解码完成的Url请求返回结果
    """
    if headers is None:
        headers = headers_default
    if proxy is not None:
        proxies = {"http": proxy, "https": proxy}
        response = requests.get(url, headers=headers, proxies=proxies, verify=verify)
        return response.content.decode(decode)
    else:
        response = requests.get(url, headers=headers, verify=verify)
        return response.content.decode(decode)


def get_text(soup, selector):
    """ 提取标签内文本(利用BeautifulSoup包)
    :param soup: <bs4.BeautifulSoup> 需要提取信息的BeautifulSoup对象
    :param selector: <str> 目标标签的CSS选择器
    :return: <str> 目标标签内文本的内容
    """
    try:
        return soup.select(selector)[0].get_text()
    except IndexError:
        return ""


class Request:
    """网页请求工具"""

    def __init__(self, url, info=None):
        self.url = url  # 请求url
        self.proxy = None  # 请求使用代理
        self.headers = None
        if info is not None:
            if "proxy" in info:
                self.proxy = {}
                if isinstance(info["proxy"], str):
                    self.proxy["http"] = info["proxy"]
                    self.proxy["https"] = info["proxy"]
                elif isinstance(info["proxy"], dict):
                    if "http" in info["proxy"] and "https" in info["proxy"]:
                        self.proxy["http"] = info["proxy"]["http"]
                        self.proxy["https"] = info["proxy"]["https"]
        self.response = None
        self.execute()

    def execute(self):
        proxies = self.proxy if self.proxy else None
        self.response = requests.get(self.url, proxies=proxies)

    def content(self, decode="UTF-8"):
        return self.response.content.decode(decode)
