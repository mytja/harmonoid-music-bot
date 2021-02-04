import asyncio
import aiofiles
import os

from discord.ext import commands
import harmonoidservice as hs
import logging
from harmonoidbot import *

logging.basicConfig(level=logging.DEBUG, filename="harmonoid-bot.log")

TOKEN = os.environ["DISCORD_TOKEN"]

bot = commands.AutoShardedBot(command_prefix="!")

harmonoid = hs.HarmonoidService()

vc = []
tc_id = []
vc_id = []
sr_id = []

"""
JSON for queue should look something like this:

{
    <server_id>: ["Song 1", "Song 2"...],
    <server_id>: ["Birds - Imagine Drangons", "Faded - Alan Walker"...],
}

Everything should be queried from YouTube (not YouTube Music)
"""

queueList = {}

error = 0

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    asyncio.ensure_future(playNext(), loop=bot.loop)
    asyncio.ensure_future(disconnectOnEmptyChannel(), loop=bot.loop)

class Playing:
    def __init__(self, bot):
        self.bot = bot

    @bot.command(aliases=["p"])
    async def play(ctx, *, arg):
        global vc
        global vc_id
        global error
        global sr_id

        server_id = ctx.message.guild.id

        if ctx.author == bot.user:
            return

        try:
            filename = await harmonoid.trackDownload(
                trackName=arg, trackId=None, albumId=None
            )
            if not filename:
                await ctx.send("Sorry, but we couldn't retrieve data for track")
                return
        except Exception as e:
            await ctx.send(
                f"Sorry, but there was an Internal Server Error :cry: ! Please report it to our maintainers! Unique error code: {error}"
            )
            logging.exception("\n\n--------\n\nException number " + str(error) + ": ")
            error += 1
            print(f"[track-download] {e}")
            return 500

        try:
            channel = discord.utils.get(ctx.guild.channels, name="Music")
            channel_id = channel.id
            channel = bot.get_channel(channel_id)
        except:
            await ctx.send("No voice channel called Music. Please create one.")
            return

        chat_id = ctx.message.channel.id

        if channel_id not in vc_id:
            print("[server-append] Server was not appended!")
            vc1 = await channel.connect()
            vc.append(vc1)
            tc_id.append(chat_id)
            vc_id.append(channel_id)
            sr_id.append(server_id)

        vcid = vc_id.index(channel_id)

        try:
            vc[vcid].play(
                discord.FFmpegPCMAudio(filename["trackId"] + ".ogg"),
                after=lambda e: print(
                    "[ffmpeg-player] Successfully summoned FFMPEG player!", e
                ),
            )
        except:
            try:
                vc[vcid].stop()
                vc[vcid].play(
                    discord.FFmpegPCMAudio(filename["trackId"] + ".ogg"),
                    after=lambda e: print(
                        "[ffmpeg-player] Successfully summoned FFMPEG player!", e
                    ),
                )
            except Exception as e:
                print(f"Failed to summon FFMPEG player - Exception: ", e)
                logging.exception("\n\n--------\n\nException number " + str(error) + ": ")
                ctx.send(
                    f"Failed to summon a player :cry: ... Please report a problem to our maintainers. Unique error code {error-1}"
                )
                error += 1
                return

        if len(channel.members) == 1:
            await ctx.send("Come and join me in the voice channel")
        try:
            await embedNow(music=filename, ctx=ctx)
        except Exception as e:
            print(f"[embed-exception] Exception: {e}")
            await ctx.send(
                "Failed to summon an embed :sad: ... Well, the song is still playing :wink: "
            )
        
        #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=filename["trackName"]))


    @bot.command(aliases=["play_yt", "py"])
    async def playYT(ctx, *, arg):
        global vc
        global vc_id
        global sr_id

        server_id = ctx.message.guild.id

        try:
            await harmonoid.youtube.getJS()
        except Exception as e:
            print(f"Failed to get JS: {e}")
            logging.exception("\n\n--------\n\nException number " + str(error) + ": ")
            error += 1

            await ctx.send(
                f"Failed to get JavaScript from a player :sad: . Trying to continue. Code to report to maintainers: {error-1}"
            )
        #if ctx.author == bot.user:
        #    return

        try:
            filename = await harmonoid.YTdownload(trackName=arg)
        except Exception as e:
            await ctx.send(
                f"Sorry, but there was an Internal Server Error. Please report it to our maintainers. Unique error ID: {error}"
            )
            logging.exception("\n\n--------\n\nException number " + str(error) + ": ")
            error += 1
            print(f"[track-download] {e}")
            return

        try:
            channel = discord.utils.get(ctx.guild.channels, name="Music")
            channel_id = channel.id
            channel = bot.get_channel(channel_id)
        except:
            await ctx.send("No voice channel called Music... Please create one.")
            return

        chat_id = ctx.message.channel.id

        if channel_id not in vc_id:
            print("[server-append] Server was not appended!")
            vc1 = await channel.connect()
            vc.append(vc1)
            tc_id.append(chat_id)
            vc_id.append(channel_id)
            sr_id.append(server_id)

        vcid = vc_id.index(channel_id)

        try:
            vc[vcid].play(
                discord.FFmpegPCMAudio(filename["trackId"] + ".ogg"),
                after=lambda e: print(
                    "[ffmpeg-player] Successfully summoned FFMPEG player!", e
                ),
            )
        except:
            try:
                vc[vcid].stop()
                vc[vcid].play(
                    discord.FFmpegPCMAudio(filename["trackId"] + ".ogg"),
                    after=lambda e: print(
                        "[ffmpeg-player] Successfully summoned FFMPEG player!", e
                    ),
                )
            except:
                print(f"Failed to summon FFMPEG player - Exception: ", e)
                logging.exception("\n\n--------\n\nException number " + str(error) + ": ")
                error += 1
                ctx.send(
                    f"Failed to summon a player :cry: ... Please report a problem to our maintainers. Unique error code {error-1}"
                )
                return

        if len(channel.members) == 1:
            await ctx.send("Come and join me in the voice channel")
        try:
            await embedNowYT(music=filename, ctx=ctx)
        except Exception as e:
            print(f"[embed-exception] Exception: {e}")
            await ctx.send(
                "Failed to summon an embed :sad: . But the song is still playing :wink: "
            )
        
