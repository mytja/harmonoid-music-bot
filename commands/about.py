from commands import *


class About(Commands):

    def __init__(self):
        super().__init__(Commands.bot)
        
    @commands.command()
    async def about(self, ctx):
        await self.embed.about(ctx)

    @commands.command(aliases=['h'])
    async def help(self, ctx):
        await self.embed.help(ctx)

    @commands.command()
    async def status(self, ctx):
        await self.embed.status(ctx, Commands)
