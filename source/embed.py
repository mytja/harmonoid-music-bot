from typing import Optional

import discord
import asyncio
from source.method import Method
from constants import Constants


class Embed:

    async def nowPlaying(self, context, track):
        if 'trackName' in track.keys():
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
        else:
            video = track
            await self.__createEmbed(
                context,
                'Now Playing',
                f'**[{video["title"]}](https://youtu.be/{video["id"]})**',
                video['thumbnails'][-1]['url'],
                [
                    EmbedField('Channel', video['uploader'], False),
                    EmbedField('Duration', f'{video["duration"]//60}:{video["duration"]%60}', True),
                ],
                '🎶',
                True,
            )
    
    async def lyrics(self, context, lyrics):
        await self.__createEmbed(
            context,
            'Lyrics',
            f'**[{lyrics["title"]}](https://youtube.com/watch?v={lyrics["videoId"]})**',
            lyrics['thumbnails'][-1]['url'],
            [
                EmbedField('Album', lyrics['album']['name'], inline = False),
                EmbedField('Artists', ', '.join([artist['name'] for artist in lyrics['artists']]), inline = False),
            ],
            '🎹',
            True,
        )
        await self.__createText(
            context,
            f'```{lyrics["lyrics"]}```\n{lyrics["source"]}',
            '🎹'
        )

    async def addedToQueue(self, context, track):
        if 'trackName' in track.keys():
            await self.__createEmbed(
                context,
                'Added To Queue',
                f'**[{track["trackName"]}](https://music.youtube.com/watch?v={track["trackId"]})**',
                track['albumArtHigh'],
                [
                    EmbedField('Album', track['albumName'], True),
                    EmbedField('Year', track['year'], True),
                    EmbedField('Duration', Method.formatDuration(track['trackDuration']), True),
                    EmbedField('Artists', ', '.join(track['trackArtistNames']), False),
                ],
                '📑',
                True,
            )
        else:
            video = track
            await self.__createEmbed(
                context,
                'Added To Queue',
                f'**[{video["title"]}](https://youtu.be/{video["id"]})**',
                video['thumbnails'][-1]['url'],
                [
                    EmbedField('Channel', video['uploader'], False),
                    EmbedField('Duration', video["duration_string"], True),
                ],
                '🎶',
                True,
            )

    async def channel_leave(self, ctx):
        await self.__createEmbed(
            ctx,
            'Left the voice channel',
            f'The bot has left the voice channel in order to save some bandwidth. To make the bot rejoin, run any playback (-py, -p) command while in voice channel.',
            None,
            [],
            'ℹ',
            True,
        )

    async def latency(self, ctx, latency):
        await self.__createEmbed(
            ctx,
            'Latency',
            f'**Average latency is {latency}**',
            None,
            [],
            'ℹ',
            True,
        )

    async def removedFromQueue(self, context, track):
        if 'trackName' in track.keys():
            await self.__createEmbed(
                context,
                'Removed From Queue',
                f'**[{track["trackName"]}](https://music.youtube.com/watch?v={track["trackId"]})**',
                None,
                [
                    EmbedField('Album', track['albumName'], True),
                    EmbedField('Year', track['year'], True),
                    EmbedField('Duration', Method.formatDuration(track['trackDuration']), True),
                    EmbedField('Artists', ', '.join(track['trackArtistNames']), False),
                ],
                '📑',
                True,
            )
        else:
            video = track
            await self.__createEmbed(
                context,
                'Removed From Queue',
                f'**[{video["title"]}]({video["link"]})**',
                None,
                [
                    EmbedField('Channel', video['channel']['name'], False),
                    EmbedField('Duration', Method.formatDuration(video["duration"]["secondsText"]), True),
                ],
                '🎶',
                True,
            )

    async def queue(self, context, queue, queueIndex):
        if not queue:
            await self.exception(
                context,
                'Empty Queue',
                'No tracks found in the queue. 📑',
                '📑'
            )
            return None
        queueString = ''
        for index, query in enumerate(queue):
            if queueIndex == index:
                queueString += '🎵'
            elif queueIndex < index:
                queueString += '❎'
            elif queueIndex > index:
                queueString += '✅'
            if 'trackName' in query.keys():
                queueString += f'  {index + 1}. {query["trackName"]} - _{", ".join(query["trackArtistNames"])}_\n    {Method.formatDuration(query["trackDuration"])}\n'
            else:
                queueString += f'  {index + 1}. {query["title"]} - _{query["uploader"]}_\n    {query["duration_string"]}\n'
        await self.__createEmbed(
            context,
            'Queue',
            'Tracks in the queue',
            None,
            [
                EmbedField('Coming Up', queueString, False),
            ],
            '📑',
            False,
        )

    async def about(self, context):
        developers = ''
        for developer in ['mytja', 'alexmercerind', 'raitonoberu']:
            developers += f'[{developer}](https://github.com/{developer})\n'
        await self.__createEmbed(
            context,
            'About',
            Constants.description,
            'https://avatars.githubusercontent.com/u/75374037?s=200&v=4',
            [
                EmbedField('Support', 'Discord Server: [Join](https://discord.gg/2Rc3edFWd8)\nSource Code: [Contribute](https://github.com/mytja/harmonoid-music-bot)', False),
                EmbedField('Version', Constants.version, False),
                EmbedField('Developers', developers, False),
            ],
            '💜',
            False,
        )

    async def help(self, context):
        await self.__createEmbed(
            context,
            'Help',
            'Information about all the commands',
            'https://avatars.githubusercontent.com/u/75374037?s=200&v=4',
            [
                EmbedField(
                    '-play <song name or link>',
                    '-p <song name or link>\nPlays or adds a track to queue from YouTube Music.',
                    False,
                ),
                EmbedField(
                    '-playYT <song name or link>',
                    '-py <song name or link>\nPlays or adds a track to queue from YouTube.',
                    False,
                ),
                EmbedField(
                    '-pause',
                    'Pauses playback. Recommended to use -pp instead.',
                    False,
                ),
                EmbedField(
                    '-resume',
                    'Resumes playback. Recommended to use -pp instead.',
                    False,
                ),
                EmbedField(
                    '-togglePlayback',
                    '-pp\nSwitches between pause & play states.',
                    False,
                ),
                EmbedField(
                    '-queue',
                    '-q\nDisplays the current queue.',
                    False,
                ),
                EmbedField(
                    '-next',
                    '-n\nJumps to next track in the queue.',
                    False,
                ),
                EmbedField(
                    '-back',
                    '-b\nJumps to previous track in the queue.',
                    False,
                ),
                EmbedField(
                    '-jump <position in queue>',
                    '-j <position in queue>\nJumps to specific track in the queue based on its position.',
                    False,
                ),
                EmbedField(
                    '-delete <position in queue>',
                    '-d <position in queue>\nRemoves track from the queue from the given position.',
                    False,
                ),
                EmbedField(
                    '-clear',
                    '-c\nClears the queue.',
                    False,
                ),
                EmbedField(
                    '-latency',
                    'Shows the latency of music playback.',
                    False,
                ),
                EmbedField(
                    '-lyrics <song name or link>',
                    '-l\nShows lyrics of a track.',
                    False,
                ),
                EmbedField(
                    '-lyricsSend <song name or link>',
                    '-ls\nSends lyrics of a track in a TXT file.',
                    False,
                ),
                EmbedField(
                    '-status',
                    '-s\nDisplays statistics of the bot.',
                    False,
                ),
                EmbedField(
                    '-about',
                    '-a\nDisplays information about bot & developer support.',
                    False,
                ),
            ],
            'ℹ',
            False,
        )

    async def status(self, context, commands):
        import ytmusicapi
        import youtubesearchpython
        import aiofiles
        import nacl
        try:
            async with aiofiles.open('runtime.txt') as file:
                runtime = await file.read()
        except:
            import sys
            runtime = sys.version
        playingMusicOnServers = 0
        for server in commands.recognisedServers:
            if server.voiceConnection:
                if server.voiceConnection.is_playing():
                    playingMusicOnServers += 1
        await self.__createEmbed(
            context,
            'Status',
            f'Information about Harmonoid Music Bot.',
            None,
            [
                EmbedField('Total Servers', f'{len(commands.bot.guilds)} servers', inline = False),
                EmbedField('Recognized Servers', f'{len(commands.recognisedServers)} servers', inline = False),
                EmbedField('Playing Music On', f'{playingMusicOnServers} servers', inline = False),
                EmbedField('This Server', f'{context.message.guild.name} in {context.message.channel.mention} channel.', inline = False),
                EmbedField('Dependencies', f'\npycord {discord.__version__}\nytmusicapi {ytmusicapi.__version__}\nyoutube-search-python {youtubesearchpython.__version__}\npynacl {nacl.__version__}''', inline = False),
                EmbedField('Runtime', f'{runtime}', inline = False),
            ],
            'ℹ',
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
            color = discord.Color.red()
        )

    async def file(self, context, fileName, reaction):
        message = await context.send(
            file=discord.File(fileName),
        )
        asyncio.ensure_future(message.add_reaction(reaction))

    async def __createEmbed(self, context, title: str, description: str, thumbnail: Optional[str], fields: list, reaction: str, isMonospaced: bool, color = discord.Color.from_rgb(179, 136, 255)):
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
        )
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        for field in fields:
            embed.add_field(
                name=field.title,
                value=f'`{field.value}`' if isMonospaced else field.value,
                inline=field.inline
            )
        embed.set_footer(
            text=f'Requested by {context.author.name}',
            icon_url=context.author.avatar.url
        )
        message = await context.send(embed=embed)
        asyncio.ensure_future(message.add_reaction(reaction))
    
    async def __createText(self, context, text: str, reaction: str):
        message = await context.send(text)
        asyncio.ensure_future(message.add_reaction(reaction))


class EmbedField:

    def __init__(self, title: str, value: str, inline: bool):
        self.title = title
        self.value = value
        self.inline = inline

