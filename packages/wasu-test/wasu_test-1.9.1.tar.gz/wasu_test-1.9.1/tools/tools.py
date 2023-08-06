"""

@FileName: tools.py
@Author: chenxiaodong
@CreatTime: 2020/9/21 11:01
@Descriptions: 

"""
import subprocess
import zipfile
import pymysql
import requests
import xlrd
import yaml
from threading import Thread
from typing import Optional, Dict
from appium import webdriver

from benedict import benedict
from pathlib import Path
from selenium import webdriver


class console_line_tools:

    def __init__(self):
        """
        :param:
        :return:

        """
        pass

    @staticmethod
    def dell_command_lines(args):
        subprocess.run(args=args, shell=True)


# 单例模式
def singleton(cls):
    _instance = {}

    def inner(*args, **kw):
        key = str(args) + str(kw)
        if key not in _instance.keys():
            _instance[str(cls) + key] = cls(*args, **kw)
        return _instance[str(cls) + key]

    return inner


class Adb:
    def __init__(self):
        """
        :param:
        :return:

        """
        pass

    def adb_kill_server(self):
        """
        :param:
        :return:

        """
        self.run("adb kill-server")

    def adb_start_server(self):
        """
        :param:
        :return:

        """
        self.run("adb start-server")

    def adb_shell(self, args):
        """
        :param:
        :return:

        """
        self.run("adb shell " + args)

    def connect(self, device: str):
        """
        :param:
        :return:

        """
        self.run("adb connect " + device)

    def devices(self):
        """
        :param:
        :return:
        获取已连接的设备


        adb 会针对每个设备输出以下状态信息：

        序列号：由 adb 创建的字符串，用于通过端口号唯一标识设备。 下面是一个序列号示例：emulator-5554
        状态：设备的连接状态可以是以下几项之一：
            offline：设备未连接到 adb 或没有响应。
            device：设备现已连接到 adb 服务器。请注意，此状态并不表示 Android 系统已完全启动并可正常运行，因为在设备连接到 adb 时系统仍在启动。不过，在启动后，这将是设备的正常运行状态。
            no device：未连接任何设备。
        说明：如果您包含 -l 选项，devices 命令会告知您设备是什么。当您连接了多个设备时，此信息很有用，可帮助您将它们区分开来。

        """
        msg = [x.decode("utf-8") for x in self.run("adb devices").splitlines()]
        cut = slice(1, -1)
        devices = [i.split("\t")[0] for i in msg[cut]]
        status = [i.split("\t")[1] for i in msg[cut]]
        if status[0] == "device":
            return devices[0]
        else:
            raise BaseException("No device is online")

    def adb_install(self, args="-a", package=None):
        """
        :param:
        :return:

        """
        self.run("adb install " + args + package)

    def adb_uninstall(self, args="-a", package=None):
        """
        :param:
        :return:

        """
        self.run("adb uninstall " + args + package)

    def up(self):
        self.run("")

    def down(self):
        self.run("")

    def right(self):
        self.run("")

    def left(self):
        self.run("")

    def ok(self):
        self.run("")

    @staticmethod
    def run(args):
        p = subprocess.run(args=args, shell=True, stdout=subprocess.PIPE)
        print(p.stdout.decode("utf-8"))
        return p.stdout.decode("utf-8")


class Excel:
    def __init__(self, path="", workbook=None, sheet_index=0, sheet=None):
        self.path = path
        self.workbook = workbook
        self.sheet_index = sheet_index
        self.sheet = sheet

    def open(self):
        """
        打开一个excel表
        :return:
        """
        self.workbook = xlrd.open_workbook(self.path)
        self.sheet = self.workbook.sheet_by_index(self.sheet_index)

    def change_sheet(self, sheet_index):
        """
        切换sheet
        :param sheet_index:sheet的索引值
        :return:
        """
        self.sheet = self.workbook.sheet_by_index(sheet_index - 1)

    def cell_value(self, x_point=1, y_point=1) -> str:
        """
        获取单元格的返回值
        :param x_point: 行数
        :param y_point: 列数
        :return: str    单元格所在的值
        """
        return self.sheet.cell_value(x_point - 1, y_point - 1)

    def row_values(self, x_point=1) -> list:
        """
        获取一行的所有值，返回一个值的列表
        :param x_point:
        :return: list
        """
        return self.sheet.row_values(x_point - 1)

    def col_values(self, y_point=1) -> list:
        """
        获取一列的所有值，返回一个值的列表
        :param y_point:
        :return: list
        """
        return self.sheet.col_values(y_point - 1)


