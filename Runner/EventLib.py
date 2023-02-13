# encoding: utf-8
import time
import yaml
import os
import shutil
import pathlib
from pathlib import Path
# from rich.progress import track
from rich.console import Console


class searchBili(object):
    def __init__(self, config):
        self.config = config

    def find(self):
        from Runner.Task import apiRenew
        if self.config.search.statu:
            # 查询
            result = apiRenew().apiInit(self.config.search.data)
            if key := apiRenew().doData(result):
                # 注册成功
                print(f'resign new task--> {key}')
                # apiRenew().cancelTask(key)  # 取消任务

    def doTask(self, push, dataInit=False):
        HaveNew = False
        from Runner.Task import apiRenew
        from Runner.Network.Uploader import Upload
        if task := yamler().read("rank/content.yaml"):
            for k in task:
                task_todo = yamler().read(task.get(k))

                if not all([self.config.botToken, self.config.channalId]):
                    raise Exception("参数不全!")
                Path(f'{os.getcwd()}/music/').mkdir(parents=True, exist_ok=True)
                    # sync = onedrive(apptoken, appid, appkey)
                if not task_todo:
                    print("Tasker nothing to do")
                    apiRenew().cancelTask(k)
                else:
                    HaveNew = True
                    # print(task_todo)
                    # print(type(task_todo))
                    # 传入
                    bvlist = []
                    if isinstance(task_todo, dict):
                        bvlist.extend(iter(task_todo))
                    time.sleep(1)
                    try:
                        if not dataInit:
                            Upload(self.config.desc).deal_audio_list(self.config.channalId, bvlist, '/music', push,
                                                                     local=False)
                    except BaseException as arg:
                        if not bvlist:
                            bvlist = 'Unknow'
                        push.sendMessage(f'Failed post {str(bvlist)}' + '\n Exception:' + str(arg))
                                            # WrongGet.append(str(Nowtime) + '\n 任务错误' + str(bvlist) + "\n" + str(arg))
                                            # mLog("err", "Fail " + n + '  -' + u).wq()
                    else:
                        apiRenew().cancelTask(k)
                        # sync.lock_token()
                shutil.rmtree(f'{os.getcwd()}/music/', ignore_errors=False, onerror=None)
        return HaveNew


class checkRss(object):
    def __init__(self):
        pass

    def run(self, pushService, config, DontPush=True, dataInit=False):
        HaveNew = False
        from Runner.DataParse import rssParse, biliParse
        from Runner.Network.Uploader import Upload
        if config.RSS.statu:
            Tool().console.print("RSS启用中", style='blue')
            Path(f'{os.getcwd()}/music/').mkdir(parents=True, exist_ok=True)
            items = rssParse(path=f'{os.getcwd()}/data/RssData.json').getItem(
                config.RSS.RssAddressToken
            )
            rssBvidItem = []
            if items:
                rssBvidItem.extend(biliParse().biliIdGet(str(v))[0] for k, v in items.items())
            try:
                if rssBvidItem:
                    HaveNew = True
                    if not dataInit:
                        Upload(config.desc).deal_audio_list(config.channalId, rssBvidItem, '/music', pushService,
                                                            DontPush)
                else:
                    print("RSS No New Data")
            except BaseException as arg:
                try:
                    if not DontPush:
                        pushService.sendMessage(
                            config.channalId,
                            f'Failed post {rssBvidItem}'
                            + '\n Exception:'
                            + str(arg),
                        )
                    else:
                        Tool().console.print(arg, style="red")
                except BaseException as e:
                    print(f"推送日志时发生错误{str(e)}")
                        # WrongGet.append(str(Nowtime) + '\n 任务错误' + str(rssBvidItem) + str(arg))
            finally:
                if not DontPush:
                    shutil.rmtree(f'{os.getcwd()}/music/', ignore_errors=False, onerror=None)
                        # mLog("err", "Fail " + n + '  -' + u).wq()

        else:
            Tool().console.print("RSS已经关闭", style='blue')
        return HaveNew


class Check(object):
    def __init__(self):
        self.file = [
            "/rank/content.yaml",
            "/rank/waiter/init.lck",
            "/config.yaml",
            "/data/history.yaml",
            "/data/RssData.json"
        ]
        self.dir = [
            "/data",
            "/music",
            "/authkey",
            "/rank",
            "/rank/waiter",

        ]
        self.inits = [
            "/data/history.yaml",
            "/data/RssData.json",
            "/rank/content.yaml",
        ]
        self.RootDir = str(pathlib.Path().cwd())

    def mk(self, tab, mkdir=True):

        for i in tab:
            if mkdir:
                pathlib.Path(self.RootDir + i).mkdir(parents=True, exist_ok=True)
            else:
                files = pathlib.Path(self.RootDir + i)
                if not files.exists():
                    files.touch(exist_ok=True)
                    with files.open("w") as fs:
                        fs.write("{}")

    def initConfig(self, path):
        with open(path, "w") as file:
            file.write("{}")
            # 禁用

    def run(self):
        self.mk(self.dir, mkdir=True)
        self.mk(self.file, mkdir=False)


