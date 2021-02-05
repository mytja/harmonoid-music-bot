from commands import *
from commands.playback import Playback
from commands.controls import Controls
from commands.queue import Queue
from commands.lyrics import Lyrics
from commands.about import About
from commands.lifecycle import Lifecycle


if __name__ == '__main__':
    Commands.bot = commands.AutoShardedBot(
        command_prefix='!'
    )
    Commands.bot.add_cog(Playback())
    Commands.bot.add_cog(Controls())
    Commands.bot.add_cog(Queue())
    Commands.bot.add_cog(Lyrics())
    Commands.bot.add_cog(About())
    @Commands.bot.event
    async def on_ready():
        print('Connected to Discord.')
        asyncio.ensure_future(
            Lifecycle.listen(),
            loop=Commands.bot.loop
        )
    import os
    TOKEN = os.environ.get('DISCORD_TOKEN')
    Commands.bot.run(TOKEN)
