import discord
from discord.ext import commands

from source.embed import Embed
from scripts.youtube import YouTube
from scripts.youtubemusic import YouTubeMusic


class Commands(commands.Cog):
    ''' Static Members '''
    voiceChannels = []
    voiceChannelIds = []
    textChannelIds = []
    serverIds = []

    def __init__(self, bot):
        self.bot = bot
        self.embed = Embed()
        self.youtubeMusic = YouTubeMusic()
        self.youtube = YouTube()

