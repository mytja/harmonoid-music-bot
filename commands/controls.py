from commands import *


class Controls(Commands):

    def __init__(self):
        super().__init__(Commands.bot)

    @commands.command(aliases=['pp'])
    async def togglePlayback(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        if server.voiceConnection:
            if server.voiceConnection.is_playing():
                server.pause()
                asyncio.ensure_future(ctx.message.add_reaction('⏸'))
            else:
                server.resume()
                asyncio.ensure_future(ctx.message.add_reaction('▶'))
        else:
            await self.embed.exception(
                ctx,
                'Invalid Command',
                'Nothing is playing. 🎶',
                '❌',
            )
    
    @commands.command()
    async def resume(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        if server.voiceConnection:
            if server.voiceConnection.is_paused():
                server.resume()
                asyncio.ensure_future(ctx.message.add_reaction('▶'))
            else:
                await self.embed.exception(
                    ctx,
                    'Invalid Command',
                    'Already playing. 🎶',
                    '❌',
                )

    @commands.command()
    async def pause(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        if server.voiceConnection:
            if server.voiceConnection.is_playing():
                server.pause()
                asyncio.ensure_future(ctx.message.add_reaction('⏸'))
            else:
                await self.embed.exception(
                    ctx,
                    'Invalid Command',
                    'Already paused. 🎶',
                    '❌',
                )
    
    @commands.command(aliases=['cc'])
    async def changeChannel(self, ctx, *, arg):
        if not (server := await Server.get(ctx)):
            return None
        await server.changeChannel(
            ctx,
            arg,
        )
        await self.embed.exception(
            ctx,
            'Voice Channel Change',
            f'Voice channel successfully changed to "{arg}".',
            '✅',
        )
    
