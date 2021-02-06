from commands import *


class About(Commands):

    def __init__(self):
        super().__init__(Commands.bot)
        
    @commands.command(aliases=['a'])
    async def about(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        await self.embed.about(ctx)
