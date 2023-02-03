from commands import *
from commands.playback import Playback
from commands.controls import Controls
from commands.lyrics import Lyrics
from commands.about import About
from scripts.youtube import youtube

if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.message_content = True
    Commands.bot = commands.AutoShardedBot(
        command_prefix='-',
        help_command=None,
        intents=intents,
    )
    Commands.bot.add_cog(Playback())
    Commands.bot.add_cog(Controls())
    Commands.bot.add_cog(Lyrics())
    Commands.bot.add_cog(About())
    @Commands.bot.event
    async def on_ready():
        await youtube.init_fetcher()
        await Commands.bot.change_presence(
            activity=discord.Activity(
                name='-help 👀',
                type=3,
            ),
        )
    import os
    TOKEN = os.environ.get('DISCORD_TOKEN')
    Commands.bot.run(TOKEN)
