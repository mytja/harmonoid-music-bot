from commands import *


class Playback(Commands):
    def __init__(self, bot):
        super().__init__(bot)
    
    @commands.command(aliases=['p'])
    async def play(self, ctx, *, arg):
        serverId = ctx.message.guild.id
        if ctx.author == self.bot.user:
            return None
        ''' Downloading Track '''
        try:
            track = await self.youtubeMusic.download(arg)
            if not track:
                await self.embed.exception(
                    ctx,
                    'Internal Error',
                    'Could not retrieve track information. ❌',
                    '❌'
                )
                return None
        except:
            await self.embed.exception(
                ctx,
                'No Result',
                f'Could not find the track. 🔎',
                '❌'
            )
            return None
        ''' Managing Server & Channel IDs '''
        try:
            voiceChannelId = discord.utils.get(ctx.guild.channels, name='Music').id
        except:
            await self.embed.exception(
                ctx,
                'Information',
                'Please make a voice channel with name "Music" first. 🔧',
                '❌'
            )
            return None
        textChannelId = ctx.message.channel.id
        if voiceChannelId not in Commands.voiceChannelIds:
            voiceChannel = await self.bot.get_channel(voiceChannelId).connect()
            Commands.voiceChannels.append(voiceChannel)
            Commands.voiceChannelIds.append(voiceChannelId)
            Commands.textChannelIds.append(textChannelId)
            Commands.serverIds.append(serverId)
        ''' Playing Track '''
        voiceChannelIndex = Commands.voiceChannelIds.index(voiceChannelId)
        try:
            Commands.voiceChannels[voiceChannelIndex].play(discord.FFmpegOpusAudio(f'{track["trackId"]}.webm'))
        except:
            try:
                Commands.voiceChannels[voiceChannelId].stop()
                Commands.voiceChannels[voiceChannelId].play(discord.FFmpegOpusAudio(f'{track["trackId"]}.webm'))
            except:
                await self.embed.exception(
                    ctx,
                    'Internal Error',
                    f'Could not start FFmpeg player. 📻',
                    '❌'
                )
                return None
        ''' Displaying Metadata '''
        try:
            await self.embed.nowPlaying(ctx, track)
        except:
            await self.embed.exception(
                ctx,
                'Now Playing',
                'Could not send track information.\nMusic is still playing. 👌',
                '👌'
            )

    @commands.command(aliases=['py'])
    async def playYT(self, ctx, *, arg):
        serverId = ctx.message.guild.id
        if ctx.author == self.bot.user:
            return None
        ''' Downloading Video '''
        try:
            video = await self.youtube.download(arg)
            if not video:
                await self.embed.exception(
                    ctx,
                    'Internal Error',
                    'Could not retrieve video information. ❌',
                    '❌'
                )
                return None
        except:
            await self.embed.exception(
                ctx,
                'No Result',
                f'Could not find the video. 🔎',
                '❌'
            )
            return None
        ''' Managing Server & Channel IDs '''
        try:
            voiceChannelId = discord.utils.get(ctx.guild.channels, name='Music').id
        except:
            await self.embed.exception(
                ctx,
                'Information',
                'Please make a voice channel with name "Music" first. 🔧',
                '❌'
            )
            return None
        textChannelId = ctx.message.channel.id
        if voiceChannelId not in Commands.voiceChannelIds:
            voiceChannel = await self.bot.get_channel(voiceChannelId).connect()
            Commands.voiceChannels.append(voiceChannel)
            Commands.voiceChannelIds.append(voiceChannelId)
            Commands.textChannelIds.append(textChannelId)
            Commands.serverIds.append(serverId)
        ''' Playing Track '''
        voiceChannelIndex = Commands.voiceChannelIds.index(voiceChannelId)
        try:
            Commands.voiceChannels[voiceChannelIndex].play(discord.FFmpegPCMAudio(f'{video["id"]}.webm'))
        except:
            try:
                Commands.voiceChannels[voiceChannelId].stop()
                Commands.voiceChannels[voiceChannelId].play(discord.FFmpegPCMAudio(f'{video["id"]}.webm'))
            except:
                await self.embed.exception(
                    ctx,
                    'Internal Error',
                    f'Could not start FFmpeg player. 📻',
                    '❌'
                )
                return None
        ''' Displaying Metadata '''
        try:
            await self.embed.nowPlayingYT(ctx, video)
        except:
            await self.embed.exception(
                ctx,
                'Now Playing',
                'Could not send video information.\nMusic is still playing. 😅',
                '😅'
            )
