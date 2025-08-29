# -*- coding:utf-8 -*


# TODO : youtube-dl.py jungleb 负责下载视频


import json
import yt_dlp

# pip install yt-dlp

URL = "https://www.bilibili.com/video/BV1PYeJzwEEH/?spm_id_from=333.40138.top_right_bar_window_history.content.click"

ydl_opts = {
    "proxy": "http://127.0.0.1:7890",
    "outtmpl": "downloads/%(title)s.%(ext)s",
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
    "ffmpeg_location": "./ffmpeg-8.0-full_build/bin/ffmpeg.exe",
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=False)

    # 打印所有可用格式信息及文件大小
    for fmt in info.get("formats", []):
        size = fmt.get("filesize") or fmt.get("filesize_approx")
        print(
            f"format_id: {fmt['format_id']}, 分辨率: {fmt.get('height')}, 文件大小: {size} 字节"
        )
