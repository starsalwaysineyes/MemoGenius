from imports import *
#从整理的库里import所有

#功能为止，目前是设置同一类的appid，从而使任务栏窗口可以堆叠
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

#超级无敌屌的全局变量之，用数组甚至都不用global
lst=[0]

#主程序定义
def main():
    #录制按钮功能
    def record_button_func():
        #标记状态为1，表面要开始录制
        lst[0]=1
        #定义线程函数，让从main线程中单开一条线程去录音
        def start_recording():
            
            print("点击了录制按钮")
            # 点击了开始录制按钮，开始录制音频
            output_file = "output.mp3"  # 设置输出文件路径
            record_microphone_audio(output_file)

        #创建录音线程
        recording_thread = threading.Thread(target=start_recording)
        recording_thread.start()
        pass
    
    #结束录制按钮功能
    def stopRecord_button_func():
        #检查是否录制过，如果录制过，按钮应该变为“上传”，避免在没录制的时候点击结束录制
        if(lst[0]==0):
            print("您还没开始录制呢！")
            return
        print("结束录制按钮被点击了")
        #修改状态标记，标记为不需要录音
        lst[0]=0
        
        #将结束录音按钮隐藏，替换为上传按钮
        record_button.config(state=tk.NORMAL)  # 将录制按钮重新设为可用
        stop_record_button.config(text="上传", command=upload_button_clicked)  # 将结束录制按钮改为上传按钮
        preview_button.config(state=tk.DISABLED)  # 禁用预览按钮
    
    #上传按钮功能
    def upload_button_clicked():
        
        setAllowed = {".wav", ".mp3", ".mp4"}
        
        # 获取文本框中的内容并赋值给变量
        user_input = input_entry.get()
        print("用户输入的内容：", user_input)
        if user_input[-4:] not in setAllowed:
            print("请输入正确的地址！")
        else:
            try:
                func_phpUpload.up(user_input)
            except:
                print("应用端上传文件失败")

    #预览按钮功能
    def preview_button_clicked():
        file_path = filedialog.askopenfilename()
        print("选择的文件路径：", file_path)

        # 将文件路径填充到输出框中
        input_entry.insert(tk.END, file_path)


    #设置以文件为参考路径
    current_path = os.path.abspath(__file__)
    #拿到文件的目录路径
    current_directory = os.path.dirname(current_path)
    #将jpg图片路径设为与文件同级目录的background.jpg图片
    jpgpath = current_directory + "\\background.jpg"

    #实例化主窗口
    window = tk.Tk()
    #设置主窗口图标
    icon = ImageTk.PhotoImage(file=jpgpath)
    window.iconphoto(True, icon)

    #设置主窗口大小
    window.geometry("800x600")
    
    #设置主窗口标题
    window.title("MemoGenius")

    # 创建Canvas组件
    canvas = tk.Canvas(window, width=800, height=600)
    canvas.pack()

    # 生成背景
    #image = Image.new("RGB", (800, 600), "black")
    background_2 = current_directory + "\\back_ground2.jpg"
    background_image = Image.open(background_2)
    background_photo = ImageTk.PhotoImage(background_image)
    canvas.create_image(0, 0, anchor="nw", image=background_photo)


    # 创建输入框、按钮，并绑定点击事件
    input_entry = tk.Entry(window, font=("Helvetica", 18), width=30)
    input_entry.place(relx=0.5, rely=0.7, anchor="center")  # 调整文本框的位置

    record_button = tk.Button(window, text="录制", font=("Helvetica", 18), command=record_button_func, bg="lightblue",
                            fg="white")
    stop_record_button = tk.Button(window, text="结束录制", font=("Helvetica", 18), command=stopRecord_button_func,
                                bg="red", fg="white")
    preview_button = tk.Button(window, text="预览", font=("Helvetica", 18), command=preview_button_clicked, bg="orange",
                            fg="white")

    record_button.place(relx=0.3, rely=0.8, anchor="center")
    stop_record_button.place(relx=0.5, rely=0.8, anchor="center")
    preview_button.place(relx=0.7, rely=0.8, anchor="center")

    # 进入主循环

    window.mainloop()



def record_microphone_audio(output_file):
    #默认参数
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    #实际录制音频线程函数
    def record_audio(stream, frames, CHUNK):
        while lst[0]:#这里只要我的这个lst[0]保持为1，就一直运行，直到出现func2使得lst[0]变为1
            data = stream.read(CHUNK)
            frames.append(data)
    
    #实例化音频对象
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    #设置录制线程并直接开启线程
    record_thread = threading.Thread(target=record_audio, args=(stream, frames,CHUNK))
    record_thread.start()
    #该函数所在的线程等待此处线程终止
    record_thread.join()

    #录制线程结束后结束流文件并关闭
    stream.stop_stream()
    stream.close()
    p.terminate()
    #终止音频对象的实例，释放资源

    #将录制到的音频按照格式从frames中提取数据并保存，最后关闭音频文件对象，
    # 此处可改成with open，可以避免程序崩溃后文件没有被关闭
    wave_file = wave.open(output_file, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(p.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()


#主程序
if(__name__ == "__main__"):
    main()


