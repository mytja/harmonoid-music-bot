from typing import List

import discord
from discord.ext import commands
import asyncio

from source.embed import Embed
from scripts.youtube import youtube
from scripts.youtubemusic import YouTubeMusic


FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


class Lifecycle:
    @staticmethod
    async def update():
        print("Updating lifecycle")
        for server in Commands.recognisedServers:
            ''' Empty Queue '''
            if not server.queue:
                continue
            ''' Not In Voice Channel '''
            if not server.voiceConnection:
                continue
            if not server.voiceConnection.is_playing() and type(server.modifiedQueueIndex) is int:
                ''' Jump on the completion of queue. '''
                if server.modifiedQueueIndex >= len(server.queue) or server.modifiedQueueIndex < 0:
                    await Embed().exception(
                        server.context,
                        'Invalid Jump',
                        f'No track is present at that index. 👀',
                        '❌'
                    )
                    server.modifiedQueueIndex = None
                    continue
                else:
                    server.queueIndex = server.modifiedQueueIndex
                    server.modifiedQueueIndex = None
            elif not server.voiceConnection.is_playing():
                ''' Track Completed '''
                print(server.queueIndex, len(server.queue))
                if server.queueIndex + 1 >= len(server.queue):
                    await server.disconnect()
                    await Embed().channel_leave(server.context)
                    continue
                else:
                    server.queueIndex += 1
            elif type(server.modifiedQueueIndex) is int:
                ''' Jump '''
                if server.modifiedQueueIndex >= len(server.queue) or server.modifiedQueueIndex < 0:
                    await Embed().exception(
                        server.context,
                        'Invalid Jump',
                        f'No track is present at that index. 👀',
                        '❌'
                    )
                    server.modifiedQueueIndex = None
                    continue
                else:
                    server.queueIndex = server.modifiedQueueIndex
                    server.modifiedQueueIndex = None
            else:
                ''' No Change '''
                continue
            ''' Track Playback '''
            track = server.queue[server.queueIndex]
            #print(f"Playing track {track}")
            url = track["requested_formats"][-1]["url"]
            print(f"Fetched URL {url}")
            try:
                server.voiceConnection.play(
                    discord.FFmpegOpusAudio(url, **FFMPEG_OPTS),
                    after=lambda exception: asyncio.run_coroutine_threadsafe(
                        Commands.listenUpdates(), Commands.bot.loop
                    ),
                )
                #print(f"Played track {track}")
                ''' Run mainloop after playback completion. '''
            except:
                try:
                    server.stop()
                    server.voiceConnection.play(
                        discord.FFmpegOpusAudio(url, **FFMPEG_OPTS),
                        after=lambda exception: asyncio.run_coroutine_threadsafe(
                            Commands.listenUpdates(), Commands.bot.loop
                        ),
                    )
                    ''' Run mainloop after playback completion. '''
                except:
                    await Embed().exception(
                        server.context,
                        'Internal Error',
                        f'Could not start player. 📻',
                        '❌'
                    )
            ''' Displaying Metadata '''
            try:
                await Embed().nowPlaying(server.context, track)
            except Exception as e:
                print(e)
                await Embed().exception(
                    server.context,
                    'Now Playing',
                    'Could not send track information.\nMusic is still playing. 😅',
                    '🎶'
                )


class Server:
    def __init__(self, context, serverId, voiceChannel):
        self.context = context
        self.serverId = serverId
        self.voiceChannel = voiceChannel
        self.voiceConnection = None
        self.queueIndex = -1
        self.modifiedQueueIndex = None
        self.queue = []

    async def connect(self):
        if not self.voiceConnection:
            self.voiceConnection = await self.voiceChannel.connect()

    async def disconnect(self):
        if self.voiceConnection:
            await self.voiceConnection.disconnect()
        self.voiceConnection = None
        self.queueIndex = -1
        self.modifiedQueueIndex = None

    def change_context(self, context):
        self.context = context

    def get_latency(self) -> float:
        return self.voiceConnection.average_latency

    def resume(self):
        self.voiceConnection.resume()

    def pause(self):
        self.voiceConnection.pause()

    def stop(self):
        self.voiceConnection.stop()

    @staticmethod
    async def get(context, connect: bool = False):
        asyncio.ensure_future(context.message.add_reaction('👀'))
        for server in Commands.recognisedServers:
            if server.serverId != context.message.guild.id:
                continue
            if context.author.voice:
                server.voiceChannel = context.author.voice.channel
                if server.voiceConnection:
                    await server.voiceConnection.move_to(server.voiceChannel)
                elif connect:
                    try:
                        await server.connect()
                    except Exception as e:
                        continue
            if connect and not server.voiceConnection:
                return None
            server.change_context(context)
            return server
        serverId = context.message.guild.id
        if context.author.voice is None:
            return None
        voiceChannel = context.author.voice.channel
        Commands.recognisedServers.append(
            Server(
                context,
                serverId,
                voiceChannel,
            )
        )
        return Commands.recognisedServers[-1]


class Commands(commands.Cog):
    """ Static Members """
    bot = None
    recognisedServers: List[Server] = []

    @staticmethod
    async def listenUpdates():
        await Lifecycle.update()

    def __init__(self, bot):
        self.bot = bot
        self.embed = Embed()
        self.youtubeMusic = YouTubeMusic()
