import argparse
import os
from TTS.api import TTS
from pydub import AudioSegment

def text_to_speech(
    input_path,
    output_path,
    model_name="tts_models/en/ljspeech/tacotron2-DDC",
    speaker_idx=None,
    speed=1.0
):
    # 读取文本内容
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read().strip()

    # 加载模型
    tts = TTS(model_name=model_name, progress_bar=True, gpu=False)

    # 生成 wav 音频
    wav_path = output_path.replace('.mp3', '.wav')
    tts.tts_to_file(
        text=text,
        file_path=wav_path,
        speaker=speaker_idx,
        speed=speed
    )

    # 转换为 mp3
    sound = AudioSegment.from_wav(wav_path)
    sound.export(output_path, format="mp3")

    # 清理中间 wav 文件
    os.remove(wav_path)

    print(f"✅ 成功生成 MP3: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将文本文件转换为语音 MP3")
    parser.add_argument("--input", required=True, help="输入的文本文件路径")
    parser.add_argument("--output", required=True, help="输出的 MP3 文件路径")
    parser.add_argument("--model", default="tts_models/en/ljspeech/tacotron2-DDC", help="使用的模型名称")
    parser.add_argument("--speaker", default=None, help="说话人ID（可用于多说话人模型）")
    parser.add_argument("--speed", type=float, default=1.0, help="语速调整（1.0为正常）")

    args = parser.parse_args()

    text_to_speech(
        input_path=args.input,
        output_path=args.output,
        model_name=args.model,
        speaker_idx=args.speaker,
        speed=args.speed
    )
