from commands import *


class About(Commands):

    def __init__(self):
        super().__init__(Commands.bot)
        
    @commands.command()
    async def about(self, ctx):
        await self.embed.about(ctx)