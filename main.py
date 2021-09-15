from commands import *
from commands.playback import Playback
from commands.controls import Controls
from commands.lyrics import Lyrics
from commands.about import About


if __name__ == '__main__':
    Commands.bot = commands.AutoShardedBot(
        command_prefix='-',
        help_command=None,
    )
    Commands.bot.add_cog(Playback())
    Commands.bot.add_cog(Controls())
    Commands.bot.add_cog(Lyrics())
    Commands.bot.add_cog(About())
    @Commands.bot.event
    async def on_ready():
        await Commands.bot.change_presence(
            activity=discord.Activity(
                name='-help 👀',
                type=3,
            ),
        )
    import os
    TOKEN = os.environ.get('DISCORD_TOKEN')
    Commands.bot.run(TOKEN)