async def pl_yt(songName, sr_id, chat_id, vc, vcid):

    server_id = sr_id
    tchannel = bot.get_channel(id=int(tc_id[vcid]))

    try:
        await harmonoid.youtube.getJS()
    except Exception as e:
        print(f"Failed to get JS: {e}")
        logging.exception("\n\n--------\n\nException number " + str(error) + ": ")
        error += 1
        await tchannel.send(
            f"Failed to get JavaScript from a player :sad: . Trying to continue. Code to report to maintainers: {error-1}"
        )
    #if ctx.author == bot.user:
    #    return

    try:
        filename = await harmonoid.YTdownload(trackName=songName)
    except Exception as e:
        await tchannel.send(
            f"Sorry, but there was an Internal Server Error. Please report it to our maintainers. Unique error ID: {error}"
        )
        logging.exception("\n\n--------\n\nException number " + str(error) + ": ")
        error += 1
        print(f"[track-download] {e}")
        return

    try:
        vc.play(
            discord.FFmpegPCMAudio(filename["trackId"] + ".ogg"),
            after=lambda e: print(
                "[ffmpeg-player] Successfully summoned FFMPEG player!", e
            ),
        )
    except:
        try:
            vc.stop()
            vc.play(
                discord.FFmpegPCMAudio(filename["trackId"] + ".ogg"),
                after=lambda e: print(
                    "[ffmpeg-player] Successfully summoned FFMPEG player!", e
                ),
            )
        except Exception as e:
            print(f"Failed to summon FFMPEG player - Exception: ", e)
            logging.exception("\n\n--------\n\nException number " + str(error) + ": ")
            error += 1
            tchannel.send(
                f"Failed to summon a player :cry: ... Please report a problem to our maintainers. Unique error code {error-1}"
            )
            return
    try:
        await embedNowYT_q(music=filename, tchannel=tchannel)
    except Exception as e:
        print(f"[embed-exception] Exception: {e}")
        await ctx.send(
            "Failed to summon an embed :sad: . But the song is still playing :wink: "
        )
        #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=filename["title"]))

# @bot.command()
# async def download(ctx, *, arg):
#    if ctx.author == bot.user:
#        return
#
#    await ctx.message.channel.send(file = discord.File(fp = await harmonoid.trackDownload(trackName = arg, trackId=None, albumId=None)))

