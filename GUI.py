from tkinter import *
import hashlib
import time
import os
import ncm2flac as conversion
import base64
import binascii
import io
import json
import os
import shutil
import struct
import time
#  此程序用于将网易云音乐的.ncm格式的音乐转换为  最初格式
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from Crypto.Cipher import AES
from PIL import Image
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, APIC

LOG_LINE_NUM = 0


# 获取当前时间
def get_current_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return current_time


class GUI:
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("NCM转换器V0.1")
        self.init_window_name.geometry(self.center_window(1068, 681))
        # self.init_window_name["bg"] = "pink"
        # self.init_window_name.attributes("-alpha", 0.9)
        #标签
        self.init_data_label = Label(self.init_window_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=0)
        #文本框
        self.init_data_Text = Text(self.init_window_name, width=67, height=35)  #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=49)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        #按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="字符串转MD5", bg="lightblue", width=10,
                                              command=self.str_trans_to_md5)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=1, column=11)

    def center_window(self, width, height):
        screen_width = self.init_window_name.winfo_screenwidth()
        screen_height = self.init_window_name.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - height / 2)
        return f"{width}x{681}+{center_x}+{center_y}"

    # 功能函数
    def conversion_to_flac(self):
        oriPath = r"E:\unibeam\Music\未转换"
        tarPath = r"E:\unibeam\Music\python"
        if tarPath[-1] != '/' or tarPath[-1] != '\\':
            tarPath += '\\'

        str = ""

        try:
            file_list = os.listdir(oriPath)
            num = len(file_list)
            self.log(f"共有{num}首歌")

        except:
            pass
            # var = str + file_list[i]



    def str_trans_to_md5(self):
        src = self.init_data_Text.get(1.0, END).strip().replace("\n", "").encode()
        #print("src =",src)
        if src:
            try:
                myMd5 = hashlib.md5()
                myMd5.update(src)
                myMd5_Digest = myMd5.hexdigest()
                #print(myMd5_Digest)
                #输出到界面
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, myMd5_Digest)
                self.log("INFO:str_trans_to_md5 success")
            except:
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, "字符串转MD5失败")
        else:
            self.log("ERROR:str_trans_to_md5 failed")

    # 日志动态打印
    def log(self, log_msg):
        global LOG_LINE_NUM
        current_time = get_current_time()
        log_msg_in = str(current_time) + " " + str(log_msg) + "\n"
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, log_msg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0, 2.0)
            self.log_data_Text.insert(END, log_msg_in)


def gui_start():
    init_window = Tk()
    nvm_conversion = GUI(init_window)
    # 设置根窗口默认属性
    nvm_conversion.set_init_window()
    init_window.mainloop()


gui_start()
