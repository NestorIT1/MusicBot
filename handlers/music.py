import os
import time
import logging
from aiogram import types, Dispatcher
import yt_dlp

class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
    def __init__(self):
        super(FilenameCollectorPP, self).__init__(None)
        self.filenames = []

    def run(self, information):
        self.filenames.append(information["filepath"])
        return [], information

async def search(message: types.Message):
    arg = message.get_args()
    await message.reply('Очікуйте...')
    YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'noplaylist': 'True',
        'ffmpeg_location': 'Your location ffmpeg',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',    
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }
    filename_collector = FilenameCollectorPP()
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        ydl.add_post_processor(filename_collector)
        try:
            result = ydl.extract_info(f"ytsearch:{arg}", download=True)
            logging.info(f"Result: {result}")
        except Exception as e:
            logging.error(f"Пішли нахуй, я не можу найти")
            await message.reply(f"Помилка завантаження: я не можу найти")
            return

    if filename_collector.filenames:
        await message.reply_document(open(filename_collector.filenames[0], 'rb'))
        time.sleep(5)
        os.remove(filename_collector.filenames[0])
    else:
        await message.reply(f"Помилка завантаження: я не можу найти")

async def youtube(message: types.Message):
    arguments = message.get_args()
    await message.reply("Очікуйте...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': 'Your location ffmpeg',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }
    filename_collector = FilenameCollectorPP()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.add_post_processor(filename_collector)
        try:
            result = ydl.extract_info(arguments, download=True)
            logging.info(f"Result: {result}")
        except Exception as e:
            logging.error(f"Failed to download: {e}")
            await message.reply(f"Помилка завантаження: я не можу найти")
            return

    if filename_collector.filenames:
        await message.reply_document(open(filename_collector.filenames[0], 'rb'))
        time.sleep(5)
        os.remove(filename_collector.filenames[0])
    else:
        await message.reply(f"Помилка завантаження:я не можу найти")

def register_handlers_music(dp: Dispatcher):
    dp.register_message_handler(search, commands=['y'])
    dp.register_message_handler(youtube, commands=['yt'])
