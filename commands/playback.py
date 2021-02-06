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
        ''' Run mainloop to notice modifiedQueueIndex. '''
        await Commands.listenUpdates()

    @commands.command(aliases=['b'])
    async def back(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        ''' Previous Track '''
        server.modifiedQueueIndex = server.queueIndex - 1
        ''' Run mainloop to notice modifiedQueueIndex. '''
        await Commands.listenUpdates()

    @commands.command(aliases=['j'])
    async def jump(self, ctx, *, arg):
        if not (server := await Server.get(ctx)):
            return None
        server.modifiedQueueIndex = int(arg) - 1
        ''' Run mainloop to notice modifiedQueueIndex. '''
        await Commands.listenUpdates()
    
    @commands.command(aliases=['d'])
    async def delete(self, ctx, *, arg):
        if not (server := await Server.get(ctx)):
            return None
        removeIndex = int(arg) - 1
        for index, track in enumerate(server.queue):
            if removeIndex == index:
                await self.embed.removedFromQueue(
                    ctx,
                    server.queue[index],
                )
                server.queue.pop(index)
                break
        if removeIndex < server.queueIndex:
            server.queueIndex -= 1
        elif removeIndex == server.queueIndex:
            server.modifiedQueueIndex = server.queueIndex
            if not server.queue and server.voiceConnection:
                await server.disconnect()
            ''' Run mainloop to notice modifiedQueueIndex. '''
            await Commands.listenUpdates()
        else:
            pass

    @commands.command(aliases=['c'])
    async def clear(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        server.queue.clear()
        await server.disconnect()
        await self.embed.exception(
            ctx,
            'Cleared Queue',
            'Queue is now empty. 🗑',
            '📑'
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
                    'Could not retrieve track information. ℹ',
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
        try:
            ''' Add To Queue '''
            server.queue.append(track)
            if not server.voiceConnection:
                await server.connect()
                ''' Run mainloop to notice server.voiceConnection. '''
                await Commands.listenUpdates()
            else:
                ''' Show addedToQueue if already connected to voiceChannel. '''
                await self.embed.addedToQueue(ctx, track)
            
        except:
            await self.embed.exception(
                ctx,
                'Internal Error',
                'Could not add track to queue. 📑',
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
                    'Could not retrieve video information. ℹ',
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
        voiceChannel = await server.connect()
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
