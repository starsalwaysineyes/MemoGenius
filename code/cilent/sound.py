import pyaudio
import wave
import threading
import keyboard

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def record_audio(stream, frames, stop_event):
    while not stop_event.is_set():
        data = stream.read(CHUNK)
        frames.append(data)

def wait_for_start(stop_event):
    keyboard.wait("esc")
    print("结束录制...")
    stop_event.set()

def wait_for_stop(stop_event):
    
    stop_event.clear()

def func():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    stop_event = threading.Event()
    frames = []

    print("按下回车开始录制麦克风音频,按下Esc停止录制...")
    input("")
    print("开始录制...")
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

    waveFile = wave.open("output1.mp4", 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    print("录制完毕！")

# 调用函数示例
func()  # 调用录制麦克风音频的函数