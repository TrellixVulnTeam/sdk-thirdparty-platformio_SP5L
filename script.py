import os
import shutil
import sys
from pathlib import Path


class PlatformioBuilder(object):
    """
    This is the platformio env builder
    """

    def __init__(self):
        dir_path = ""
        if getattr(sys, 'frozen', False):
            dir_path = os.path.dirname(sys.executable)
        elif __file__:
            dir_path = os.path.dirname(__file__)
        self.current_folder = Path(dir_path)
        print(self.current_folder)
        self.home_path = Path.home()
        self.platformio_path = self.home_path.joinpath(".platformio")
        self.python_path = self.current_folder.joinpath("python377x64/python.exe")
        self.get_platformio_script_path = self.current_folder.joinpath("python377x64/get-platformio.py")

    def rm_fr_list(self, item_list, dst_path):
        for item_path in item_list:
            dst_item_path = str(dst_path.joinpath(item_path))
            dst_item_path = dst_item_path.replace('\\', '/')
            dst_item_path = Path(dst_item_path)
            if dst_item_path.exists():
                if Path.is_dir(dst_item_path):
                    shutil.rmtree(self.long_path_enable(dst_item_path))
                else:
                    os.remove(self.long_path_enable(dst_item_path))

    @staticmethod
    def long_path_enable(path_in):
        if os.name == "nt":
            return str('\\\\?\\' + str(path_in))
        else:
            return path_in

    def cp_fr_list(self, item_list, src_path, dst_path):
        item_list_temp = []
        for item_path in item_list:
            if str(item_path) == "*":
                item_list_temp.extend(os.listdir(src_path))
            else:
                item_list_temp.append(item_path)
        item_list_all = list(set(item_list_temp))
        for item_path in item_list_all:
            src_item_path = str(src_path.joinpath(item_path))
            dst_item_path = str(dst_path.joinpath(item_path))
            src_item_path = src_item_path.replace('\\', '/')
            dst_item_path = dst_item_path.replace('\\', '/')
            src_item_path = Path(src_item_path)
            dst_item_path = Path(dst_item_path)
            if dst_item_path.exists():
                if Path.is_dir(dst_item_path):
                    shutil.rmtree(self.long_path_enable(dst_item_path))
                else:
                    os.remove(self.long_path_enable(dst_item_path))
            if not dst_item_path.parent.exists():
                os.makedirs(self.long_path_enable(dst_item_path.parent))
            if src_item_path.is_dir():
                shutil.copytree(self.long_path_enable(src_item_path), self.long_path_enable(dst_item_path))
            else:
                shutil.copy(self.long_path_enable(src_item_path), self.long_path_enable(dst_item_path))

    def copy_platformio_packages(self):
        if not self.platformio_path.exists():
            os.makedirs(self.long_path_enable(self.platformio_path))
            self.cp_fr_list([".platformio"], self.current_folder, self.home_path)
        else:
            print("update platformio")
            self.cp_fr_list(os.listdir(self.current_folder.joinpath(".platformio/packages")),
                            self.current_folder.joinpath(".platformio/packages"),
                            self.platformio_path.joinpath("packages"))
            self.cp_fr_list(os.listdir(self.current_folder.joinpath(".platformio/platforms")),
                            self.current_folder.joinpath(".platformio/platforms"),
                            self.platformio_path.joinpath("platforms"))
            print(self.current_folder.joinpath(".platformio"))
            print(os.listdir(self.current_folder.joinpath(".platformio")))
            other_file_and_folders = os.listdir(self.current_folder.joinpath(".platformio"))
            other_file_and_folders.remove("platforms")
            other_file_and_folders.remove("packages")
            self.cp_fr_list(other_file_and_folders, self.current_folder.joinpath(".platformio"), self.platformio_path)
        if self.platformio_path.joinpath("penv").exists():
            if Path.is_dir(self.platformio_path.joinpath("penv")):
                shutil.rmtree(self.long_path_enable(self.platformio_path.joinpath("penv")))
            else:
                os.remove(self.long_path_enable(self.platformio_path.joinpath("penv")))
            print("done")

    def install_platformio(self):
        os.system(str(self.python_path.as_posix()) + " " + str(self.get_platformio_script_path.as_posix()))

    def make_platformio(self):
        self.copy_platformio_packages()
        self.install_platformio()


builder = PlatformioBuilder()
builder.make_platformio()