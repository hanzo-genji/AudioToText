from vosk import Model, KaldiRecognizer
import json
import wave
from tqdm import tqdm
# import speech_recognition as sr
from pydub import AudioSegment

# 转换 m4a 文件到 wav
# audio = AudioSegment.from_file("liuhang.m4a", format="m4a")
# audio.export("audio.wav", format="wav")

# 将任何音频文件转换为wav格式音频文件并输出
def convert_to_wav(input_filepath, output_filepath):
    """
    Converts an audio file to wav format.
    
    Parameters:
        input_filepath (str): Path to the input audio file.
        output_filepath (str): Path to save the output wav file.
    """
    # Load the audio file
    audio = AudioSegment.from_file(input_filepath)
    
    # Convert to wav
    audio.export(output_filepath, format="wav")
    
# Example usage:
# convert_to_wav("path/to/input/file.mp3", "path/to/output/file.wav")


# 加载中文模型
model = Model("vosk-model-cn2")  # 修改为您的模型目录，vosk-model-cn2模型更大，准确率应该更好但是速度会更慢一点

# 读取音频文件
with wave.open("audio.wav", "rb") as wf:
    rec = KaldiRecognizer(model, wf.getframerate())
    
    total_frames = wf.getnframes()
    frames_per_chunk = 4000
    num_chunks = total_frames // frames_per_chunk + 1

    # 使用 tqdm 创建进度条
    with tqdm(total=num_chunks) as pbar:
        while True:
            data = wf.readframes(frames_per_chunk)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                pass
            pbar.update(1)

    # 获取识别结果
    result = json.loads(rec.FinalResult())
    recognized_text = result['text']

# 将识别结果保存到文本文件中
with open("recognized_result.txt", "w", encoding="utf-8") as f:
    f.write(recognized_text)

print("识别完成，结果已保存到 recognized_result.txt 文件中。")
