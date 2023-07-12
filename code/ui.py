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

# 生成星空背景图像
image = Image.new("RGB", (800, 600), "black")
draw = ImageDraw.Draw(image)

stars = []

for _ in range(500):
    x = random.randint(0, 800)
    y = random.randint(0, 600)
    size = random.randint(1, 3)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    star = {"x": x, "y": y, "size": size, "color": (r, g, b)}
    stars.append(star)
    draw.rectangle([x, y, x+size, y+size], fill=(r, g, b))

background_stars = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor="nw", image=background_stars)

# 修改"会议"的字体样式和颜色
art_font = ("Helvetica", 48, "bold")
art_text = tk.Label(window, text="会", font=art_font, fg="white", bg="black")
art_text.place(relx=0.45, rely=0.4, anchor="center")

yi_font = ("Helvetica", 48, "bold")
yi_text = tk.Label(window, text="忆", font=yi_font, fg="white", bg="black")
yi_text.place(relx=0.55, rely=0.4, anchor="center")

def change_text_color():
    r = random.randint(200, 255)
    g = random.randint(200, 255)
    b = random.randint(200, 255)
    art_text.configure(fg=f'#{r:02x}{g:02x}{b:02x}')
    yi_text.configure(fg=f'#{r:02x}{g:02x}{b:02x}')
    window.after(1000, change_text_color)

# 初始时立即调用一次，之后每隔1秒改变一次文本颜色
change_text_color() 

def animate_stars():
    for star in stars:
        x = star["x"]
        y = star["y"]
        size = star["size"]
        r, g, b = star["color"]

        # 随机改变星星的颜色
        if random.random() < 0.05:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            star["color"] = (r, g, b)
        
        # 随机改变星星的位置
        if random.random() < 0.02:
            x += random.randint(-2, 2)
            y += random.randint(-2, 2)
            star["x"] = x
            star["y"] = y
        
        # 限制星星的位置在窗口范围内
        x = max(0, min(x, 800-size))
        y = max(0, min(y, 600-size))

        # 绘制星星
        draw.rectangle([x, y, x+size, y+size], fill=(r, g, b))
    
    background_stars = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=background_stars)
    
    window.after(100, animate_stars)

# 初始时立即调用一次，之后每隔0.1秒更新一次星星的位置和颜色
animate_stars()

def change_background_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    canvas.configure(bg=f'#{r:02x}{g:02x}{b:02x}')
    window.after(5000, change_background_color)

# 初始时立即调用一次，之后每隔5秒改变一次背景颜色
change_background_color() 

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
