import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
import func_phpUpload


def record_button_clicked():
    print("录制按钮被点击了")
    
def upload_button_clicked():
    setAllowed={".wav",".mp3",".mp4"}
    print("上传按钮被点击了")
    
    # 获取文本框中的内容并赋值给变量
    user_input = input_entry.get()
    print("用户输入的内容：", user_input)
    if(user_input[-4::] not in setAllowed):
        print("请输入正确的地址！")
    else:
        try:
            func_phpUpload.up(user_input)
        except:
            print("应用端上传文件失败")
            


def preview_button_clicked():
    file_path = filedialog.askopenfilename()
    print("选择的文件路径：", file_path)
    
    # 将文件路径填充到输出框中
    input_entry.insert(tk.END, file_path)

# 创建主窗口
window = tk.Tk()
icon = ImageTk.PhotoImage(file="./background.jpg")
window.iconphoto(True, icon)
#window.iconbitmap("./background.png") 
window.geometry("800x600")

window.title("MemoGenius")


# 创建Canvas组件
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()

#生成背景
image = Image.new("RGB", (800, 600), "black")
background_image = Image.open("./back_ground2.jpg")
background_photo = ImageTk.PhotoImage(background_image)


stars = []

background_stars = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor="nw", image=background_photo)




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
