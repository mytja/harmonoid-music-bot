from commands import *


class Controls(Commands):

    def __init__(self):
        super().__init__(Commands.bot)

    @commands.command(aliases=['s'])
    async def pause(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
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
        server.resume()
        await self.embed.text(
            ctx,
            'Resumed Music. ▶',
            '✅'
        )
