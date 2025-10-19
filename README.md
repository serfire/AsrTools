
**注意：更多强大功能已经在我另一个项目实现:**

 [VideoCaptioner](https://github.com/WEIFENG2333/VideoCaptioner) 基于 LLM 的智能字幕助手，无需GPU一键高质量字幕视频合成！支持生成、断句、优化、翻译全流程。让视频字幕制作简单高效！


# 🎤 AsrTools

## 🌟 **特色功能**

- 🚀 **无需复杂配置**：无需 GPU 和繁琐的本地配置，小白也能轻松使用。
- 🖥️ **高颜值界面**：基于 **PyQt5** 和 **qfluentwidgets**，界面美观且用户友好。
- ⚡ **效率超人**：多线程并发 + 批量处理，文字转换快如闪电。
- 📄 **多格式支持**：支持生成 `.srt` 和 `.txt` 、`ass`字幕文件，满足不同需求。

欢迎为项目给上一个 Star ⭐ 。

**主界面截图示例：**

<img src="resources/main_window-1.1.0.png" width="80%" alt="主界面">


## 🌟 未来计划（TODO）

- 🎥 视频直接处理(完成)：支持输入视频文件自动转换为音频文件，无需用户手动转换为mp3等音频格式。
- 📄 多样化输出(完成)：增加输出格式选择，提供更多字幕格式选项，满足不同用户需求。
- 🔀 一键字幕视频：增加视频自动加字幕功能，一键完成从视频到带字幕视频的全流程。
- 🔗 API 集成：提供 API 接口，允许开发者将 AsrTools 集成到自己的工作流程中。
- ✏️ 字幕编辑器：集成一个简单的字幕编辑界面，允许用户直接修改、调整时间轴和校正识别错误。

 以上计划均已经实现，请访问 [VideoCaptioner](https://github.com/WEIFENG2333/VideoCaptioner)


### 🖥️ **快速上手**

1. **启动应用**：运行下载的可执行文件或通过命令行启动 GUI 界面。
2. **选择 ASR 引擎**：在下拉菜单中选择你需要使用的 ASR 引擎。
3. **添加文件**：点击“选择文件”按钮或将文件/文件夹拖拽到指定区域。
4. **开始处理**：点击“开始处理”按钮，程序将自动开始转换，并在完成后在原音频目录生成 `.srt` 或 `.txt` 字幕文件。（默认保持 3 个线程运行）

## 🛠️ **安装指南**

###  **1. 从发布版本安装**

我为 Windows 用户提供了打包好的[Release](https://github.com/WEIFENG2333/AsrTools/releases)版本，下载后解压即可直接使用，无需配置环境。

或者从网盘下载： [https://wwwm.lanzoue.com/iUJYZ2clk7xg](https://wwwm.lanzoue.com/iPKZV2eh5ina)

运行解压后的 `AsrTools.exe`，即可启动 GUI 界面。


###  **2. 从源码安装（开发者）**

项目的依赖仅仅为 `requests`。

如果您需要 GUI 界面，请额外安装 `PyQt5`, `qfluentwidgets`。

如果您想从源码运行，请按照以下步骤操作：

1. **克隆仓库并进入项目目录**

    ```bash
    git clone https://github.com/WEIFENG2333/AsrTools.git
    cd AsrTools
    ```

2. **安装依赖并运行**

    - **启动 GUI 界面**

        ```bash
        pip install -r requirements.txt
        python asr_gui.py
        ```

    - **使用命令行工具**

        ```bash
        pip install -r requirements.txt
        python asr_cli.py --help
        ```

        **命令行工具特性：**
        - 🎵 支持多种音频/视频格式
        - 🚀 支持三种ASR引擎（B接口、J接口、K接口）
        - 📄 支持TXT、SRT、ASS三种输出格式
        - ⚡ 支持批量处理和文件夹递归扫描
        - 💾 智能缓存机制，避免重复处理
        - 🔧 自动视频转音频功能

        **使用示例：**
        ```bash
        # 处理单个文件
        python asr_cli.py -i audio.mp3 -e b -f txt

        # 批量处理文件夹
        python asr_cli.py -i /path/to/audio/folder -e b -f srt

        # 处理视频文件
        python asr_cli.py -i video.mp4 -e j -f ass
        ```

        **安装到系统PATH（可选）：**
        ```bash
        python install_cli.py
        # 安装后可直接使用: asr_cli --help
        ```
---

## 日志
-  **（v1.1.0）已经增加视频文件支持🎥**：支持直接导入视频文件，自动转换为音频进行处理，无需手动转换。

## 📬 **联系与支持**

- **Issues**：[提交问题](https://github.com/WEIFENG2333/AsrTools/issues)

感谢您使用 **AsrTools**！🎉  

目前项目的相关调用和GUI页面的功能仍在不断完善中...

希望这款工具能为您带来便利。😊

---
## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WEIFENG2333/AsrTools&type=Date)](https://star-history.com/#WEIFENG2333/AsrTools&Date)
