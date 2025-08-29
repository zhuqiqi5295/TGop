# -*- coding:utf-8 -*

from telegram import ForceReply, Update, MessageOrigin
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
# pip install toml
# pip install nest_asyncio

import telegram
import asyncio

from telethon import TelegramClient, events

import os
import toml

import asyncio


class fmarket_bot(object):

    def __init__(self):
        super().__init__()

        self.toml_data = self.read_toml_file("./config.toml")
        print(self.toml_data)

        self.token = self.toml_data["telegram"]["token"]
        self.chat_id = self.toml_data["telegram"]["chat_id"]

        self.proxy_url = self.toml_data["proxy"]["url"]  # 替换为你的代理地址
        self.download_dir = self.toml_data["download"]["dir"]  # 视频保存目录

        os.makedirs(self.download_dir, exist_ok=True)  # 确保目录存在

    def main(self):

        # 创建应用
        self.application = (
            Application.builder().token(self.token).proxy(self.proxy_url).build()
        )

        # 注册处理器
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_logger)
        )
        self.application.add_handler(MessageHandler(filters.VIDEO, self.video_handler))

        self.application.run_polling()

    def read_toml_file(self, file_path):
        """
        读取并解析 TOML 文件内容
        :param file_path: TOML 文件路径
        :return: 解析后的字典
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = toml.load(file)
            return data
        except FileNotFoundError:
            print(f"文件未找到: {file_path}")
        except toml.TomlDecodeError as e:
            print(f"TOML 文件格式错误: {e}")

    async def _send_async(self, text: str):
        """异步发送消息"""
        await self.application.bot.send_message(chat_id=self.chat_id, text=text)

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

        message: MessageOrigin = update.message.forward_origin
        download = message.chat.link + "/" + str(message.message_id)

        print(download)

        log_message = f"""
        收到新视频消息:
        - 用户: {user.full_name} (@{user.username or 'N/A'}) [{user.id}]
        - 聊天: {chat.title or 'Private'} [{chat.id}]
        - 视频文件 ID: {video.file_id}
        - 视频大小: {video.file_size} 字节
        - 视频时长: {video.duration} 秒
        """
        print(log_message.strip())


if __name__ == "__main__":

    fmarket_bot().main()
