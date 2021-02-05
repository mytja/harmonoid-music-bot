from commands import *


class Lifecycle:
    @staticmethod
    async def listen():
        while True:
            await Commands.bot.wait_until_ready()
            for server in Commands.recognisedServers:
                try:
                    ''' Track Completed OR Jump '''
                    if (
                        not server.voiceConnection.is_playing() or type(server.modifiedQueueIndex) is int
                    ) and server.queue:
                        ''' Analysing Queue '''
                        if server.modifiedQueueIndex is None:
                            ''' Next Track On Completion '''
                            server.queueIndex += 1
                            if server.queueIndex >= len(server.queue):
                                ''' Queue Completed '''
                                continue
                            else:
                                track = server.queue[server.queueIndex]
                        else:
                            ''' Modified Index '''
                            if server.modifiedQueueIndex >= len(server.queue) or server.modifiedQueueIndex < 0:
                                await Embed().exception(
                                    server.context,
                                    'Invalid Jump',
                                    f'No track is present at that index. 👀',
                                    '❌'
                                )
                            else:
                                server.queueIndex = server.modifiedQueueIndex
                                track = server.queue[server.queueIndex]
                            server.modifiedQueueIndex = None
                        ''' Playing Track '''
                        voiceChannel = await server.getVoiceChannel(server.context)
                        try:
                            voiceChannel.play(discord.FFmpegOpusAudio(f'{track["trackId"]}.webm'))
                        except:
                            try:
                                voiceChannel.stop()
                                voiceChannel.play(discord.FFmpegOpusAudio(f'{track["trackId"]}.webm'))
                            except:
                                await Embed().exception(
                                    server.context,
                                    'Internal Error',
                                    f'Could not start player. 📻',
                                    '❌'
                                )
                        ''' Displaying Metadata '''
                        try:
                            await Embed().nowPlaying(server.context, track)
                        except:
                            await Embed().exception(
                                server.context,
                                'Now Playing',
                                'Could not send track information.\nMusic is still playing. 👌',
                                '👌'
                            )
                except:
                    pass
            await asyncio.sleep(2)