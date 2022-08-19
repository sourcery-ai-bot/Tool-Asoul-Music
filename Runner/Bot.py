# -*- coding: utf-8 -*-
# @Time    : 8/17/22 6:00 PM
# @FileName: Bot.py
# @Software: PyCharm
# @Github    ：sudoskys
import os
import shutil
import time
import joblib

from Runner.DataParse import biliParse
from Runner.EventLib import Tool
from Runner.Network.Uploader import Upload


class CallingCounter(object):
    def __init__(self):
        pass

    def get(self, key):
        key = str(key) + time.strftime("%Y-%m-%d-%H", time.localtime())
        if not hasattr(self, 'count'):
            self.count = dict()
        if key in self.count:
            self.count[key] += 1
        else:
            self.count[key] = 0
        return self.count[key]


class ClinetBot(object):
    def __init__(self):
        pass

    @staticmethod
    def life():
        try:
            if joblib.load('life.pkl') == "on":
                return True
            else:
                return False
        except Exception as e:
            print("Wrong:life.pkl do not exist" + str(e))
            joblib.dump("off", 'life.pkl')
            return False

    def run(self, pushService, config):
        if config.ClientBot.statu:
            Tool().console.print("Bot Running", style='blue')
            import telebot
            import joblib
            bot = telebot.TeleBot(config.botToken)
            count = CallingCounter()
            joblib.dump("on", 'life.pkl')
            """
            def master(message):
                userID = message.from_user.id
                if str(userID) == config.ClientBot.owner:
                    try:
                        chat_id = message.chat.id
                        command = message.text
                        if command == "off":
                            joblib.dump("off", 'life.pkl')
                            bot.reply_to(message, 'success！')
                        if command == "on":
                            joblib.dump("on", 'life.pkl')
                            bot.reply_to(message, 'success！')
                    except Exception as e:
                        bot.reply_to(message, "Wrong:" + str(e))
            """

            @bot.message_handler(commands=['start'])
            def send_welcome(message):
                bot.reply_to(message, "发送链接，我会发送回音频")

            @bot.message_handler(commands=['about'])
            def send_about(message):
                bot.reply_to(message, "https://github.com/sudoskys/Tool-Asoul-Music")

            @bot.message_handler(content_types=['text'])
            def replay(message, items=None):
                userID = message.from_user.id
                if str(userID) == config.ClientBot.owner:
                    try:
                        # chat_id = message.chat.id
                        command = message.text
                        if command == "off":
                            joblib.dump("off", 'life.pkl')
                            bot.reply_to(message, 'success！')
                        if command == "on":
                            joblib.dump("on", 'life.pkl')
                            bot.reply_to(message, 'success！')
                    except Exception as e:
                        bot.reply_to(message, "Wrong:" + str(e))
                # Name = message.from_user.first_name
                commands = message.text
                ids = biliParse().biliIdGet(commands)
                if ids:
                    if count.get(userID) < 30:
                        if ClinetBot.life():
                            rssBvidItem = ids
                            bot.reply_to(message, "OK,NewTask:" + str(rssBvidItem))
                            if items:
                                for k, v in items.items():
                                    rssBvidItem.append(biliParse().biliIdGet(str(v))[0])
                            try:
                                if not len(rssBvidItem) == 0:
                                    Upload(config.desc).deal_audio_list(userID, rssBvidItem, '/music', pushService,
                                                                        local=False)
                                else:
                                    print("No New Data")
                            except BaseException as arg:
                                try:
                                    bot.reply_to(message,
                                                 'Failed post ' + str(rssBvidItem) + '\n Exception:' + str(
                                                     arg))
                                except BaseException as e:
                                    print("推送错误")
                                # WrongGet.append(str(Nowtime) + '\n 任务错误' + str(rssBvidItem) + str(arg))
                            finally:
                                pass
                                # shutil.rmtree(os.getcwd() + '/music/', ignore_errors=False, onerror=None)

                        else:
                            Tool().console.print("Bot已经关闭", style='blue')
                    else:
                        bot.reply_to(message, "服务维护中")

            bot.infinity_polling()
