# encoding: utf-8
# From https://github.com/liuyunhaozz/bilibiliDownloader

import os
import time
import urllib
import requests
import random

from fake_useragent import UserAgent
from PIL import Image
from pathlib import Path

ua_fake = UserAgent()


class infoGet(object):
    def __init__(self):
        self.debug = False

        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Referer': 'http://api.bilibili.com/',
            'Connection': 'keep-alive',
            'Host': 'api.bilibili.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': ua_fake.random,  # 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
            'Cookie': '1P_JAR=2022-02-09-02;SEARCH_SAMESITE=CgQQB;ID=CgQv5QB0',
        }

    def getData(self, bvid):
        url = 'http://api.bilibili.com/x/web-interface/view?bvid=' + bvid
        data = requests.get(url=url, headers=self.header).json().get("data")
        if not data:
            raise Exception("Api 访问异常... Detail:" + str(data))
        return data

    def getCidAndTitle(self, ciddata, p=1):
        title = ciddata['title']
        cid = ciddata['pages'][p - 1]['cid']
        return str(cid), title

    def getInformation(self, bvList):
        infoList = []
        for bvid in bvList:
            item = []
            if len(bvid) == 12:
                data = self.getData(bvid)
                cid, title = self.getCidAndTitle(data)
                item.append(bvid)
            else:
                data = self.getData(bvid[:12], int(bvid[13:]))
                cid, title = self.getCidAndTitle(data)
                item.append(bvid[:12])
            item.append(cid)
            item.append(title)  # 2
            item.append(data.get("owner")["name"])
            item.append(data.get("pic"))

            # item.append('mool_' + str(id + 1))
            infoList.append(item)
        # print(infoList)

        return infoList

    def getMutipleInformation(self, bvid):
        url = 'http://api.bilibili.com/x/web-interface/view?bvid=' + bvid
        data = requests.get(url).json().get('data')
        # base_title = data['title']
        infoList = []
        for page in data['pages']:
            # print(page)
            title = page['part']
            cid = str(page['cid'])
            item = [bvid, cid, title]
            infoList.append(item)

        return infoList


