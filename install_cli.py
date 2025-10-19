#!/usr/bin/env python3
"""
ASR CLI 安装脚本
用于安装命令行工具到系统PATH
"""

import os
import sys
import shutil
import platform
from pathlib import Path

def get_install_dir():
    """获取安装目录"""
    if platform.system() == "Windows":
        # Windows: 安装到用户目录下的Scripts文件夹
        return Path.home() / "AppData" / "Local" / "Programs" / "Python" / "Scripts"
    else:
        # macOS/Linux: 安装到用户本地bin目录
        return Path.home() / ".local" / "bin"

def install_cli():
    """安装命令行工具"""
    print("ASR CLI 安装程序")
    print("=" * 40)
    
    # 获取当前脚本目录
    current_dir = Path(__file__).parent.absolute()
    cli_script = current_dir / "asr_cli.py"
    
    if not cli_script.exists():
        print("❌ 错误: 找不到 asr_cli.py 文件")
        return False
    
    # 获取安装目录
    install_dir = get_install_dir()
    install_dir.mkdir(parents=True, exist_ok=True)
    
    # 安装文件
    if platform.system() == "Windows":
        # Windows: 复制文件并创建批处理文件
        target_file = install_dir / "asr_cli.py"
        shutil.copy2(cli_script, target_file)
        
        # 创建批处理文件
        bat_file = install_dir / "asr_cli.bat"
        with open(bat_file, 'w') as f:
            f.write(f'@echo off\npython "{target_file}" %*\n')
        
        print(f"✅ 已安装到: {target_file}")
        print(f"✅ 批处理文件: {bat_file}")
    else:
        # macOS/Linux: 复制文件并设置执行权限
        target_file = install_dir / "asr_cli"
        shutil.copy2(cli_script, target_file)
        
        # 设置执行权限
        os.chmod(target_file, 0o755)
        
        print(f"✅ 已安装到: {target_file}")
    
    # 检查PATH
    path_env = os.environ.get('PATH', '')
    if str(install_dir) not in path_env:
        print(f"\n⚠️  警告: {install_dir} 不在PATH中")
        print("请将以下路径添加到PATH环境变量:")
        print(f"  {install_dir}")
        print("\n或者重新启动终端后运行:")
        print("  source ~/.bashrc  # Linux")
        print("  source ~/.zshrc   # macOS with zsh")
    else:
        print(f"\n✅ {install_dir} 已在PATH中")
    
    print("\n安装完成！现在可以使用以下命令:")
    print("  asr_cli --help")
    
    return True

def uninstall_cli():
    """卸载命令行工具"""
    print("ASR CLI 卸载程序")
    print("=" * 40)
    
    install_dir = get_install_dir()
    
    if platform.system() == "Windows":
        target_file = install_dir / "asr_cli.py"
        bat_file = install_dir / "asr_cli.bat"
        
        if target_file.exists():
            target_file.unlink()
            print(f"✅ 已删除: {target_file}")
        
        if bat_file.exists():
            bat_file.unlink()
            print(f"✅ 已删除: {bat_file}")
    else:
        target_file = install_dir / "asr_cli"
        
        if target_file.exists():
            target_file.unlink()
            print(f"✅ 已删除: {target_file}")
        else:
            print("❌ 未找到安装的文件")
            return False
    
    print("\n卸载完成！")
    return True

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        return uninstall_cli()
    else:
        return install_cli()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
