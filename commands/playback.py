from commands import *


class Playback(Commands):
    def __init__(self):
        super().__init__(Commands.bot)

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        if not (server := await Server.get(ctx)):
            await self.embed.exception(
                ctx,
                'Internal Error',
                'Please join a voice channel before requesting any music. ℹ',
                '❌'
            )
            return None
        await self.embed.queue(
            ctx,
            server.queue,
            server.queueIndex,
        )

    @commands.command()
    async def latency(self, ctx):
        server: Server = await Server.get(ctx)
        if not server:
            await self.embed.exception(
                ctx,
                'Internal Error',
                'Please join a voice channel before requesting any music. ℹ',
                '❌'
            )
            return None
        await self.embed.latency(ctx, server.get_latency())

    @commands.command()
    async def changeChannel(self, ctx):
        await self.embed.exception(
            ctx,
            'Internal Error',
            'Oops, this command was recently removed. You don\'t to setup a channel before playback, just hop into a voice channel & get started with music playback. ℹ',
            '❌'
        )
        return None

    @commands.command(aliases=['n', 's'])
    async def next(self, ctx):
        if not (server := await Server.get(ctx, connect=True)):
            await self.embed.exception(
                ctx,
                'Internal Error',
                'Please join a voice channel before requesting any music. ℹ',
                '❌'
            )
            return None
        ''' Next Track '''
        server.modifiedQueueIndex = server.queueIndex + 1
        ''' Run mainloop to notice modifiedQueueIndex. '''
        await Commands.listenUpdates()

    @commands.command(aliases=['b'])
    async def back(self, ctx):
        if not (server := await Server.get(ctx, connect=True)):
            await self.embed.exception(
                ctx,
                'Internal Error',
                'Please join a voice channel before requesting any music. ℹ',
                '❌'
            )
            return None
        ''' Previous Track '''
        server.modifiedQueueIndex = server.queueIndex - 1
        ''' Run mainloop to notice modifiedQueueIndex. '''
        await Commands.listenUpdates()

    @commands.command(aliases=['j'])
    async def jump(self, ctx, *, arg):
        if not (server := await Server.get(ctx, connect=True)):
            await self.embed.exception(
                ctx,
                'Internal Error',
                'Please join a voice channel before requesting any music. ℹ',
                '❌'
            )
            return None
        server.modifiedQueueIndex = int(arg) - 1
        ''' Run mainloop to notice modifiedQueueIndex. '''
        await Commands.listenUpdates()
    
    @commands.command(aliases=['d'])
    async def delete(self, ctx, *, arg):
        if not (server := await Server.get(ctx)):
            await self.embed.exception(
                ctx,
                'Internal Error',
                'Please join a voice channel before requesting any music. ℹ',
                '❌'
            )
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
            await self.embed.exception(
                ctx,
                'Internal Error',
                'Please join a voice channel before requesting any music. ℹ',
                '❌'
            )
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
        if not (server := await Server.get(ctx, connect=True)):
            await self.embed.exception(
                ctx,
                'Internal Error',
                'Please join a voice channel before requesting any music. ℹ',
                '❌'
            )
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
        except Exception as exception:
            print(exception)
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
                if server.voiceConnection.is_playing():
                    ''' Only add to queue if something is playing. '''
                    await self.embed.addedToQueue(ctx, track)
                else:
                    ''' Run mainloop if something is not playing. '''
                    server.queueIndex -= 1
                    await Commands.listenUpdates()
        except Exception as e:
            print(e)
            await self.embed.exception(
                ctx,
                'Internal Error',
                'Could not add track to queue. 📑',
                '❌'
            )

    @commands.command(aliases=['py'])
    async def playYT(self, ctx, *, arg):
        if not (server := await Server.get(ctx, connect=True)):
            await self.embed.exception(
                ctx,
                'Internal Error',
                'Please join a voice channel before requesting any music. ℹ',
                '❌'
            )
            return None
        ''' Downloading Track '''
        try:
            video = await youtube.download(arg)
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
        try:
            ''' Add To Queue '''
            server.queue.append(video)
            if not server.voiceConnection:
                await server.connect()
                ''' Run mainloop to notice server.voiceConnection. '''
                await Commands.listenUpdates()
            else:
                if server.voiceConnection.is_playing():
                    ''' Only add to queue if something is playing. '''
                    await self.embed.addedToQueue(ctx, video)
                else:
                    ''' Run mainloop if something is not playing. '''
                    server.queueIndex -= 1
                    await Commands.listenUpdates()
        except Exception as e:
            print(e)
            await self.embed.exception(
                ctx,
                'Internal Error',
                'Could not add video to queue. 📑',
                '❌'
            )