class QueueManagment:
    def __init__(self, bot):
        self.bot = bot

    # Prints current queue for the server
    @bot.command(aliases=["q"])
    async def queue(ctx):
        server_id = ctx.message.guild.id
        msg = ""
        try:
            q = queueList[server_id]
        except:
            await ctx.send("Sorry, but there are no songs in queue")
            return
        
        if q == [] or q == None:
            await ctx.send("Sorry, but there are no songs in queue")
            return
        
        index = 0
        for qu in q:
            index += 1
            msg = msg + "\n" + str(index) + ". " + qu
        
        await ctx.send(msg)
    
    @bot.command(aliases=["pq", "add", "queue add"])
    async def playQueue(ctx, *, arg):
        global queueList
        result = await harmonoid.searchYT(arg)
        result = result["result"][0]
        server_id = ctx.message.guild.id
        try:
            queue = queueList[server_id]
        except:
            print("Appending queue to JSON")
            #z = json.loads(queueList)
            y = {server_id:[]}
            queueList.update(y)
        queuePos = len(queueList[server_id]) + 1
        queueList[server_id].append(result["title"])
        #queue = queue.append(result["title"])
        #queueList[server_id] = queue
        print(queueList)
        await addedToQueue(music = result, ctx = ctx, pos = queuePos)
    
    """
    @bot.command(aliases=["sq", "start queue"]
    async def queueStart(ctx):
        global sr_id
        global vc_id
        global vc
        global tc_id
        
        server_id = ctx.message.guild.id
        vcid = vc_id.index(channel_id)
        channel = discord.utils.get(ctx.guild.channels, name="Music")
        if channel.id not in vc_id:
            vc1 = await channel.connect()
            vc.append(vc1)
            tc_id.append(ctx.message.channel.id)
            vc_id.append(channel.id)
            sr_id.append(server_id)
        
        await ctx.send("Successfully connected to voice channel.")
    """        
    
    @bot.command(aliases=["rm"])
    async def remove(ctx, *, arg):
        global queueList
        
        server_id = ctx.message.guild.id
        
        try:
            q = int(arg) - 1
        except:
            ctx.send("Cannot remove! Given was a string instead of a position")
            return 
        try:
            del queueList[server_id][q]
            await ctx.send("Successfully removed song #"+str(q))
        except:
            await ctx.send("Failed to remove song #"+str(q))
    
    @bot.command(aliases=["qc", "c"])
    async def clear(ctx):
        global queueList
        
        server_id = ctx.message.guild.id
        
        try:
            queueList[server_id].clear()
            await ctx.send("Successfully cleared queue")
        except:
            await ctx.send("Failed to clear queue")


class PlayingUtils:
    def __init__(self, bot):
        self.bot = bot

    @bot.command(aliases=["s"])
    async def stop(ctx):
        server_id = ctx.message.channel.id
        tcid = tc_id.index(server_id)
        if tcid != None:
            if vc[tcid].is_playing():
                vc[tcid].stop()
                await ctx.send("Okay")
            else:
                await ctx.send("Cannot stop! No song is playing.")
        
        #await bot.change_presence(activity=None)


    @bot.command()
    async def pause(ctx):
        server_id = ctx.message.channel.id
        tcid = tc_id.index(server_id)
        if tcid != None:
            if vc[tcid].is_playing():
                vc[tcid].pause()
                await ctx.send("Okay")
            else:
                await ctx.send("Cannot pause! No song is playing.")


    @bot.command(aliases=["r"])
    async def resume(ctx):
        server_id = ctx.message.channel.id
        tcid = tc_id.index(server_id)
        if tcid != None:
            vc[tcid].resume()
            await ctx.send("Okay")


class Utils:
    def __init__(self, bot):
        self.bot = bot
    
    @bot.command()
    async def refresh(ctx):
        global vc
        global vc_id
        global tc_id
        tcid = tc_id.index(ctx.message.channel.id)

        try:
            tc_id.remove(ctx.message.channel.id)
        except:
            print("Server wasn't in list of servers, so it can't be refreshed!")

        try:
            await vc[tcid].stop()
        except:
            print("Couldn't stop!")

        try:
            await vc[tcid].disconnect()
        except:
            print("Couldn't disconnect from a voice channel!")

        # try:
        #    np[vcid] = None
        # except Exception as e:
        #    print(e)

        try:
            del vc[tcid]
            del vc_id[tcid]
            del tc_id[tcid]
        except:
            print("Server wasn't in list of servers, so it can't be refreshed!")

        await ctx.send("Succesfully refreshed server with ID: " + str(ctx.message.guild.id))

    @bot.command()
    async def disconnect(ctx):
        global vc
        global vc_id
        global tc_id
        tcid = tc_id.index(ctx.message.guild.id)

        try:
            await vc[tcid].stop()
        except:
            logging.exception("\n\n--------\n\[stop] Disconnect exception: ")

        try:
            await vc[tcid].disconnect()
        except:
            logging.exception("\n\n--------\n\[disconnect] Disconnect exception: ")
            return

        del tc_id[tcid]
        del vc_id[tcid]
        del vc[tcid]

        await ctx.send("Successfully disconnected from a voice channel :smiley: ")
    
    @bot.command(aliases=["conn"])
    async def connect(ctx):
        global sr_id
        global vc_id
        global vc
        global tc_id
        
        server_id = ctx.message.guild.id
        channel = discord.utils.get(ctx.guild.channels, name="Music")
        if channel.id not in vc_id:
            #vcid = vc_id.index(channel.id)
            vc1 = await channel.connect()
            vc.append(vc1)
            tc_id.append(ctx.message.channel.id)
            vc_id.append(channel.id)
            sr_id.append(server_id)
        
        await ctx.send("Successfully connected to voice channel.")

