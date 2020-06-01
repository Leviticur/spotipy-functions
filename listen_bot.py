import os
from time import sleep

import discord
from discord.ext import commands
import youtube_dl
from youtube_search import YoutubeSearch

client = commands.Bot(command_prefix='!')

listeners = {}
voices = {}

ydl_opt = {
    'format': 'bestaudio/best',
    'outtmpl': '',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


async def listening(guild, author=None):
    if guild not in voices or not voices[guild]:
        if author:
            channel = author.voice.channel
            voice = await channel.connect()
            voices[guild] = voice
        else:
            print("Could create voice client because no author was given")

    for activity in listeners[guild].activities:
        if activity.name == "Spotify":
            title_artist = f"{activity.title} {activity.artist}"
            results = YoutubeSearch(title_artist, max_results=1)
            if results.videos:
                url = f"https://www.youtube.com{results.videos[0]['link']}"
                if voices[guild].is_playing():
                    voices[guild].stop()

                sleep((1/50))

                for file in os.listdir("./"):
                    if file == f"{guild.id}.mp3":
                        os.remove(file)

                ydl_opt['outtmpl'] = f"{guild.id}.mp3"

                with youtube_dl.YoutubeDL(ydl_opt) as ydl:
                    ydl.download([url])
                voices[guild].play(discord.FFmpegPCMAudio(f"{guild.id}.mp3"))
                voices[guild].source = discord.PCMVolumeTransformer(voices[guild].source)
                voices[guild].source.volume = .05
                print("")
            else:
                print("Could not find video")


@client.command()
async def listen(ctx, listened):
    for member in ctx.guild.members:
        if member.nick and member.nick.lower() == listened.lower():
            listeners[ctx.guild] = member
        elif member.name.lower() == listened.lower():
            listeners[ctx.guild] = member

    if ctx.guild in listeners and listeners[ctx.guild]:
        await listening(ctx.guild, ctx.author)


@client.event
async def on_member_update(before, after):
    for guild, listened in listeners.items():
        if after == listened:
            await listening(guild)


@client.event
async def on_voice_state_update(member, before, after):
    if member == client.user and before.channel and not after.channel:
        voices[member.guild] = None
        listeners[member.guild] = None


client.run("NzA5NTAxMDcwODgzNDIyMjA4.Xrm0Yw.oilPxgpEjKjaACZoq1Wyg9pkALo")
