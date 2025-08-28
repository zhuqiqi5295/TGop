# -*- coding:utf-8 -*

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.ext import Updater, CommandHandler

# pip install python-telegram-bot
# pip install telethon

import telegram
import asyncio

import socket

from telethon import TelegramClient, events

import os

import subprocess

# api_id = 16612890
# api_hash = "c0fc7dab1acc44f2a2da55cba248d656"

# client = TelegramClient(
#     "session_name",
#     api_id,
#     api_hash,
#     proxy=("socks5", "127.0.0.1", 7890),
# )


class fmarket_bot(object):

    def __init__(self):
        super().__init__()

        # https://api.telegram.org/bot5865737744:AAGOcxcgvAkoFg9Tgwl33U3Y_GoCdNVnHas/getMe
        # https://api.telegram.org/bot5865737744:AAGOcxcgvAkoFg9Tgwl33U3Y_GoCdNVnHas/getupdates

        self.token = "5865737744:AAGOcxcgvAkoFg9Tgwl33U3Y_GoCdNVnHas"
        self.chat_id = 5751491127

        self.proxy_url = "http://127.0.0.1:7890"  # 替换为你的代理地址

        self.bot = telegram.Bot(self.token)

        self.download_dir = "downloads"  # 视频保存目录
        os.makedirs(self.download_dir, exist_ok=True)  # 确保目录存在

        self.loop = asyncio.get_event_loop_policy().get_event_loop()

    def send_message(self, text):
        self.loop.run_until_complete(self._send_async(text))

    async def _send_async(self, text: str):
        """异步发送消息"""
        await self.bot.send_message(chat_id=self.chat_id, text=text)

    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /start 命令"""
        await update.message.reply_text("Hello! 我已经准备好接收消息了!")

    async def message_logger(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """记录所有接收到的消息"""
        user = update.effective_user
        chat = update.effective_chat
        message = update.message

        log_message = f"""
        收到新消息:
        - 用户: {user.full_name} (@{user.username or 'N/A'}) [{user.id}]
        - 聊天: {chat.title or 'Private'} [{chat.id}]
        - 内容: {message.text or 'Non-text message'}
        - 时间: {message.date}
        """
        print(log_message.strip())

    async def video_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理接收到的视频消息"""
        video = update.message.video  # 获取视频对象
        user = update.effective_user
        chat = update.effective_chat

        log_message = f"""
        收到新视频消息:
        - 用户: {user.full_name} (@{user.username or 'N/A'}) [{user.id}]
        - 聊天: {chat.title or 'Private'} [{chat.id}]
        - 视频文件 ID: {video.file_id}
        - 视频大小: {video.file_size} 字节
        - 视频时长: {video.duration} 秒
        """
        print(log_message.strip())

        # 使用 tdl 下载视频
        try:
            file_path = os.path.join(
                self.download_dir, f"{video.file_id}.mp4"
            )  # 保存路径
            command = [
                ".\\tdl.exe",
                "download",
                "--output",
                file_path,
                video.file_id,  # 文件 ID
            ]
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"视频已下载并保存到: {file_path}")
            else:
                print(f"视频下载失败: {result.stderr}")
        except Exception as e:
            print(f"视频下载失败: {e}")

    async def main(self):
        """主函数"""
        # 创建应用
        self.application = (
            Application.builder().token(self.token).proxy(self.proxy_url).build()
        )

        # 注册处理器
        self.application.add_handler(CommandHandler("start", self.start_command))

        # 注册消息处理器
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_logger)
        )

        self.application.add_handler(MessageHandler(filters.VIDEO, self.video_handler))

        print("Telegram Bot 已启动，正在监听消息...")
        print("等待接收消息...")

        # 启动机器人
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

    async def main1(self):

        while True:
            await asyncio.sleep(30)
            await self._send_async("zhuqiqi")

    async def run_all(self):
        """同时运行所有任务"""
        tasks = [
            self.main(),
            self.main1(),
        ]

        await asyncio.gather(*tasks)

    def start(self):

        asyncio.run(self.run_all())


if __name__ == "__main__":

    fmarket_bot().start()