class About:
    def __init__(self, bot):
        self.bot = bot
        
    @bot.command()
    async def about(ctx):
        await embedAbout(ctx)


class Lyrics:
    def __init__(self, bot):
        self.bot = bot
        
    @bot.command()
    async def lyrics(ctx, *, arg):
        lyrics = await harmonoid.getLyrics(trackName=arg, trackId=None)
        print(lyrics)
        if lyrics["lyrics"]:
            lyrics = lyrics["lyrics"]
            if len(lyrics) > 1999:
                await ctx.send(
                    "Lyrics are longer than 2000 characters... Please use !lyricsSend to send lyrics in .txt file"
                )
            else:
                await ctx.send(lyrics)


    @bot.command()
    async def lyricsSend(ctx, *, arg):
        lyrics = await harmonoid.getLyrics(trackName=arg, trackId=None)
        trackId = await harmonoid.searchYoutube(keyword=arg, mode="track")
        print(trackId)
        trackId = trackId["result"][0]["trackId"]
        if os.path.isfile(f"{trackId}.txt"):
            print(
                f"[lyrics] Lyrics already downloaded for track ID: {trackId}.\n[server] Sending audio binary for track ID: {trackId}."
            )
            await ctx.send(file=discord.File(trackId + ".txt"))
        elif lyrics["lyrics"]:
            lyrics = lyrics["lyrics"]
            filename = trackId + ".txt"
            async with aiofiles.open(filename, "w", encoding="UTF-8") as file:
                await file.write(lyrics)
            await ctx.send(file=discord.File(trackId + ".txt"))

async def disconnectOnEmptyChannel():
    global vc
    global vc_id
    global tc_id

    while True:
        try:
            for voice_id in vc_id:
                vcid = vc_id.index(voice_id)
                await bot.wait_until_ready()
                channel = bot.get_channel(id=voice_id)
                if len(channel.members) < 2:
                    try:
                        await vc[vcid].stop()
                    except:
                        print("Nothing is playing")
                    try:
                        await vc[vcid].disconnect()
                    except:
                        print("Failed to disconnect")
                    del tc_id[vcid]
                    del vc_id[vcid]
                    del vc[vcid]
                    #await bot.change_presence(status=discord.Status.idle)
        except Exception as e:
            print(e)
        await asyncio.sleep(600)  # Do it every 10 minutes

async def playNext():
    global vc
    global vc_id
    global tc_id
    global sr_id
    global queueList

    while True:
        try:
            for voice_id in vc_id:
                vcid = vc_id.index(voice_id)
                await bot.wait_until_ready()
                tchannel = bot.get_channel(id=int(tc_id[vcid]))
                serverId = sr_id[vcid]

                #print("Queue checking!")
                #print(f"[voice-channel] {vc}")
                #print(f"[voice-id] {vc_id}")
                #print(f"[text-channel] {tc_id}")
                #print(f"[serverId] {sr_id}")
                print(f"[queue-list] {queueList}")
                #print(f"[is-playing] {vc[vcid].is_playing()}")

                if vc[vcid].is_playing() or queueList[serverId] == None or queueList[serverId] == []:
                    print("Skipping, since it still is playing!")
                else:
                    print("Nothing is playing! Playing next in queue")
                    await tchannel.send("Playing next in queue!")
                    await pl_yt(vcid=vcid, vc=vc[vcid], chat_id=tchannel, songName=queueList[serverId][0], sr_id=serverId)
                    del queueList[serverId][0]
                    #await bot.change_presence(status=discord.Status.idle)
        except Exception as e:
            print(e)
        await asyncio.sleep(1)  # Do it every 5 seconds

def setup(bot):
    bot.add_cog(Playing(bot))
    bot.add_cog(PlayingUtils(bot))
    bot.add_cog(Lyrics(bot))
    bot.add_cog(About(bot))
    bot.add_cog(Utils(bot))
    bot.add_cog(QueueManagment(bot))

if __name__ == "__main__":
    bot.run(TOKEN)
