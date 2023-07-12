import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk
import random
import ctypes
import os
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

def record_button_clicked():
    print("录制按钮被点击了")

def upload_button_clicked():
    print("上传按钮被点击了")
    
    # 获取文本框中的内容并赋值给变量
    user_input = input_entry.get()
    print("用户输入的内容：", user_input)

def preview_button_clicked():
    file_path = filedialog.askopenfilename()
    print("选择的文件路径：", file_path)
    
    # 将文件路径填充到输出框中
    input_entry.insert(tk.END, file_path)

# 创建主窗口
current_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_path)
jpgpath = current_directory + "\\background.jpg"
iconpath = current_directory + "\\background.ico"
window = tk.Tk()
icon = ImageTk.PhotoImage(file=jpgpath)
window.iconphoto(True, icon)
window.iconbitmap(iconpath)
window.geometry("800x600")

window.title("MemoGenius")


# 创建Canvas组件
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()
# 加载自定义背景图片
background_2 = current_directory + "\\back_ground2.jpg"
background_image = Image.open(background_2)
background_resized = background_image.resize((800, 600))
background_stars = ImageTk.PhotoImage(background_resized)
canvas.create_image(0, 0, anchor="nw", image=background_stars)


# 创建输入框、按钮，并绑定点击事件
input_entry = tk.Entry(window, font=("Helvetica", 18), width=30)
input_entry.place(relx=0.5, rely=0.7, anchor="center")  # 调整文本框的位置

record_button = tk.Button(window, text="录制", font=("Helvetica", 18), command=record_button_clicked, bg="lightblue", fg="white")
upload_button = tk.Button(window, text="上传", font=("Helvetica", 18), command=upload_button_clicked, bg="lightgreen", fg="white")
preview_button = tk.Button(window, text="预览", font=("Helvetica", 18), command=preview_button_clicked, bg="orange", fg="white")

record_button.place(relx=0.3, rely=0.8, anchor="center")
upload_button.place(relx=0.5, rely=0.8, anchor="center")
preview_button.place(relx=0.7, rely=0.8, anchor="center")

# 进入主循环
window.mainloop()
