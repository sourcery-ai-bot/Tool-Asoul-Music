# encoding: utf-8
import os
import json
import re
import time
import requests


# ren sheng ku duan ,bu yao yong python ,
class rssParse(object):
    def __init__(self, path='RssData.json'):
        self.parseMode = True
        self.dataPath = path
        if not os.path.exists(path):
            with open(path, 'w+') as f:
                json.dump({}, f)

    def well(self, name):
        """
        过滤非法字符
        :param name:
        :return: able use str
        """
        # import string
        name = name.replace('"', '_')  # 消除目标对路径的干扰
        name = name.replace("'", '_')
        # remove = string.punctuation
        table = str.maketrans(r'~!#$%^&,[]{}\/？?', '________________', "")
        return name.translate(table)

    def setUrl(self, url, save):
        import feedparser
        fp = feedparser.parse(url)
        name_list = []
        target_list = []
        for m in fp.entries:
            # print('T:',m.title)
            # print('U:',m.links[0].href)
            name_list.append(self.well(m.title))
            target_list.append(m.links[0].href)
        items = dict(zip(name_list, target_list))
        if save:
            with open(self.dataPath, 'w+') as f:
                json.dump(items, f, indent=4, ensure_ascii=False)
        return items

    def getItem(self, url, Save=True):
        older = {}
        with open(self.dataPath, 'r') as f:
            older = json.load(fp=f)
        newer = self.setUrl(url, Save)
        if len(older) == 0:
            return newer
        result_key = newer.keys() - older.keys()
        return {
            name: value for name, value in newer.items() if name in result_key
        } or {}

    def getFullItem(self, url, Save=False):
        return self.setUrl(url, Save)


class biliParse(object):

    def __init__(self):
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Referer': 'https://api.bilibili.com/',
            'Connection': 'keep-alive',
            'Host': 'api.bilibili.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
            'Cookie': '1P_JAR=2022-02-09-02;SEARCH_SAMESITE=Cgv5QB;ID=CgQIsv5QB0',
        }

    def b32_url(self, bili_url):
        """ 禁止重定向"""
        return requests.get(bili_url, headers=self.header, allow_redirects=False).headers['location']

    # repost代表所有转发，post代表动态。
    def timestamp_datetime(self, value):
        formats = r'%Y-%m-%d %H:%M:%S'
        value = time.localtime(value)
        return time.strftime(formats, value)

    def get_oid_type(self, bili_id, bili_type):
        if bili_type == 0:
            b_oid, b_type = (self.BV_AV(bili_id), 1)
        elif bili_type == 1:  # 动态
            api_url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id='
            r1 = requests.get(api_url + str(bili_id), headers=self.header).json()
            dynamic_type = r1['data']['card']['desc']['type']
            b_oid = r1['data']['card']['desc']['rid'] if int(dynamic_type) == 2 else bili_id
            b_type = 11 if int(dynamic_type) == 2 else 17
        else:  # 专栏
            b_oid, b_type = (bili_id, 12)
        return b_oid, b_type  # oid, type

    def BV_AV(self, bv_id):
        bv_id = bv_id.replace('/', '')
        """ BV号还原AV号 """
        table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        tr = {table[i]: i for i in range(58)}
        s = [11, 10, 3, 8, 4, 6]
        xor = 177451812
        add = 8728348608
        r = sum(tr[bv_id[s[i]]] * 58 ** i for i in range(6))
        return (r - add) ^ xor

    def AV_BV(self, av):
        av = "".join(list(filter(str.isdigit, str(av))))
        Str = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        Dict = {Str[i]: i for i in range(58)}
        s = [11, 10, 3, 8, 4, 6, 2, 9, 5, 7]
        xor = 177451812
        add = 100618342136696320
        ret = av
        av = int(av)
        av = (av ^ xor) + add
        r = list('BV          ')
        for i in range(10):
            r[s[i]] = Str[av // 58 ** i % 58]
        return ''.join(r)

    def add_url(self, b_oid, b_type):
        """ 拼接url or https://api.bilibili.com/x/v2/reply?&type={}&oid={}&pn={} """
        return f"https://api.bilibili.com/x/v2/reply/main?&type={b_type}&oid={b_oid}&next="

    def get_bili_id(self, bili_url):
        """ 判断传入链接的类型,并获取id """
        url_re = self.b32_url(bili_url) if "b23.tv" in bili_url else bili_url
        list_re = re.split("/", url_re)
        url_text_re = list_re[len(list_re) - 1]
        # print(url_text_re)  # re 的链接！！
        bili_id_tf = [tf in url_text_re for tf in ["?", "#"]]
        bili_id = re.findall(r".+?[?|#]", url_text_re)[0][:-1] if any(bili_id_tf) else url_text_re
        if bili_id[:2] == "cv" or len(list(bili_id)) < 9:  # 判断专栏
            bili_id = bili_id[2:] if bili_id[:2] == "cv" else bili_id
            bili_type = 2
        else:  # 判断动态或视频
            bili_type = 0 if bili_id[:2] == "BV" else 1
        # print(bili_id) # id在这里
        """ 0.视频 1.动态 2.专栏 """

        return bili_id, bili_type  # id, type

    def biliIdGet(self, urls):
        # urls = self.b32_url(urls) if "b23.tv" in urls else urls
        urls = self.b32_url(urls) if "b23.tv" in urls else urls
        b = re.findall(r'(?:bv.*?).{10}', urls)
        B = re.findall(r'(?:BV.*?).{10}', urls)
        bv = B + b
        Av = [self.BV_AV(i) for i in bv]
        a = re.compile(r'(?:av)\d+\.?\d*').findall(urls)
        A = re.compile(r'(?:AV)\d+\.?\d*').findall(urls)
        # a = re.findall(r"(?:av.*?).{9}", urls)
        # A = re.findall(r"(?:AV.*?).{9}", urls)
        deal = Av + a + A
        Bv = [self.AV_BV(i) for i in deal]
        if not (ids := Bv):
            return False
        for i in ids:
            if strs := re.search(r"\W", str(i)):
                ids = False
        return list(set(ids))


class AESlock(object):
    def __init__(self):
        pass

    def add_to_16(self, text):
        if len(text.encode('utf-8')) % 16:
            add = 16 - (len(text.encode('utf-8')) % 16)
        else:
            add = 0
        text = text + ('\0' * add)
        return text.encode('utf-8')

    # 加密
    def encrypt(self, key, text):
        from Crypto.Cipher import AES
        from binascii import b2a_hex
        key = self.add_to_16(key)
        mode = AES.MODE_ECB
        text = self.add_to_16(text)
        cryptos = AES.new(key, mode)

        cipher_text = cryptos.encrypt(text)
        return b2a_hex(cipher_text)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, key, text):
        from Crypto.Cipher import AES
        from binascii import a2b_hex
        key = self.add_to_16(key)
        mode = AES.MODE_ECB
        cryptor = AES.new(key, mode)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return bytes.decode(plain_text).rstrip('\0')
