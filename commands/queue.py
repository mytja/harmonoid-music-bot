from commands import *


class Queue(Commands):
    def __init__(self):
        super().__init__(Commands.bot)

    @commands.command(aliases=['n'])
    async def next(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        ''' Playing Track '''
        track = server.queue[0]
        voiceChannel = await server.getVoiceChannel(server.context)
        try:
            voiceChannel.play(discord.FFmpegOpusAudio(f'{track["trackId"]}.webm'))
        except:
            try:
                voiceChannel.stop()
                voiceChannel.play(discord.FFmpegOpusAudio(f'{track["trackId"]}.webm'))
            except:
                await Embed().exception(
                    server.context,
                    'Internal Error',
                    f'Could not start player. 📻',
                    '❌'
                )
                return None
        ''' Displaying Metadata '''
        try:
            await Embed().nowPlaying(server.context, track)
        except:
            await Embed().exception(
                server.context,
                'Now Playing',
                'Could not send track information.\nMusic is still playing. 👌',
                '👌'
            )
        server.queue.pop(0)

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        await self.embed.queue(
            ctx,
            server.queue,
        )
    
    @commands.command(aliases=['pq', 'add', 'queue add'])
    async def playQueue(self, ctx, *, arg):
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
            await self.embed.addedToQueue(ctx, track)
        except:
            await self.embed.exception(
                ctx,
                'Internal Error',
                'Could not add track to queue. ❌',
                '❌'
            )
        ''' Playing Track '''
