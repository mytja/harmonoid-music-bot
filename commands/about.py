from commands import *


class About(Commands):

    def __init__(self, bot):
        super().__init__(bot)
        
    @commands.command()
    async def about(self, ctx):
        await self.embed.about(ctx)
