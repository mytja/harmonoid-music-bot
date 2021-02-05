import discord
from discord.ext import commands
import asyncio

from source.embed import Embed
from scripts.youtube import YouTube
from scripts.youtubemusic import YouTubeMusic


class Commands(commands.Cog):
    ''' Static Members '''
    bot = None
    recognisedServers = []

    def __init__(self, bot):
        self.bot = bot
        self.embed = Embed()
        self.youtubeMusic = YouTubeMusic()
        self.youtube = YouTube()


class Server:

    def __init__(self, context, serverId, voiceChannelId, textChannelId):
        self.context = context
        self.serverId = serverId
        self.voiceChannelId = voiceChannelId
        self.textChannelId = textChannelId
        self.voiceChannel = None
        self.textChannel = None
        self.voiceConnection = None
        self.queueIndex = None
        self.modifiedQueueIndex = None
        self.queue = []

    async def getVoiceChannel(self, context):
        if not self.voiceConnection:
            self.voiceChannel = Commands.bot.get_channel(discord.utils.get(context.guild.channels, name='Music').id)
            self.textChannel = Commands.bot.get_channel(self.textChannelId)
            await self.connect()
        return self.voiceConnection

    async def connect(self):
        self.voiceConnection = await self.voiceChannel.connect()

    async def disconnect(self):
        await self.voiceChannel.disconnect()
        self.voiceConnection = None

    def resume(self):
        self.voiceConnection.resume()

    def pause(self):
        self.voiceConnection.pause()

    def stop(self):
        self.voiceConnection.stop()

    @staticmethod
    async def get(context):
        asyncio.ensure_future(context.message.add_reaction('👀'))
        for server in Commands.recognisedServers:
            if server.serverId == context.message.guild.id:
                return server
        try:
            voiceChannelId = discord.utils.get(context.guild.channels, name='Music').id
        except:
            await Embed().exception(
                context,
                'Information',
                'Please make a voice channel with name "Music" first. 🔧',
                '❌'
            )
            return None
        Commands.recognisedServers.append(
            Server(
                context,
                context.message.guild.id,
                voiceChannelId,
                context.message.channel.id,
            )
        )
        return Commands.recognisedServers[-1]
