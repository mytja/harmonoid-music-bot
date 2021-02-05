from commands import *


class Playback(Commands):

    def __init__(self):
        super().__init__(Commands.bot)
    
    @commands.command(aliases=['p'])
    async def play(self, ctx, *, arg):
        if not (server := await Server.get(ctx)):
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
        ''' Playing Track '''
        voiceChannel = await server.getVoiceChannel(ctx)
        try:
            voiceChannel.play(discord.FFmpegOpusAudio(f'{track["trackId"]}.webm'))
        except:
            try:
                voiceChannel.stop()
                voiceChannel.play(discord.FFmpegOpusAudio(f'{track["trackId"]}.webm'))
            except:
                await self.embed.exception(
                    ctx,
                    'Internal Error',
                    f'Could not start player. 📻',
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
        if not (server := await Server.get(ctx)):
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
        ''' Playing Video '''
        voiceChannel = await server.getVoiceChannel(ctx)
        try:
            voiceChannel.play(discord.FFmpegPCMAudio(f'{video["id"]}.webm'))
        except:
            try:
                voiceChannel.stop()
                voiceChannel.play(discord.FFmpegPCMAudio(f'{video["id"]}.webm'))
            except:
                await self.embed.exception(
                    ctx,
                    'Internal Error',
                    f'Could not start player. 📻',
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