"""
队列类
"""


class MyQueue:
    def __init__(self):
        self.queue = []

    def add(self, obj):
        self.queue.append(obj)

    def delete(self, index):
        self.queue.pop(index)

    def get_size(self):
        return len(self.queue)


"""
线程类
"""


class MyThread(Thread):
    def __init__(self, func):
        super().__init__()
        self.target = func

    def run(self) -> None:
        super().run()


"""
文件处理类
"""


class Files:
    def __init__(self):
        pass

    def download_file(self, source_url="", path=""):
        if self.check_file_is_exist(path):
            return path
        else:
            url = source_url
            req = requests.get(url)
            with open(path, "wb") as file:
                file.write(req.content)

    def check_file_is_exist(self, file_name):
        if file_name in self.get_list_dir():
            return True
        else:
            return False

    @staticmethod
    def get_current_file_path():
        return str(Path().resolve())

    @staticmethod
    def get_list_dir():
        return [str(x) for x in Path().iterdir()]

    @staticmethod
    def mkdir(filepath):
        if Path(filepath).exists():
            return
        else:
            Path(filepath).mkdir()


class SqlClass:
    def __init__(self, host, username, password, dbName, db=None, port=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dbName = dbName
        self.db = db

    def connect_mysql(self):
        self.db = pymysql.connect(host=self.host, port=self.port, user=self.username,
                                  password=self.password, db=self.dbName)

    def deal_sql(self, sql_str):
        cursor = self.db.cursor()
        cursor.excute(sql_str)
        return cursor


class Yaml:
    def __init__(self, path="") -> None:
        self.path = path

    def yaml_to_dict(self) -> dict:
        with open(self.path, "r") as f:
            yaml_file = yaml.safe_load(f)
        return yaml_file

    def get_config_by_name(self, config_name=""):
        dic = benedict(self.yaml_to_dict())
        return dic[config_name]

    # TODO 添加文件内容的异常处理
    # TODO yaml单例模式
    # TODO yaml读取进行缓存处理


"""
appium类
"""


@singleton
class Appium:
    def __init__(self, address: str = "localhost", port: int = 4723,
                 desired_capabilities: Optional[Dict] = None):
        self.address = address
        self.port = port
        self.url = "http://" + address + ":" + str(port) + "/wd/hub"
        self.desc = desired_capabilities
        self.driver = None

    def start_server(self):
        thread1 = MyThread(self.deal())
        thread1.start()

    def deal(self):
        Adb.run("lsof -i tcp:4723|awk '{print $2}' |sed -n '2p'|xargs kill -9")
        if self.address != "localhost" or self.port != 4723:
            Adb.run("appium  --a " + self.address + " --p " + str(self.port))
        Adb.run("appium")
        # if "started on" in str(msg):
        #     print("start success")

    def start_driver(self):
        print(self.url)
        self.driver = webdriver.Remote(self.url, self.desc)
        return self.driver


# adb装饰器
def adb_wrapper(func):
    def wrapper(*args, **kwargs):
        u = func()
        return u

    return wrapper()


"""
selenium类
"""


@singleton
class Selenium(object):

    def __init__(self, version: str = "", platform: str = "", config_dir: str = "",
                 yaml_file_path: str = "", driver_zip: str = "",
                 driver=None):
        self._version = version
        self._platform = platform
        self._config_dir = config_dir
        self._config_file = yaml_file_path
        self._yaml_file = None
        self._driver = driver
        self._driver_zip = driver_zip
        if self._platform == "windows":
            self._driver_path = self._config_dir + "/chromedriver.exe"
        else:
            self._driver_path = self._config_dir + "/chromedriver"

    def get_webdriver_package(self):
        file_tool = Files()
        if file_tool.check_file_is_exist(self._config_dir):
            if file_tool.check_file_is_exist(self._driver_path):
                return self._driver_path
            else:
                self._yaml_file = Yaml(self._config_dir + self._config_file)
                url = self._yaml_file.get_config_by_name(
                    "download_url.base_url") + self._version + self._yaml_file.get_config_by_name(self._platform)
                f = requests.get(url, stream=True)
                with open(self._driver_zip, "wb") as file:
                    file.write(f.content)
                z = zipfile.ZipFile(self._driver_zip, 'r')
        else:
            file_tool.mkdir(self._config_dir)

    def start_driver(self):
        self._driver = webdriver.Chrome(executable_path=self.get_webdriver_package())
        self._driver.get(self._yaml_file.get_config_by_name("selenium_url"))
        return self._driver
