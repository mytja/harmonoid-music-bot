import discord
import asyncio
from source.method import Method


class Embed:

    async def nowPlaying(self, context, track):
        await self.__createEmbed(
            context,
            'Now Playing',
            f'**[{track["trackName"]}](https://music.youtube.com/watch?v={track["trackId"]})**',
            track['albumArtHigh'],
            [
                EmbedField('Album', track['albumName'], True),
                EmbedField('Year', track['year'], True),
                EmbedField('Duration', Method.formatDuration(track['trackDuration']), True),
                EmbedField('Artists', ', '.join(track['trackArtistNames']), False),
            ],
            '🎶',
            True,
        )
    
    async def nowPlayingYT(self, context, video):
        await self.__createEmbed(
            context,
            'Now Playing',
            f'**[{video["title"]}]({video["link"]})**',
            video['thumbnails'][-1]['url'],
            [
                EmbedField('Channel', video['channel']['name'], False),
                EmbedField('Duration', Method.formatDuration(int(video['streamingData']['formats'][0]['approxDurationMs']) // 1000), True),
                EmbedField('Year', video['publishDate'].split('-')[0], True),
            ],
            '🎶',
            True,
        )

    async def addedToQueue(self, context, track, position):
        await self.__createEmbed(
            context,
            'Added To Queue',
            f'**[{track["trackName"]}](https://music.youtube.com/watch?v={track["trackId"]})**',
            track['albumArtHigh'],
            [
                EmbedField('Duration', track['duration'], True),
                EmbedField('Position', track['duration'], True),
            ],
            '📑',
            True,
        )

    async def about(self, context):
        developers = ''
        for developer in ['mytja', 'alexmercerind', 'raitonoberu']:
            developers += f'[{developer}](https://github.com/{developer})\n'
        await self.__createEmbed(
            context,
            'About',
            '''
            Hello! 👋
            I'm Harmonoid Music Bot. 
            I can play music for you & get lyrics. 🎉
            I play music from both YouTube music & YouTube unlike other bots.
            You may join our discord server from the link below to provide feedback or just chill with us.

            Thankyou,
            Harmonoid project developers.
            ''',
            'https://avatars.githubusercontent.com/u/75374037?s=200&v=4',
            [
                EmbedField('Support', 'Discord Server: [Join](https://discord.gg/ZG7Pj9SREG)\nSource Code: [Contribute](https://github.com/harmonoid/harmonoid-music-bot)', False),
                EmbedField('Version', 'beta-1.0.0', False),
                EmbedField('Developers', developers, False),
            ],
            '💜',
            False,
        )

    async def exception(self, context, title, exception, reaction):
        await self.__createEmbed(
            context,
            title,
            exception,
            None,
            [],
            reaction,
            True,
        )

    async def __createEmbed(self, context, title: str, description: str, thumbnail:str, fields: list, reaction: str, isMonospaced: bool):
        asyncio.ensure_future(context.message.add_reaction('👌'))
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Colour.random(),
        )
        if thumbnail:
            embed.set_image(url=thumbnail)
        for field in fields:
            embed.add_field(
                name=field.title,
                value=f'`{field.value}`' if isMonospaced else field.value,
                inline=field.inline
            )
        embed.set_footer(
            text=f'Requested by {context.author.name}',
            icon_url=context.author.avatar_url
        )
        message = await context.send(embed=embed)
        asyncio.ensure_future(message.add_reaction(reaction))


class EmbedField:

    def __init__(self, title: str, value: str, inline: bool):
        self.title = title
        self.value = value
        self.inline = inline