class Read(object):
    def __init__(self, paths):
        data = yamler().read(paths)
        self.config = Tool().dictToObj(data)

    def get(self, args):
        # 解密 机器人 token
        if self.config.Lock:
            Tool().console.print("加密模式开启", style='blue')
            from Runner.DataParse import AESlock
            # import sys
            self.keyword = args.password
            if self.keyword:
                self.config.botToken = AESlock().decrypt(str(self.keyword), self.config.botToken.encode('utf-8'))
            else:
                Tool().console.print("加密密钥未知", style='blue')
                self.config.Lock = False

        # 解密 rss 地址
        if self.config.RSS.statu and self.config.Lock:
            from Runner.DataParse import AESlock
            self.config.RSS.RssAddressToken = AESlock().decrypt(str(self.keyword),
                                                                self.config.RSS.RssAddressToken.encode('utf-8'))
        # 解密备份发送到的人的ID
        if self.config.DataCallback.statu and self.config.Lock:
            from Runner.DataParse import AESlock
            self.config.DataCallback.UserIdToken = AESlock().decrypt(str(self.keyword),
                                                                     self.config.DataCallback.UserIdToken.encode(
                                                                         'utf-8'))
        return self.config


class feedBack(object):
    @staticmethod
    def run(config, pushService):
        if config.DataCallback.statu:
            try:
                filePath = doTarGz().mkTarAll(
                    f'{os.getcwd()}/-dataBack.tar.gz', f"{os.getcwd()}/data"
                )
                pushService.postDoc(config.DataCallback.UserIdToken, filePath)
            except BaseException as arg:
                print("Fail:数据备份推送执行失败")
                pushService.sendMessage(config.DataCallback.UserIdToken,
                                        'Failed post data backup ' + '\n Exception:' + str(arg))
                # mLog("err", "Fail " + n + '  -' + u).wq()
            else:
                print("Success:数据备份推送成功")
        else:
            print("请注意保存data文件夹中的文件...防止重复推送")


class yamler(object):
    # sudoskys@github
    def __init__(self):
        self.debug = False
        self.home = Path().cwd()

    def debug(self, log):
        if self.debug:
            print(log)

    def rm(self, top):
        Path(top).unlink()

    def read(self, path):
        if not Path(path).exists():
            raise Exception(f"Config dont exists in{path}")
        with open(path, 'r', encoding='utf-8') as f:
            result = yaml.full_load(f.read())
        return result

    def save(self, path, Data):
        with open(path, 'w+', encoding='utf-8') as f:
            yaml.dump(data=Data, stream=f, allow_unicode=True)


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


class Tool(object):
    def __init__(self):
        self.console = Console(color_system='256', style=None)
        self.now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def dictToObj(self, dictObj):
        if not isinstance(dictObj, dict):
            return dictObj
        d = Dict()
        for k, v in dictObj.items():
            d[k] = self.dictToObj(v)
        return d


class doTarGz(object):
    # csdn paisen110/article/details/124188478
    def __init__(self):
        self.debug = False
        self.home = Path().cwd()
        # 如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。

    def mkTarAll(self, output_filename, source_dir):
        import tarfile
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
        return output_filename

    # 逐个添加
    def mkTarCareful(self, output_filename, source_dir):
        import tarfile
        tar = tarfile.open(output_filename, "w:gz")
        for root, dir, files in os.walk(source_dir):
            for file in files:
                pathfile = os.path.join(root, file)
                tar.add(pathfile)
        tar.close()
        return output_filename

    def unGz(self, file_name):
        """ungz zip file"""
        import gzip
        f_name = file_name.replace(".gz", "")
        g_file = gzip.GzipFile(file_name)
        open(f_name, "wb+").write(g_file.read())
        g_file.close()

    def unTar(self, file_name):
        """untar zip file"""
        import tarfile
        tar = tarfile.open(file_name)
        names = tar.getnames()
        if not os.path.isdir(f"{file_name}_files"):
            os.mkdir(f"{file_name}_files")
        for name in names:
            tar.extract(name, f"{file_name}_files/")
        tar.close()
