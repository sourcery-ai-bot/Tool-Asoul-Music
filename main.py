# encoding: utf-8


import os
from Runner.EventLib import Tool, Check, Read, checkRss, searchBili, feedBack
from Runner.Network.Uploader import Robot
from pathlib import Path

# import shutil
# import time
# from rich.progress import track
# from rich.console import Console
# from mods.uploadFile import Upload

# ===== 初始化 ======

# 初始化
Check().run()
Tool().console.print("完成初始化", style='blue')
config = Read(str(Path.cwd()) + "/config.yaml").get()

# 注册机器人
pushService = Robot(config.botToken)

# ===== 交互型逻辑区 =====

# Bot
from Runner.Bot import ClinetBot

ClinetBot().run(config)

# ===== 推送型逻辑区 =====

# Rss推送
is_new_Rss = checkRss().run(pushService, config, DontPush=True)

# 自动搜索
cat = searchBili(config)
cat.find()
is_new_Find = cat.doTask(pushService)

# Backup data!
if is_new_Rss or is_new_Find:
    feedBack.run(config, pushService)
