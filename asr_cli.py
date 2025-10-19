#!/usr/bin/env python3
"""
ASR Tools 命令行工具
支持批量处理指定文件夹中的音频/视频文件，转换为文本格式
"""

import argparse
import logging
import os
import sys
import time
from pathlib import Path
from typing import List, Optional
import subprocess

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from bk_asr.BcutASR import BcutASR
from bk_asr.JianYingASR import JianYingASR
from bk_asr.KuaiShouASR import KuaiShouASR

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 支持的音频/视频格式
SUPPORTED_FORMATS = {
    # 音频格式
    '.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a', '.wma',
    # 视频格式
    '.mp4', '.avi', '.mov', '.ts', '.mkv', '.wmv', '.flv', '.webm', '.rmvb'
}

# ASR引擎映射
ASR_ENGINES = {
    'b': 'B接口',
    'j': 'J接口', 
    'k': 'K接口',
    'bcut': 'B接口',
    'jianying': 'J接口',
    'kuaisou': 'K接口'
}

def video2audio(input_file: str, output: str = "") -> bool:
    """使用ffmpeg将视频转换为音频"""
    try:
        # 创建output目录
        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output = str(output)

        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-ac', '1',
            '-f', 'mp3',
            '-af', 'aresample=async=1',
            '-y',
            output
        ]
        result = subprocess.run(cmd, capture_output=True, check=True, encoding='utf-8', errors='replace')

        if result.returncode == 0 and Path(output).is_file():
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"视频转音频失败: {e}")
        return False

def get_audio_files(directory: str) -> List[str]:
    """扫描目录获取所有支持的音频/视频文件"""
    audio_files = []
    directory = Path(directory)
    
    if not directory.exists():
        logger.error(f"目录不存在: {directory}")
        return audio_files
    
    if directory.is_file():
        # 如果是文件，检查是否支持
        if directory.suffix.lower() in SUPPORTED_FORMATS:
            audio_files.append(str(directory))
        else:
            logger.warning(f"不支持的文件格式: {directory}")
    else:
        # 如果是目录，递归扫描
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_FORMATS:
                audio_files.append(str(file_path))
    
    return audio_files

def process_audio_file(file_path: str, engine: str, output_format: str = 'txt', use_cache: bool = True) -> bool:
    """处理单个音频文件"""
    try:
        logger.info(f"开始处理文件: {file_path}")
        
        # 检查文件类型，如果不是音频则转换
        audio_exts = ['.mp3', '.wav']
        if not any(file_path.lower().endswith(ext) for ext in audio_exts):
            logger.info("正在使用ffmpeg转换音频格式...")
            temp_audio = file_path.rsplit(".", 1)[0] + ".mp3"
            if not video2audio(file_path, temp_audio):
                logger.error("音频转换失败，确保安装ffmpeg")
                return False
            audio_path = temp_audio
        else:
            audio_path = file_path
        
        # 根据选择的 ASR 引擎实例化相应的类
        if engine == 'B接口':
            asr = BcutASR(audio_path, use_cache=use_cache)
        elif engine == 'J接口':
            asr = JianYingASR(audio_path, use_cache=use_cache)
        elif engine == 'K接口':
            asr = KuaiShouASR(audio_path, use_cache=use_cache)
        else:
            raise ValueError(f"未知的 ASR 引擎: {engine}")

        # 运行ASR
        result = asr.run()
        
        # 根据导出格式选择转换方法
        save_ext = output_format.lower()
        if save_ext == 'srt':
            result_text = result.to_srt()
        elif save_ext == 'ass':
            result_text = result.to_ass()
        elif save_ext == 'txt':
            result_text = result.to_txt()
        else:
            raise ValueError(f"不支持的输出格式: {output_format}")
        
        # 保存结果
        save_path = file_path.rsplit(".", 1)[0] + "." + save_ext
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(result_text)
        
        logger.info(f"处理完成: {save_path}")
        
        # 清理临时文件
        if audio_path != file_path and os.path.exists(audio_path):
            os.remove(audio_path)
        
        return True
        
    except Exception as e:
        logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="ASR Tools 命令行工具 - 批量音频转文本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s -i /path/to/audio/folder -e b
  %(prog)s -i /path/to/video.mp4 -e j -f srt
  %(prog)s -i /path/to/folder -e k -f txt --no-cache
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='输入文件或文件夹路径'
    )
    
    parser.add_argument(
        '-e', '--engine',
        choices=['b', 'j', 'k', 'bcut', 'jianying', 'kuaisou'],
        default='b',
        help='ASR引擎选择 (默认: b)'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['txt', 'srt', 'ass'],
        default='txt',
        help='输出格式 (默认: txt)'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='不使用缓存'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='详细输出'
    )
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 转换引擎名称
    engine_name = ASR_ENGINES[args.engine]
    use_cache = not args.no_cache
    
    logger.info(f"ASR Tools 命令行工具启动")
    logger.info(f"输入路径: {args.input}")
    logger.info(f"ASR引擎: {engine_name}")
    logger.info(f"输出格式: {args.format}")
    logger.info(f"使用缓存: {use_cache}")
    
    # 获取音频文件列表
    audio_files = get_audio_files(args.input)
    
    if not audio_files:
        logger.warning("未找到支持的音频/视频文件")
        return 1
    
    logger.info(f"找到 {len(audio_files)} 个文件待处理")
    
    # 处理文件
    success_count = 0
    failed_count = 0
    start_time = time.time()
    
    for i, file_path in enumerate(audio_files, 1):
        logger.info(f"处理进度: {i}/{len(audio_files)} - {os.path.basename(file_path)}")
        
        if process_audio_file(file_path, engine_name, args.format, use_cache):
            success_count += 1
        else:
            failed_count += 1
    
    # 输出统计信息
    elapsed_time = time.time() - start_time
    logger.info("=" * 50)
    logger.info("处理完成!")
    logger.info(f"总文件数: {len(audio_files)}")
    logger.info(f"成功处理: {success_count}")
    logger.info(f"处理失败: {failed_count}")
    logger.info(f"总耗时: {elapsed_time:.2f} 秒")
    
    return 0 if failed_count == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
