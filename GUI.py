import os
import time
import tkinter
from tkinter import *
from tkinter import filedialog

import ncm2flac as conversion

LOG_LINE_NUM = 0
default_input_path = r"E:\unibeam\Music\VipSongsDownload"
default_output_path = r"E:\unibeam\Music"


# 获取当前时间
def get_current_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return current_time


def browse_file(entry):
    file_name = filedialog.askdirectory()
    entry.delete(0, tkinter.END)
    entry.insert(0, file_name)


class GUI:
    def __init__(self, init_window_name):
        self.log_data_Text = None
        self.conversion_button = None
        self.output_button = None
        self.output_entry = None
        self.input_button = None
        self.input_entry = None
        self.init_window_name = init_window_name
        self.set_init_window()

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("NCM转换器V0.1")
        self.init_window_name.geometry(self.center_window(600, 300))
        # self.init_window_name["bg"] = "pink"
        # self.init_window_name.attributes("-alpha", 0.9)

        self.init_window_name.grid_columnconfigure(0, weight=0)
        self.init_window_name.grid_columnconfigure(1, weight=100)
        self.init_window_name.grid_rowconfigure(0, weight=1)
        self.init_window_name.grid_rowconfigure(1, weight=1)
        self.init_window_name.grid_rowconfigure(2, weight=5)
        self.input_entry = tkinter.Entry(self.init_window_name)
        self.input_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.input_button = tkinter.Button(self.init_window_name, text="源路径",
                                           command=lambda: browse_file(self.input_entry))
        self.input_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.output_entry = tkinter.Entry(self.init_window_name)
        self.output_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.output_button = tkinter.Button(self.init_window_name, text="目标路径",
                                            command=lambda: browse_file(self.output_entry))
        self.output_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.conversion_button = tkinter.Button(self.init_window_name, text="转换",
                                                command=lambda: self.conversion_to_flac())
        self.conversion_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.log_data_Text = Text(self.init_window_name, height=9)
        self.log_data_Text.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.log_data_Text.tag_config("red", foreground="red")
        self.log_data_Text.tag_config("black", foreground="black")

        # 设置默认路径
        self.input_entry.insert(0, default_input_path)
        self.output_entry.insert(0, default_output_path)

    def center_window(self, width, height):
        screen_width = self.init_window_name.winfo_screenwidth()
        screen_height = self.init_window_name.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - height / 2)
        return f"{width}x{height}+{center_x}+{center_y}"

    # 功能函数
    def conversion_to_flac(self):
        oriPath = self.input_entry.get()
        tarPath = self.output_entry.get()
        if tarPath[-1] != '/' or tarPath[-1] != '\\':
            tarPath += '\\'
        print(tarPath)

        failed_item = ""
        file_list = os.listdir(oriPath)
        num = len(file_list)
        self.log(f"共有{num}首歌")
        self.log("正在转换...")
        for i in range(0, len(file_list)):
            try:
                self.log(f"正在转换第{i + 1}/{num}首")
                path = os.path.join(oriPath, file_list[i])
                if os.path.isfile(path):
                    startTime = time.time()
                    conversion.dump(path, tarPath)
                    endTime = time.time()
                    duration = endTime - startTime
                    self.log(f"第{i + 1}/{num}首歌转换完成，用时{duration}秒")
                    # os.remove(path)
            except Exception as e:
                failed_item += str(file_list[i]) + "\n"
                pass
        self.log("转换失败的文件\n", True)
        self.log(failed_item, True)
        self.log("转换完成！")

    # 日志动态打印
    def log(self, log_msg, error=False):
        global LOG_LINE_NUM
        current_time = get_current_time()
        log_msg_in = str(current_time) + " " + str(log_msg) + "\n"
        if error:
            self.log_data_Text.insert(tkinter.END, str(log_msg), "red")
        else:
            self.log_data_Text.insert(tkinter.END, log_msg_in, "black")
        self.init_window_name.update_idletasks()

        LOG_LINE_NUM = LOG_LINE_NUM + 1
        print(LOG_LINE_NUM)
        if LOG_LINE_NUM >= 7:
            self.log_data_Text.see(tkinter.END)


def gui_start():
    init_window = tkinter.Tk()
    GUI(init_window)
    init_window.mainloop()


if __name__ == '__main__':
    gui_start()
