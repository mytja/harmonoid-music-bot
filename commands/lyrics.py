from commands import *


class Lyrics(Commands):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command()
    async def lyrics(self, ctx, *, arg):
        lyrics = await self.youtubeMusic.getLyrics(arg)
        if lyrics:
            if len(lyrics['lyrics']) > 1800:
                lyrics['lyrics'] = f'{lyrics["lyrics"][0: 1800]}\n...'
                lyrics['source'] += '\nLyrics contain more than 2000 characters. Use !lyricsSend to get them in a TXT file.'
            await self.embed.lyrics(
                ctx,
                lyrics,
            )
        else:
            await self.embed.exception(
                ctx,
                'Lyrics Not Found',
                'Lyrics are not present for this track. 📖',
                '❌'
            )
    
    @commands.command()
    async def lyricsSend(self, ctx, *, arg):
        lyrics = await self.youtubeMusic.getLyrics(arg, True)
        if lyrics:
            await self.embed.file(
                ctx,
                'lyrics.txt',
                '📄'
            )
        else:
            await self.embed.exception(
                ctx,
                'Lyrics Not Found',
                'Lyrics are not present for this track. 📖',
                '❌'
            )