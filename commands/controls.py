from commands import *


class Controls(Commands):

    def __init__(self):
        super().__init__(Commands.bot)

    @commands.command(aliases=['s'])
    async def stop(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        if not server.isStopped:
            server.stop()
            await self.embed.text(
                ctx,
                'Stopped Music. ⏹',
                '✅'
            )

    @commands.command()
    async def pause(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        if not server.isPaused:
            server.pause()
            await self.embed.text(
                ctx,
                'Paused Music. ⏸',
                '✅'
            )

    @commands.command(aliases=['r'])
    async def resume(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        if server.isPaused:
            server.resume()
            await self.embed.text(
                ctx,
                'Resumed Music. ▶',
                '✅'
            )
