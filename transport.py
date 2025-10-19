import os
import sys
import argparse
from faster_whisper import WhisperModel

import time
import contextlib

model = WhisperModel("medium", device="cpu", compute_type="int8")

current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
from bk_asr import BcutASR
if current_dir not in sys.path:
  sys.path.append(current_dir)
  
def parse_args():
  parser = argparse.ArgumentParser(description="Transport")
  parser.add_argument("-i", "--input", type=str, required=True, help="Input file path")
  return parser.parse_args()


def get_audio_duration(file_path):
  import subprocess
  result = subprocess.run(
      ["ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path],
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT)
  return float(result.stdout)

def sts_file_clean(file_path):
    output_path = file_path.replace(".mp3", ".txt").replace(".wav", ".txt")

    # 记录处理前时间
    start_time = time.time()

    # 获取音频时长
    audio_duration = get_audio_duration(file_path)

    # Whisper 转写
    segments, _ = model.transcribe(file_path, vad_filter=True)

    # 保存文本
    with open(output_path, "w", encoding="utf-8") as f:
        for seg in segments:
            text = seg.text.strip()
            if text:
                f.write(text + "\n")

    # 处理耗时
    elapsed_time = time.time() - start_time

    # 打印信息
    print(f"🎧 音频时长：{audio_duration:.2f} 秒（约 {audio_duration/60:.1f} 分钟）")
    print(f"⏱ 处理耗时：{elapsed_time:.2f} 秒")
    print(f"✅ 转写完成：{output_path}")

     
def handle_file(file_path):
  if os.path.isdir(file_path):
    for file in os.listdir(file_path):
      filename = os.path.join(file_path, file)
      handle_file(filename)
  else:
    if file_path.endswith(".mp3"):
      print(f"Transcoding {file_path}")
      srt_file = file_path.replace(".mp3", ".txt")
      if os.path.exists(srt_file):
        print(f"SRT file {srt_file} already exists")
        return
      else:
        sts_file_clean(file_path)
        # try:
        #   asr = BcutASR(file_path)
        #   result = asr.run()
        #   txt = result.to_txt()
        #   with open(srt_file,  "w", encoding="utf-8") as f:
        #     f.write(txt)
        #   print(f"SRT file {srt_file} created")
        # except Exception as e:
        #   print(e)
        #   print(f"Error transcoding {file_path}: {e}")

if __name__ == "__main__":
  args = parse_args()
  if not os.path.exists(args.input):
    print(f"Input file {args.input} does not exist")
    sys.exit(1)
  handle_file(args.input)
  
