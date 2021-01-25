# bot.py
import os

import discord
from discord.ext import commands
from discord.ext.commands import AutoShardedBot
import harmonoidservice as hs

TOKEN = os.environ['DISCORD_TOKEN']

bot = commands.AutoShardedBot(command_prefix='!')

harmonoid = hs.HarmonoidService()

vc = []
vc_id = []

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def download(ctx, *, arg):
    if ctx.author == bot.user:
        return

    await ctx.message.channel.send(file = discord.File(fp = await harmonoid.trackDownload(trackName = arg, trackId=None, albumId=None)))

@bot.command()
async def play(ctx, *, arg):
    global vc
    global vc_id
    if ctx.author == bot.user:
        return

    filename = await harmonoid.trackDownload(trackName = arg, trackId=None, albumId=None)

    channel = discord.utils.get(ctx.guild.channels, name="Music")
    channel_id = channel.id
    channel = bot.get_channel(channel_id)
    
    server_id = ctx.message.guild.id
    
    if server_id not in vc_id:
        print("[server-append] Server was not appended!")
        vc1 = await channel.connect()
        vc.append(vc1)
        vc_id.append(server_id)
    
    vcid = vc_id.index(server_id)
    
    try:
        vc[vcid].play(discord.FFmpegPCMAudio(filename), after=lambda e: print('[ffmpeg-player] Successfully summoned FFMPEG player!', e))
    except Exception as e:
        print(f"Failed to summon FFMPEG player - Exception: ", e)
    
    if (len(channel.members) == 1):
        await ctx.send("Come and join me in the voice channel")
    else:
        await ctx.send("Okay")

@bot.command()
async def stop(ctx):
    server_id = ctx.message.guild.id
    if vc.index(server_id) != None:
        if vc.index(server_id).is_playing():
            vc.index(server_id).stop()
            await ctx.send("Okay")
        else:
            await ctx.send("Cannot stop! No song is playing!")

@bot.command()
async def pause(ctx):
    server_id = ctx.message.guild.id
    if vc.index(server_id) != None:
        if vc.index(server_id).is_playing():
            vc.index(server_id).pause()
            await ctx.send("Okay")
        else:
            await ctx.send("Cannot pause! No song is playing!")

@bot.command()
async def resume(ctx):
    server_id = ctx.message.guild.id
    if vc.index(server_id) != None:
        vc.resume()
        await ctx.send("Okay")


bot.run(TOKEN)
