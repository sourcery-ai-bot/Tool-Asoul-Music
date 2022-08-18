# encoding: utf-8

import argparse

from Runner.EventLib import Tool, Check, Read, checkRss, searchBili, feedBack
from Runner.Network.Uploader import Robot
from Runner.Bot import ClinetBot
from pathlib import Path

# import shutil
# import time
# from rich.progress import track
# from rich.console import Console
# from mods.uploadFile import Upload

# ===== 初始化 ======


# 接收参数
parser = argparse.ArgumentParser(description='运行命令')
parser.add_argument('--password', '-p', help='密码，非必要参数，只有配置开启才会使用', default="")
parser.add_argument('--init', '-i', help='是否执行数据初始化，避免大量推送', default=False)
# parser.add_argument('--test', '-b', help='body 属性，必要参数', required=True)
args = parser.parse_args()

# 初始化
Check().run()
Tool().console.print("完成初始化", style='blue')
config = Read(str(Path.cwd()) + "/config.yaml").get(args)

# 注册机器人
pushService = Robot(config.botToken)

# ===== 交互型逻辑区 =====

# Bot
ClinetBot().run(pushService, config)

# ===== 推送型逻辑区 =====

# Rss推送
is_new_Rss = checkRss().run(pushService, config, DontPush=True, dataInit=False)  # 本地推送且不开启填充数据测试

# 自动搜索
cat = searchBili(config)
cat.find()
is_new_Find = cat.doTask(pushService, dataInit=True)  # 开启填充数据测试

# Backup data!
if is_new_Rss or is_new_Find:
    feedBack.run(config, pushService)
