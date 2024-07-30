import discord
import openai
from discord.ext import commands
from gtts import gTTS
from io import BytesIO
import asyncio
import pytube
import os
from yt_dlp import YoutubeDL
import ffmpeg


import json
import requests
import wave


ydl_video_opts = {
    'outtmpl': 'audio.mp3',
    'format': 'bestaudio'
}

openai.api_key = "api_key"


client = discord.Client(intents=discord.Intents.all())

async def download_video(url):
    loop = asyncio.get_running_loop()
    ydl = YoutubeDL(ydl_opts)
    await loop.run_in_executor(None, ydl.download, [url])

async def play_music(message, source):
    message.guild.voice_client.play(source)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.bot:
        return
    
    if message.content == "!vc":
        if message.author.voice is None:
            await message.channel.send("ボイスチャットに接続してね")
            return
        # ボイスチャンネルに接続する
        vc = await message.author.voice.channel.connect()
        await message.channel.send("VC ON")

    elif message.content == "!exit":
        if message.guild.voice_client is None:
            await message.channel.send("ボイスチャットに接続してね")
            return

        # 切断する
        await message.guild.voice_client.disconnect()

        await message.channel.send("VC OFF")
    
    elif "youtube.com/watch?v=" in message.content:
        if message.guild.voice_client is None:
            await message.channel.send("ボイスチャットに接続してね")
            return

        try:
            if os.path.exists("audio.mp3"):
                os.remove("audio.mp3")
            # ダウンロード
            await message.channel.send("DL NOW")
            # 音声をダウンロードする
            with YoutubeDL(ydl_video_opts) as ydl:
                result = ydl.download([
                    message.content,
                ])
            
            # 再生
            await message.channel.send("PLAY")
            source = discord.FFmpegPCMAudio("audio.mp3")
            source = discord.PCMVolumeTransformer(source, volume=0.04)
            message.guild.voice_client.play(source)
        except Exception as e:
            # エラーが発生した場合
            await message.channel.send(f"エラーです: {e}")
        finally:
            # ダウンロードしたファイルを削除する
            await message.channel.send(f"終わり")

    elif "!music!" in message.content:
        if message.guild.voice_client is None:
            await message.channel.send("ボイスチャットに接続してね")
            return

        try:
            if os.path.exists("audio.mp3"):
                os.remove("audio.mp3")
            # ダウンロード
            await message.channel.send("DL NOW")

            
            # 音声をダウンロードする
            search_query = message.content.replace("music!", "")
            ydl_video_opts_word['query'] = search_query.strip()
            with YoutubeDL(ydl_video_opts_word) as ydl:
                result = ydl.extract_info('ytsearch1:' + ydl_video_opts_word['query'], download=True)
            
            # 再生
            await message.channel.send("再生開始")
            source = discord.FFmpegPCMAudio("audio.mp3")
            source = discord.PCMVolumeTransformer(source, volume=0.04)
            message.guild.voice_client.play(source)
        except Exception as e:
            # エラーが発生した場合
            await message.channel.send(f"Error : {e}")
        finally:
            # ダウンロードしたファイルを削除する
            await message.channel.send(f"END")
    
    elif message.content == "!stop":
        if message.guild.voice_client is None:
            await message.channel.send("ボイスチャットに接続してね")
            return

        # 音声を停止する
        message.guild.voice_client.stop()
        await message.channel.send("音声停止")



client.run('clientkey')