class fileGet(object):
    def __init__(self):
        self.debug = False
        self.saveCover = False
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate ,br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Referer': 'http://api.bilibili.com/',
            'Connection': 'keep-alive',
            'Host': 'api.bilibili.com',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': ua_fake.random,  # 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
            'Cookie': '1P_JAR=2022-02-09-02;SEARCH_SAMESITE=CgQIv5QB;ID=Cg0',

            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        }

    def random_sleep(self, mu=3, sigma=1.7):
        """正态分布随机睡眠
            :param mu: 平均值
            :param sigma: 标准差，决定波动范围
        """
        secs = random.normalvariate(mu, sigma)
        if secs <= 0:
            secs = mu  # 太小则重置为平均值
        time.sleep(secs)

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

    def getAudio(self, item, dirname):
        from functools import partial
        from rich.progress import (
            BarColumn,
            DownloadColumn,
            Progress,
            TaskID,
            TextColumn,
            TimeRemainingColumn,
            TransferSpeedColumn,
        )
        progress = Progress(
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
        )
        baseUrl = 'http://api.bilibili.com/x/player/playurl?fnval=16&'
        if not os.path.exists(dirname):  # 创建为文件夹
            os.makedirs(dirname)
        # st = time.time()
        bvid, cid, title = item[0], item[1], item[2]
        apiUrl = baseUrl + 'bvid=' + bvid + '&cid=' + cid
        # print(title + '---' + str(bvid) + '---->' + apiUrl)
        title = self.well(title)
        audioSong = requests.get(url=apiUrl, headers=self.header).json()
        if not audioSong.get("code") == 0:
            raise Exception("BiliBili Api 狐务器拒绝了请求！!... \n Detail:" + str(audioSong) + ' \n 目标Url:' + str(apiUrl))
        audioUrl = audioSong.get('data').get('dash')['audio'][0]['baseUrl']

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent', ua_fake.random),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),
            ('Referer', 'http://api.bilibili.com/x/web-interface/view?bvid=' + bvid),  # referer 验证
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]
        MusicName = os.path.join(dirname, self.well(title) + '.mp3')
        if not Path(MusicName + '.flac').exists():
            if int(audioSong.get('data').get("timelength")) > 360000:
                is_too_lang = True
            else:
                is_too_lang = False
                urllib.request.install_opener(opener)

                def hook(count, block_size, total_size):
                    """
                    @count:        已经下载的数据块
                    @block_size:    数据块大小
                    @total_size:    文件大小
                    """
                    progress.update(task_id, total=int(total_size))
                    progress.start_task(task_id)
                    progress.update(task_id, advance=block_size)
                    # print('%0f%%' % (100.0 * count * block_size / total_size))

                task_id = progress.add_task("Download..", filename=item[0], start=False)
                with progress:
                    urllib.request.urlretrieve(url=audioUrl, filename=MusicName, reporthook=hook)

                # ed = time.time()
                # 回调函数
                # print(str(round(ed-st,2))+' seconds download finish:',title)
                self.random_sleep()
        else:
            MusicName = MusicName + '.flac'
            is_too_lang = False
            pass
        return MusicName, is_too_lang

    def convertAudio(self, item, audio_path, dirname, setCover=True):
        """
        音频格式转换为flac格式，需要安装ffmpeg
        """
        from pydub import AudioSegment
        movie = AudioSegment.from_file(audio_path)
        channels = movie.channels  # 声道数
        # sample_width = movie.sample_width  # 采样大小
        frame_rate = movie.frame_rate  # 帧率
        musicPath = audio_path + '.flac'
        if not Path(musicPath).exists():
            movie.export(musicPath, format="flac",
                         parameters=["-ac", str(channels), "-ar", str(frame_rate)])
            # os.system("ffmpeg -y -i " + audio_path + " -ac 2 -ab 192000 -ar 44100" + " " + musicPath)
            os.remove(audio_path)
            if setCover:
                try:
                    CoverPath = self.getCover(item, dirname)
                    musicPath = self.setCover(CoverPath, musicPath)
                    musicPath, is_ok = self.setInfo(item, musicPath)
                except Exception as e:
                    print(e)

        return musicPath

    def setCover(self, CoverPath, DownPath):
        # from mutagen.flac import File
        from mutagen.flac import Picture, FLAC
        import os
        audio = FLAC(DownPath)
        image = Picture()
        image.type = 3
        # if  os.path.splitext(albumart)[-1][1:]==('png'):
        if ".png" in CoverPath:
            mime = 'image/png'
        else:
            mime = 'image/jpeg'
        image.desc = 'front cover'
        with open(CoverPath, 'rb') as f:  # better than open(albumart, 'rb').read() ?
            image.data = f.read()
        audio.add_picture(image)
        audio.save()
        # return albumart
        if self.saveCover:
            os.remove(CoverPath)
        return DownPath

    def getCover(self, item, dirname):
        """
        :param item:
        :param dirname:
        :return:
        """
        """
        baseUrl = 'http://api.bilibili.com/x/web-interface/view?'
        if not os.path.exists(dirname):  # 创建为文件夹
            os.makedirs(dirname)
        # st = time.time()
        bvid, cid, title = item[0], item[1], item[2]
        apiUrl = baseUrl + 'bvid=' + bvid
        # print(title + '---' + str(bvid) + '---->' + apiUrl)
        title = self.well(title)
        pic = requests.get(url=apiUrl, headers=self.header).json()
        if not pic.get("code") == 0:
            raise Exception("BiliBili Cover Api 狐务器拒绝了请求！!... \n Detail:" + str(pic) + ' \n 目标Url:' + str(apiUrl))
        coverUrl = pic.get('data').get('pic')
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),
            ('Referer', 'http://api.bilibili.com/x/web-interface/view?bvid=' + bvid),  # referer 验证
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]
        """
        coverUrl = str(item[4])
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),
            ('Referer', 'http://api.bilibili.com/x/web-interface/view?bvid=' + item[0]),  # referer 验证
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]
        urllib.request.install_opener(opener)
        picPath = os.path.join(dirname, item[0] + '.jpg')
        urllib.request.urlretrieve(url=coverUrl, filename=picPath)
        Cover = picPath + "_cover.png"
        img = Image.open(picPath)
        img_size = img.size
        cutSize = img_size[0] if (img_size[0] < img_size[1]) else img_size[1]
        if img_size[0] > img_size[1]:  # 宽比高长
            startX = int((img_size[0] - img_size[1]) / 2)  # 计算中间的位置
            cropped = img.crop((startX, 0, cutSize + startX, cutSize))  # (left, upper, right, lower)
        else:  # 高比宽长
            startY = int((img_size[1] - img_size[0]) / 2)  # 计算中间的位置
            cropped = img.crop((0, startY, cutSize, cutSize + startY))  # (left, upper, right, lower)
        cropped.save(Cover)
        return Cover

    def setInfo(self, item, musicPath):
        from mutagen.flac import FLAC
        audio = FLAC(musicPath)
        try:
            encoding = audio["ENCODING"]
        except Exception as e:
            # print(e)
            encoding = ""
            audio.delete()
        # add FLAC tag data
        audio["TITLE"] = item[2]
        audio["ARTIST"] = item[3]
        audio["ALBUM"] = item[3]
        audio["YEAR"] = str(2022)
        # audio["DESCRIPTION"] = '::> Don\'t believe the hype! <::'
        if len(encoding) != 0:
            audio["ENCODING"] = encoding
        audio.pprint()
        try:
            audio.save()
        except BaseException as e:
            print(e)
            return musicPath, False
        else:
            return musicPath, True
