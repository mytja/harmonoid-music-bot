import os
from commands import *
from commands.playback import Playback
from commands.controls import Controls
from commands.lyrics import Lyrics
from commands.about import About


if __name__ == '__main__':
    harmonoidMusicBot = commands.AutoShardedBot(
        command_prefix='!'
    )
    harmonoidMusicBot.add_cog(Playback(harmonoidMusicBot))
    harmonoidMusicBot.add_cog(Controls(harmonoidMusicBot))
    harmonoidMusicBot.add_cog(Lyrics(harmonoidMusicBot))
    harmonoidMusicBot.add_cog(About(harmonoidMusicBot))
    TOKEN = os.environ.get('DISCORD_TOKEN')
    harmonoidMusicBot.run(TOKEN)
