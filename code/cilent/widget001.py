#应用端窗口界面
import tkinter as tk

def on_button_click():
    print("Button clicked!")
def func1():
    print(1)
def func2():
    print(2)
def func3():
    print(3)

# 创建主窗口
window = tk.Tk()

# 设置窗口标题
window.title("Colorful Interface")

# 设置窗口大小
window.geometry("800x600")

# 创建多样的按钮样式
button_styles = [
    {"text": "Button 1", "bg": "red", "fg": "white", "font": ("Arial", 12)},
    {"text": "Button 2", "bg": "blue", "fg": "white", "font": ("Helvetica", 14, "bold")},
    {"text": "Button 3", "bg": "#00FF00", "fg": "black", "font": ("Roboto", 10)},
]

# 创建并放置多个按钮
button = tk.Button(window, text=button_styles[0]["text"], bg=button_styles[0]["bg"], fg=button_styles[0]["fg"], font=button_styles[0]["font"], command=func1())
button.pack(pady=10)
button = tk.Button(window, text=button_styles[1]["text"], bg=button_styles[1]["bg"], fg=button_styles[1]["fg"], font=button_styles[1]["font"], command=func2())
button.pack(pady=10)
button = tk.Button(window, text=button_styles[2]["text"], bg=button_styles[2]["bg"], fg=button_styles[2]["fg"], font=button_styles[2]["font"], command=func3())
button.pack(pady=10)

# 运行界面主循环
window.mainloop()