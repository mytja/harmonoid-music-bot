from commands import *


class Playback(Commands):
    def __init__(self):
        super().__init__(Commands.bot)

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        await self.embed.queue(
            ctx,
            server.queue,
            server.queueIndex,
        )

    @commands.command(aliases=['n'])
    async def next(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        ''' Next Track '''
        server.modifiedQueueIndex = server.queueIndex + 1

    @commands.command(aliases=['b'])
    async def back(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        ''' Previous Track '''
        server.modifiedQueueIndex = server.queueIndex - 1

    @commands.command(aliases=['j'])
    async def jump(self, ctx, *, arg):
        if not (server := await Server.get(ctx)):
            return None
        ''' Previous Track '''
        try:
            server.modifiedQueueIndex = int(arg) - 1
        except:
            await self.embed.exception(
                ctx,
                'Invalid Jump',
                'No track is present at that index. 👀',
                '❌'
            )
    
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
        ''' Displaying Metadata '''
        try:
            server.queue.append(track)
            if server.queueIndex is None:
                ''' Show Now Playing '''
                if not server.voiceChannel:
                    await server.getVoiceChannel(ctx)
                server.queueIndex = -1
            else:
                ''' Show Added To Queue '''
                await self.embed.addedToQueue(ctx, track)
        except:
            await self.embed.exception(
                ctx,
                'Internal Error',
                'Could not add track to queue. ❌',
                '❌'
            )
        ''' Playing Track '''

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
