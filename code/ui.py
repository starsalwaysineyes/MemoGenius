import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import random

def record_button_clicked():
    print("录制按钮被点击了")

def upload_button_clicked():
    print("上传按钮被点击了")
    
    # 获取文本框中的内容并赋值给变量
    user_input = input_entry.get()
    print("用户输入的内容：", user_input)

# 创建主窗口
window = tk.Tk()
window.geometry("800x600")

# 创建Canvas组件
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()

# 生成背景花纹
image = Image.new("RGB", (800, 600), "white")
draw = ImageDraw.Draw(image)

for _ in range(5000):
    x1 = random.randint(0, 800)
    y1 = random.randint(0, 600)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    draw.point((x1, y1), fill=(r, g, b))

background_pattern = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor="nw", image=background_pattern)

# 添加"会忆"的艺术字
art_text = tk.Label(window, text="会忆", font=("Helvetica", 36), fg="white")
art_text.place(relx=0.5, rely=0.4, anchor="center")

def change_text_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    art_text.configure(fg=f'#{r:02x}{g:02x}{b:02x}')
    window.after(1000, change_text_color)

# 初始时立即调用一次，之后每隔1秒改变一次文本颜色
change_text_color() 

# 创建输入框和按钮，并绑定点击事件
input_entry = tk.Entry(window, font=("Helvetica", 18), width=20)
input_entry.place(relx=0.5, rely=0.7, anchor="center")  # 调整文本框的位置

record_button = tk.Button(window, text="录制", font=("Helvetica", 18), command=record_button_clicked, bg="lightblue", fg="white")
upload_button = tk.Button(window, text="上传", font=("Helvetica", 18), command=upload_button_clicked, bg="lightgreen", fg="white")

record_button.place(relx=0.3, rely=0.8, anchor="center")
upload_button.place(relx=0.7, rely=0.8, anchor="center")

# 进入主循环
window.mainloop()