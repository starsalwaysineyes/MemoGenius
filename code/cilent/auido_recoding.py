import pyaudio
import wave
import threading
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

is_recording = 0

def record_audio(stream, frames, stop_event):
    #实际录制音频
    while not stop_event.is_set():
        data = stream.read(CHUNK)
        frames.append(data)

def wait_for_start(stop_event):
    # 在一个循环中等待开始录制的信号
    while True:
        if is_recording == 1:
            break
        time.sleep(0.01)
    #停止录制
    stop_event.set()


def wait_for_stop(stop_event):
    # 清除停止事件的信号
    stop_event.clear()

def record_microphone_audio(output_file):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    stop_event = threading.Event()
    frames = []


    start_thread = threading.Thread(target=wait_for_start, args=(stop_event,))
    stop_thread = threading.Thread(target=wait_for_stop, args=(stop_event,))
    start_thread.start()
    stop_thread.start()

    record_thread = threading.Thread(target=record_audio, args=(stream, frames, stop_event))
    record_thread.start()

    stop_thread.join()
    start_thread.join()
    record_thread.join()

    stream.stop_stream()
    stream.close()
    p.terminate()

    wave_file = wave.open(output_file, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(p.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()


def check_recording_status():
    # 在一个循环中检查全局变量is_recording的值
    while True:
        if is_recording == 1:
            # 点击了开始录制按钮，开始录制音频
            output_file = "output.mp3"  # 设置输出文件路径
            record_microphone_audio(output_file)
        else:
            # 停止录制音频
            time.sleep(0.001)  # 暂停1毫秒

# 创建并启动检查录制状态的线程
check_thread = threading.Thread(target=check_recording_status)
check_thread.start()