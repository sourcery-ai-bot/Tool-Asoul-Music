# encoding: utf-8
import time
import os
from Runner.Network.Downloader import infoGet
from Runner.Network.Downloader import fileGet
from pathlib import Path

# from tqdm.notebook import trange

# 接受数据格式如下
'''
BVList=[
'BV1QL4y1g7sA','BV1QP4y1F7La',
#     'BV1dA411L7Kj','BV1aK4y1a7sd','BV1wf4y1k7as',
#     'BV1CK4y1W7Cc','BV12X4y1K7Ys','BV1Fz4y167Ru',
#     'BV17y4y167xu','BV1wD4y1X7fP','BV1wV41117GP']
'''


class Upload(object):
    def __init__(self, desc):
        self.IsDebug = False
        self.desc = desc

    #    def callback(self,filePath):
    #        print(filePath)
    def deal_audio_list(self, tarID, bvid_list, savePath, botService, local):
        # from rich.progress import track
        infoList = infoGet().getInformation(bvid_list)
        ath = str(Path().cwd()) + savePath
        for item in infoList:
            # print('Downloader Start!')
            sath = f"{ath}/{item[0]}"
            # st = time.time()
            DownPath, is_too_lang = fileGet().getAudio(item, sath)
            if not is_too_lang:
                convertPath = fileGet().convertAudio(item, DownPath, sath)
                # https: // api.bilibili.com / x / web - interface / view?bvid = BV1ip4y1D7iY
                bvid, cid, title = item[0], item[1], item[2]
                if not local:
                    try:
                        botService.postAudio(tarID, convertPath, title + '\n' + 'https://www.bilibili.com/video/' + str(
                            bvid) + "\n #MusicConvert " + str(self.desc), title)  # +
                    except Exception as e:
                        raise Exception(f"Cant post{str(e)}")
                # ed = time.time()
                # print('Download Finish! Time consuming:',str(round(ed-st,2))+' seconds')


# Upload().deal_audio_list(BVList,'/music')


'''
class onedrive(object):
    # robotPush(token,groupID).postAudio(fileroad,info,name):
    def __init__(self, pri, zuhuid, keyid):
        import base64
        import mods.rsatool as rastool
        with open(useTool().filesafer('data/public.cer'), 'r', encoding='utf-8') as f:
            pub = f.read()
        alice_call = {
            'pub': pub,
            'pri': str(base64.b64decode(pri), "utf-8"),
        }
        self.zras = rastool.RsaUtil(mode="STR", **alice_call)
        self.zuhuid = zuhuid
        self.keyid = keyid
        # import json
        with open(useTool().filesafer('o365_token.txt'), 'r', encoding='utf-8') as f:
            token = f.read()
        tokens = self.zras.decrypt_by_private_key(str(token))
        tokens = str(base64.b64decode(tokens), "utf-8")
        with open(useTool().filesafer("o365_token.txt"), 'w+') as f:
            # f.write(json.dumps(self.token))
            f.write(tokens)

    def upload(self, _path):
        from O365 import Account
        credentials = (self.zuhuid, self.keyid)
        account = Account(credentials=credentials)  # credentials=credentials)
        storage = account.storage()
        my_drive = storage.get_default_drive()
        pro = my_drive.get_item_by_path('/share/Music')
        pro.upload_file(item=_path)
        return useTool().filesafer("o365_token.txt")

    def lock_token(self):
        import base64
        with open(useTool().filesafer("o365_token.txt"), 'r', encoding='utf-8') as f:
            tokens = f.read()
        tokens = str(base64.b64encode(tokens.encode("utf-8")), "utf-8")
        con = self.zras.encrypt_by_public_key(tokens).decode('utf-8')
        with open(useTool().filesafer("o365_token.txt"), 'w+') as f:
            f.write(con)
'''

# 机器人实例


import telebot


class Robot(object):
    # robotPush(token,groupID).postAudio(fileroad,info,name):
    def __init__(self, token):
        self.BOT = telebot.TeleBot(token, parse_mode="HTML")  # You can set parse_mode by default. HTML or MARKDOWN

    def sendMessage(self, objectID, msg):
        self.BOT.send_message(objectID, str(msg))

    def replyMessage(self, objectID, msg, reply_id):
        self.BOT.send_message(objectID, str(msg), reply_to_message_id=reply_id)

    def postDoc(self, objectID, files):
        if Path(str(files)).exists():
            with open(files, 'rb') as doc:
                self.BOT.send_document(objectID, doc)
            return files

    def postVideo(self, objectID, files, source, name):
        if Path(str(files)).exists():
            with open(files, 'rb') as video:
                self.BOT.send_video(objectID, video, source, name, name)
            return files

    def postAudio(self, objectID, files, source, name):
        if Path(str(files)).exists():
            with open(files, 'rb') as audio:
                self.BOT.send_audio(objectID, audio, source, name, name)
            return files
