![a](https://s1.328888.xyz/2022/04/13/fPSGZ.jpg)

------------------------------------

<p align="center">
  <a href="https://img.shields.io/badge/LICENSE-Apache2-ff69b4"><img alt="License" src="https://img.shields.io/badge/LICENSE-Apache2-ff69b4"></a>
  <img src="https://img.shields.io/badge/USE-python-green" alt="PYTHON" >
  <img src="https://img.shields.io/badge/Version-220415-9cf" alt="V" >
  <a href="https://dun.mianbaoduo.com/@Sky0717"><img src="https://img.shields.io/badge/Become-sponsor-DB94A2" alt="SPONSOR"></a>
</p>




<h2 align="center">Tool-Asoul-Music</h2>

*A tool for telegram channal delivery,and it can help you to deliver the audio file by asking bilibili api.*

*自动抓取 BiliBili 音乐二创并推送至频道，支持 自动搜索 与 指定收藏夹。有完善的错误处理与数据备份*

*支持本地同步收藏夹库*

*支持自动截取视频封面为音乐封面，并添加作者信息*


> 禁止使用本项目执行商业活动，请注意。

重构自上游项目 github.com/sudoskys/BiliBiliVideoToMusic

## 开始

**[中文](README.md)**

### 1. 安装要求

#### 自动

```
curl -LO https://raw.githubusercontent.com/sudoskys/Tool-Asoul-Music/main/setup.sh; sh setup.sh
```

#### 手动

**Python 3.8 或更高版本,但3.10不能构建加密库**

```shell
python -m pip install --upgrade pip
pip3 install -r requirements.txt
```

FFmpeg环境

- pip 已装

> （仓库Action使用 https://github.com/marketplace/actions/setup-ffmpeg ）

### 2. 准备

#### 本地部署运行

你也许可以Fork本项目，修改下面的命令与setup.sh中的内容～

文件中 `local.py` 为本地同步收藏夹歌曲版本，`main.py` 提供完整推送服务。

**拉取程序**

```bash
sudo apt update
sudo apt install git
sudo apt install -y curl
bash -c "$(curl -L raw.githubusercontent.com/sudoskys/Tool-Asoul-Music/main/setup.sh)"
cd Tool-Asoul-Music
python3 -m pip install -r requirements.txt
python3 main.py password
```

旧机子可选

```bash
sudo apt install python3-pip
sudo apt-get install python3.8
```

**重装最新版本(会删除数据，请谨慎)**

```bash
rm -r Tool-Asoul-Music
bash -c "$(curl -L raw.githubusercontent.com/sudoskys/Tool-Asoul-Music/main/setup.sh)"
```

**编辑config.yaml**

```bash
cd Tool-Asoul-Music
sudo apt install vim
vim config.yaml
```

[Vim使用](https://blog.csdn.net/Algorithmguy/article/details/81937711)

**填充/初始化 数据**

只填充不推送数据.其实是main的复制版

```bash
python3 dataInit.py password
```

**配置程序定时运行**

对于乌班图，配置如下(不同服务器不同路径呃)

*授权*

```bash
cd Tool-Asoul-Music
chmod 777 main.py
date
```

*crontab 执行*

```bash
crontab -l
crontab -e

```

*每天5和17执行任务语法*

```0 5,17 * * *  /user/local/python /path/xxx.py```

> 如果脚本中会有涉及读取配置文件或者读写文件的动作,一般定时任务都不会执行.
> 脚本在执行时,由于是通过crontab去执行的,他的执行目录会变成当前用户的家目录,如果是root,就会在/root/下执行.

所以把执行python的命令放到shell脚本里，然后crontab 定时执行
详见`cron.sh`

*cron用法*

```
chmod +x cron.sh
```

cron 服务的启动与停止，命令如下
1）service cron start /*启动服务*/

    2）service cron stop /*关闭服务*/

    3）service cron restart /*重启服务*/

    4）service cron reload /*重新载入配置*/

    5）service cron status /*查看crond状态*/ 

*使用`crontab -e`*

```
00 08   * * *  /bin/sh /root/Tool-Asoul-Music/cron.sh
```

https://blog.csdn.net/xys2333/article/details/112469461
https://blog.csdn.net/GX_1_11_real/article/details/86535942

**记得在main文件头部添加类似语句**

```
import sys
sys.path.insert(0, '/root/Tool-Asoul-Music')
```

**记得在cron.sh里面修改密码**

#### 托管 Github Action （不推荐）

* Fork 本仓库并设置secrets

Tips: 如果您使用action部署，请注意风控策略。

配置此action，需要在环境内加secrets，一个是 githubtoken，一个是 email。

申请地址[github openapi token](https://github.com/settings/tokens/new)

**Add Repository secrets**

```
${{ secrets.key }}
```

**Add Environment secrets**

```
${{ secrets.GITHUB_TOKEN }}
${{ secrets.GITHUB_EMAIL }}

```

### 3.配置程序设置文件

*USE config.yaml*

```yaml
Lock: False
channalId: -1001741448769
desc: 'music from @somename'
botToken: '8c259c4dc1xxxxxxxxxxxxxxxxxxxxx050b44453a0'
#when you select lock:true,you must use aes to encode all Token! And Dont push your token to github directly. 
onedrive: { statu: True, target: authkey/onedrive.token }
search: { duration: '1', keyword: xxxxxx, order: pubdate, page: '1', search_type: video,  tids_1: '3', tids_2: '28' }
RSS: { statu: True, RssAddressToken: 'https://rssxxxxxxxxxxxxxxxxx' }
DataCallback: { statu: True, UserIdToken: 'bxxxxxxxxxx79' }
ClientBot: { statu: False, owner: 'xxxxxxx' }
```

| Key          | Value                                      | Des                                                                                                                                   |
|--------------|--------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| Lock         | `boolen`                                   | if `True` then ***Token string will be decode by AESTOOL in addition                                                                  |
| channalId    | `-xxxxxxxx`                                | USE tg@getidsbot                                                                                                                      |
| botToken     | `xxxxxxxx`                                 | USE tg@BotFather                                                                                                                      |
| onedrive     | `xxxxxxxx`                                 | undo 还没做                                                                                                                              |
| search       | search: { statu: False,data:{ dur....8' }} | see PS[1] ,statu 控制开关                                                                                                                 |
| RSS          | `xxxxxxxx`                                 | statu mean start use and,token must be the link from [Rsshub](docs.rsshub.app) #bili-->fav list https://xxxxx.com/bilibili/fav/xxx/xx |
| DataCallback | `statu: True, UserIdToken: ''`             | 发送执行的缓存数据(比如服务到期但是没有同步数据see PS[2])。 Token是用户ID或者某些频道ID（需要拉机器人入频道） use tg@getidsbot                                                    |
| ClientBot    | `{statu: False, owner: 'xxxxxxx'}`         | 交互式机器人！可以在线部署 ,owner 为 主人ID                                                                                                          |
|desc| `some desc`                                | 发送消息时的描述                                                                                                                              |

**PS**

- [1 -参数详情](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/search/search_request.md#%E5%88%86%E7%B1%BB%E6%90%9C%E7%B4%A2web%E7%AB%AF)
- 2.请务必先start机器人对话

*生成Token*
项目的 `docs/newToken.md` 中提供了生成的实例。

*关于推送服务*

- 配置音乐频道推送服务
  1.申请一个Bot,向BotFather索取Token
  2.使用ID机器人查看目标频道ID
  3.将机器人添加至频道并只赋予发消息权限

```yaml
channalId: -youchannalIDnumberhere
```
### 机器人

**后台运行**

```shell
nohup python3 main.py > output.log 2>&1 &
```

**查看进程**

```
ps -aux|grep python3
```

**终止进程**

```
kill -9  进程号
```

------------------

### 题外

```shell
python main.py IfYouSetPassword
```

- Github Action
  Github action 可以每天6:20运行一次流程（这需要手动取消yaml文件注释），仓库主人加星会触发流程.

如果您要使用本项目，建议单用一个机器人进行推送，不要将同一机器人接入不同项目，而且机器人最好在私密频道。
减少被识别为滥用机器人的概率。

### Colab 调试

```
!rm -f -r /content/*
!git clone https://github.com/sudoskys/Tool-Asoul-Music
!rsync -r /content/Tool-Asoul-Music/* /content/
!python -m pip install --upgrade pip
!pip3 install -r requirements.txt
```

## 特性

分离了请求与推送，采用队列制，可以方便开发与扩展。
打包Rss类库，模块式编程，低耦合度。

### 目录结构描述

```
.
├── config_exp.yaml # 示例文件
├── cron.sh # cron用
├── data  # 数据目录，智能生成
│   ├── history.yaml
│   └── RssData.json
├── docs # 文档，如何加密
│   └── newToken.md
├── LICENSE
├── main.py  # 运行文件
├── README.md # 自述文件
├── requirements.txt # 依赖说明
├── Runner  # 运行库
│   ├── DataParse.py
│   ├── EventLib.py
│   ├── Network
│   ├── __pycache__
│   └── Task.py
└── setup.sh  # 服务器用


```

### TODO

- [x] 重构代码结构
- [x] 优化冗余代码
- [x] 优化实现流程
- [x] 支持手动添加
- [ ] 支持同步OD盘
- [x] 重构 1 次
- [ ] 重构 2 次
- [ ] 重构 3 次

### 鸣谢

- [BilibiliDownloader](https://github.com/liuyunhaozz/bilibiliDownloader)|下载部分参考|
- [O365](https://github.com/O365/python-o365) |微软云盘同步实现|
- [RSShub](https://docs.rsshub.app/) |数据源RSS|

#### 常见问题

https://stackoverflow.com/questions/338768/python-error-importerror-no-module-named

https://blog.csdn.net/qq_35756383/article/details/109135720

#### Support

如果你感觉这对你有帮助，可以试着我赞助我一点～

[![s](https://img.shields.io/badge/Become-sponsor-DB94A2)](https://dun.mianbaoduo.com/@Sky0717)

